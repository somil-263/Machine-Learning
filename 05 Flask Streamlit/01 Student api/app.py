from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

students_data = [
    {
        'id' : 1,
        'name' : 'John Doe',
        'age' : 20,
        'major' : 'Computer Science'
    },
    {
        'id' : 2,
        'name' : 'Alice',
        'age' : 22,
        'major' : 'Mathematics'
    }
]

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def students():
    return jsonify(students_data)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data or data is None or data.get('name') is None:
        return jsonify({"error" : "Missing parameters name is required"}), 400
    
    name = data.get('name')
    age = data.get('age')
    major = data.get('major')

    new_student = {
        'id' : students_data[-1].get('id') + 1,
        'name' : name,
        'age' : age,
        'major' : major
    }

    students_data.append(new_student)

    return jsonify(new_student), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def find_user(student_id):
    student = next((student for student in students_data if student.get('id') == student_id), None)

    if student is None:
        return jsonify({"error" : "Student Not Found"}), 404
    
    return jsonify(student), 200

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = next((student for student in students_data if student.get('id') == id), None)

    if student is None:
        return jsonify({"error" : "Student Not Found"}), 404
    
    students_data.remove(student)

    return jsonify({"Success" : "Student removed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)