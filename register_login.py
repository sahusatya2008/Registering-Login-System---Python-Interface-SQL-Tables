#10) Registering & Login System - Python Interface + SQL Databases
import mysql.connector
import os, hashlib
import getpass

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "root123"
DB_NAME = "schooldb"

def connect_db():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

def create_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "username VARCHAR(50) PRIMARY KEY, "
        "salt VARCHAR(64), "
        "pwd_hash VARCHAR(64))"
    )
    con.commit(); con.close()

def hash_with_salt(salt_hex, password):
    # returns sha256 hex of salt + password
    return hashlib.sha256((salt_hex + password).encode()).hexdigest()

def register():
    create_table()
    con = connect_db(); cur = con.cursor()
    uname = input("Enter new username: ").strip()
    pwd = getpass.getpass("Enter new password (hidden): ").strip()

    cur.execute("SELECT username FROM users WHERE username=%s", (uname,))
    if cur.fetchone():
        print("Username already exists. Try another.")
    else:
        salt = os.urandom(16).hex()                 # 16 bytes salt -> 32 hex chars
        pwd_hash = hash_with_salt(salt, pwd)
        cur.execute("INSERT INTO users (username, salt, pwd_hash) VALUES (%s,%s,%s)", (uname, salt, pwd_hash))
        con.commit()
        print("Registration successful!")
    con.close()

def login():
    create_table()
    con = connect_db(); cur = con.cursor()
    uname = input("Enter username: ").strip()
    pwd = getpass.getpass("Enter password (hidden): ").strip()

    cur.execute("SELECT salt, pwd_hash FROM users WHERE username=%s", (uname,))
    row = cur.fetchone()
    if not row:
        print("Invalid username or password!")
    else:
        salt, stored_hash = row
        if hash_with_salt(salt, pwd) == stored_hash:
            print(f"Login successful! Welcome, {uname}")
        else:
            print("Invalid username or password!")
    con.close()

def main():
    while True:
        print("\n===== LOGIN SYSTEM =====")
        print("1. Register\n2. Login\n3. Exit")
        ch = input("Enter choice: ").strip()
        if ch == '1': register()
        elif ch == '2': login()
        elif ch == '3':
            print("Goodbye!"); break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
