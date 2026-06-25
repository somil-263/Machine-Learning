from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "employees.db"

def get_db_connection():
    """Helper function For connecting the database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Function for create the table and it run for the first time"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    
    if not data or 'name' not in data or 'salary' not in data:
        return jsonify({"error": "Invalid data! 'name' aur 'salary' are required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, salary) VALUES (?, ?)",
        (data['name'], data['salary'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"message": "Employee added successfully!", "id": new_id}), 201

@app.route('/employee', methods=['GET'])
def get_all_employees():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    
    employees = [dict(row) for row in rows]
    return jsonify(employees), 200

@app.route('/employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    conn.close()
    
    if row is None:
        return jsonify({"error": f"Employee with ID {emp_id} not found"}), 404
        
    return jsonify(dict(row)), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)