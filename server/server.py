from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def get_primary_db_connection():
    return psycopg2.connect(
        dbname="university",
        user="postgresadmin",
        password="admin123",
        host="postgres_primary",
        port="5432"
    )

def get_replica_db_connection():
    return psycopg2.connect(
        dbname="university",
        user="postgresadmin",
        password="admin123",
        host="postgres_replica",
        port="5432"
    )

@app.route('/students/primary', methods=['GET'])
def get_students_primary():
    try:
        conn = get_primary_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": s[0], "имя": s[1], "фамилия": s[2], "группа": s[3]} for s in students])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch students from primary: {str(e)}"}), 500

@app.route('/students/replica', methods=['GET'])
def get_students_replica():
    try:
        conn = get_replica_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": s[0], "имя": s[1], "фамилия": s[2], "группа": s[3]} for s in students])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch students from replica: {str(e)}"}), 500

@app.route('/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        conn = get_primary_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (имя, фамилия, группа) VALUES (%s, %s, %s) RETURNING id",
            (data['имя'], data['фамилия'], data['группа'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Student added"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add student: {str(e)}"}), 500

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        conn = get_primary_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        if cur.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"Student with ID {student_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete student: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)