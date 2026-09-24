from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("students.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)
    return conn

@app.route("/")
def home():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
        (request.form["name"], request.form["email"], request.form["course"])
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
