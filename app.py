from flask import Flask, render_template, request, redirect, flash
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
    )


@app.route("/")
def home():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, school FROM students ORDER BY id;"
        )
        students = cursor.fetchall()

    connection.close()

    return render_template("home.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"].strip()
    school = request.form["school"].strip()

    if not name or not school:
        flash("Name and school are required.")
        return redirect("/")

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
	    "INSERT INTO students (name, school) VALUES (%s, %s);",
	    (name, school),

	)
    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
	    "DELETE FROM students WHERE id = %s;",
	    (student_id,),
	)

        if cursor.rowcount == 0:
            connection.close()
            return "Student not found.", 404

    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
	    "SELECT id, name, school FROM students WHERE id = %s;",
	    (student_id,),

        )
        student = cursor.fetchone()

        connection.close()

        if student is None:
            return "Student not found.", 404

    return render_template("edit.html", student=student)

@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form["name"].strip()
    school = request.form["school"].strip()

    if not name or not school:
        flash("Name and school are required.")
        return redirect(f"/edit/{student_id}")

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
	    "UPDATE students SET name = %s, school = %s WHERE id = %s",
	    (name, school, student_id),
	)

    if cursor.rowcount == 0:
        connection.close()
        return "Student not found.", 404

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
