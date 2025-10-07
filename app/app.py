from flask import Flask, render_template, request
from db import get_conn_a, get_conn_b
from xa_manager import make_xid, xa_start, xa_end, xa_prepare, xa_commit, xa_rollback, XAException
import decimal
import os

app = Flask(__name__)
app.secret_key = 'devsecret'
API_KEY = os.getenv('API_KEY', 'supersecretkey')

@app.route('/')
def index():
    conn_a = get_conn_a()
    conn_b = get_conn_b()
    cur_a = conn_a.cursor(dictionary=True)
    cur_b = conn_b.cursor(dictionary=True)
    cur_a.execute('SELECT * FROM accounts')
    cur_b.execute('SELECT * FROM accounts')
    accounts_a = cur_a.fetchall()
    accounts_b = cur_b.fetchall()
    cur_a.close(); cur_b.close(); conn_a.close(); conn_b.close()
    return render_template('index.html', accounts_a=accounts_a, accounts_b=accounts_b)

@app.route('/transfer', methods=['POST'])
def transfer():
    key = request.form.get('api_key') or request.headers.get('X-API-KEY')
    if key != API_KEY:
        return "Unauthorized", 401

    src_acc = int(request.form['src_acc'])
    dst_acc = int(request.form['dst_acc'])
    amount = decimal.Decimal(request.form['amount'])

    xid = make_xid()
    conn_a = get_conn_a()
    conn_b = get_conn_b()
    cur_a = conn_a.cursor()
    cur_b = conn_b.cursor()

    try:
        xa_start(cur_a, xid)
        xa_start(cur_b, xid)

        cur_a.execute('SELECT balance FROM accounts WHERE id=%s FOR UPDATE', (src_acc,))
        row = cur_a.fetchone()
        if not row:
            raise XAException('Source account not found')
        src_balance = decimal.Decimal(row[0])
        if src_balance < amount:
            raise XAException('Insufficient funds')

        cur_b.execute('SELECT balance FROM accounts WHERE id=%s FOR UPDATE', (dst_acc,))
        rowb = cur_b.fetchone()
        if not rowb:
            raise XAException('Destination account not found')

        new_src = src_balance - amount
        cur_a.execute('UPDATE accounts SET balance=%s, version=version+1 WHERE id=%s', (new_src, src_acc))
        cur_b.execute('SELECT balance FROM accounts WHERE id=%s', (dst_acc,))
        dst_balance = decimal.Decimal(cur_b.fetchone()[0])
        new_dst = dst_balance + amount
        cur_b.execute('UPDATE accounts SET balance=%s, version=version+1 WHERE id=%s', (new_dst, dst_acc))

        xa_end(cur_a, xid)
        xa_end(cur_b, xid)
        xa_prepare(cur_a, xid)
        xa_prepare(cur_b, xid)
        xa_commit(cur_a, xid)
        xa_commit(cur_b, xid)

        return render_template('result.html', success=True, message=f'Transfer successful (xid={xid})')
    except Exception as e:
        try: xa_rollback(cur_a, xid)
        except Exception: pass
        try: xa_rollback(cur_b, xid)
        except Exception: pass
        return render_template('result.html', success=False, message=str(e))
    finally:
        cur_a.close(); cur_b.close(); conn_a.close(); conn_b.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
