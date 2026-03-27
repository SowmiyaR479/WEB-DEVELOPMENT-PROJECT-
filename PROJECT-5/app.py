from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "mysecretkey"

db = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="root",   
    database="studentdb"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add_student():
    try:
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        gpa = request.form['gpa']

        if not name or not age or not email:
            flash("Name, Age, and Email are required!", "error")
            return redirect('/')

        age = int(age)
        gpa = float(gpa)

        query = """
            INSERT INTO students (name, age, gender, email, phone, department, gpa, admission_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
        """
        values = (name, age, gender, email, phone, department, gpa)
        cursor.execute(query, values)
        db.commit()

        flash("Student added successfully!", "success")
        return redirect('/students')

    except Exception as e:
        print("Error:", e)
        flash("Failed to add student!", "error")
        return redirect('/')


@app.route('/students')
def students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('students.html', students=data)


if __name__ == '__main__':
    app.run(debug=True)