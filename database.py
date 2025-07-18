import mysql.connector
from db_config import host, user, password, database

def create_connection():
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(100),
            salary FLOAT
        )
    """)
    conn.commit()
    conn.close()

def insert_employee(name, department, salary):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)", (name, department, salary))
    conn.commit()
    conn.close()

def get_all_employees():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    conn.close()
    return data

def search_employees(keyword):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE name LIKE %s OR department LIKE %s", (f"%{keyword}%", f"%{keyword}%"))
    data = cursor.fetchall()
    conn.close()
    return data

def update_employee(emp_id, name, department, salary):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET name=%s, department=%s, salary=%s WHERE id=%s", (name, department, salary, emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
    conn.commit()
    conn.close()
