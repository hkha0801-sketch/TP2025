from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_students():
    try:
        data = request.get_json()
        
        if not data or 'students' not in data or not isinstance(data['students'], list):
            return jsonify({
                "status": "error",
                "message": "Dữ liệu không hợp lệ. Cần có danh sách 'students'."
            }), 400

        raw_students = data['students']
        total_students = len(raw_students)
        
        seen_ids = set()
        duplicate_students = []
        unique_eligible_students = []

        for student in raw_students:
            required_fields = ['student_id', 'name', 'age', 'gender']
            if not all(field in student for field in required_fields):
                return jsonify({
                    "status": "error", 
                    "message": "Dữ liệu thiếu trường thông tin bắt buộc."
                }), 400

            s_id = student['student_id']
            age = student['age']


            if s_id in seen_ids:
                duplicate_students.append(student)
            else:
                seen_ids.add(s_id)
                if age < 23:
                    unique_eligible_students.append(student)

        return jsonify({
            "status": "success",
            "message": "Danh sách đã được xử lý thành công.",
            "total_students": total_students,
            "duplicate_students": duplicate_students,
            "students_eligible_for_free_ticket": unique_eligible_students
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Đã có lỗi xảy ra: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)