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
