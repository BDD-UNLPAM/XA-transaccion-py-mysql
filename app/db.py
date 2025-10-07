import os
import mysql.connector

def get_conn_a():
    return mysql.connector.connect(
        host=os.getenv('BANK_A_HOST', 'bank_a_db'),
        port=int(os.getenv('BANK_A_PORT', 3306)),
        user=os.getenv('BANK_A_USER', 'root'),
        password=os.getenv('BANK_A_PASSWORD', 'rootpass'),
        database=os.getenv('BANK_A_DB', 'bank_a'),
        autocommit=False
    )

def get_conn_b():
    return mysql.connector.connect(
        host=os.getenv('BANK_B_HOST', 'bank_b_db'),
        port=int(os.getenv('BANK_B_PORT', 3306)),
        user=os.getenv('BANK_B_USER', 'root'),
        password=os.getenv('BANK_B_PASSWORD', 'rootpass2'),
        database=os.getenv('BANK_B_DB', 'bank_b'),
        autocommit=False
    )

def get_prepared_transactions():
    """
    Devuelve las transacciones XA PREPARED de ambos bancos.
    """
    results = []
    connections = {
        "bank_a": mysql.connector.connect(
            host="bank_a_db",
            user="root",
            password="rootpass",
            database="bank_a"
        ),
        "bank_b": mysql.connector.connect(
            host="bank_b_db",
            user="root",
            password="rootpass2",
            database="bank_b"
        )
    }

    prepared_a = []
    prepared_b = []

    try:
        cursor_a = connections["bank_a"].cursor()
        cursor_a.execute("XA RECOVER")
        prepared_a = [row for row in cursor_a.fetchall()]

        cursor_b = connections["bank_b"].cursor()
        cursor_b.execute("XA RECOVER")
        prepared_b = [row for row in cursor_b.fetchall()]
    finally:
        for conn in connections.values():
            conn.close()

    return prepared_a, prepared_b
