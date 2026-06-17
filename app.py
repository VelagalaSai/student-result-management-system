from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
import io

app = Flask(__name__)
def get_db():
    conn = sqlite3.connect('srms.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_number TEXT UNIQUE NOT NULL,
        branch TEXT NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT UNIQUE NOT NULL,
        subject_name TEXT NOT NULL,
        branch TEXT NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        marks INTEGER,
        grade TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )''')
    conn.commit()
    conn.close()

def calculate_grade(marks):
    if marks >= 90: return 'O'
    elif marks >= 80: return 'A+'
    elif marks >= 70: return 'A'
    elif marks >= 60: return 'B+'
    elif marks >= 50: return 'B'
    elif marks >= 40: return 'C'
    else: return 'F'

def calculate_cgpa(grade):
    grade_points = {'O':10,'A+':9,'A':8,'B+':7,'B':6,'C':5,'F':0}
    return grade_points.get(grade, 0)

@app.route('/')
def index():
    conn = get_db()
    student_count = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    subject_count = conn.execute('SELECT COUNT(*) FROM subjects').fetchone()[0]
    result_count = conn.execute('SELECT COUNT(*) FROM results').fetchone()[0]
    conn.close()
    return render_template('index.html', student_count=student_count,
                           subject_count=subject_count, result_count=result_count)

@app.route('/students')
def students():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll_number']
        branch = request.form['branch']
        conn = get_db()
        conn.execute('INSERT INTO students (name, roll_number, branch) VALUES (?,?,?)',
                     (name, roll, branch))
        conn.commit()
        conn.close()
        return redirect(url_for('students'))
    return render_template('student_form.html')

@app.route('/subjects')
def subjects():
    conn = get_db()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    conn.close()
    return render_template('subjects.html', subjects=subjects)

@app.route('/subjects/add', methods=['GET','POST'])
def add_subject():
    if request.method == 'POST':
        code = request.form['subject_code']
        name = request.form['subject_name']
        branch = request.form['branch']
        conn = get_db()
        conn.execute('INSERT INTO subjects (subject_code, subject_name, branch) VALUES (?,?,?)',
                     (code, name, branch))
        conn.commit()
        conn.close()
        return redirect(url_for('subjects'))
    return render_template('subject_form.html')

@app.route('/results')
def results():
    conn = get_db()
    results = conn.execute('''
        SELECT s.name, s.roll_number, sub.subject_name, r.marks, r.grade
        FROM results r
        JOIN students s ON r.student_id = s.id
        JOIN subjects sub ON r.subject_id = sub.id
    ''').fetchall()
    conn.close()
    return render_template('results.html', results=results)

@app.route('/results/add', methods=['GET','POST'])
def add_result():
    conn = get_db()
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        marks = int(request.form['marks'])
        grade = calculate_grade(marks)
        conn.execute('INSERT INTO results (student_id, subject_id, marks, grade) VALUES (?,?,?,?)',
                     (student_id, subject_id, marks, grade))
        conn.commit()
        conn.close()
        return redirect(url_for('results'))
    students = conn.execute('SELECT * FROM students').fetchall()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    conn.close()
    return render_template('result_form.html', students=students, subjects=subjects)

@app.route('/reports')
def reports():
    conn = get_db()
    data = conn.execute('''
        SELECT s.name, s.roll_number, s.branch,
               COUNT(r.id) as total_subjects,
               AVG(r.marks) as avg_marks,
               GROUP_CONCAT(r.grade) as grades
        FROM students s
        LEFT JOIN results r ON s.id = r.student_id
        GROUP BY s.id
    ''').fetchall()
    conn.close()
    return render_template('reports.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
