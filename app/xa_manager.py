import uuid

class XAException(Exception):
    pass

def make_xid():
    return 'xid-' + uuid.uuid4().hex

def xa_start(cursor, xid):
    cursor.execute(f"XA START '{xid}'")

def xa_end(cursor, xid):
    cursor.execute(f"XA END '{xid}'")

def xa_prepare(cursor, xid):
    cursor.execute(f"XA PREPARE '{xid}'")

def xa_commit(cursor, xid):
    cursor.execute(f"XA COMMIT '{xid}'")

def xa_rollback(cursor, xid):
    cursor.execute(f"XA ROLLBACK '{xid}'")
