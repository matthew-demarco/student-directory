from flask import Flask, render_template, request, redirect
import psycopg

app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        dbname="practice",
        user="student_app",
        password="practice_password",
        host="localhost",
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
    name = request.form["name"]
    school = request.form["school"]

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
    return render_template("edit.html", student=student)

@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form["name"]
    school = request.form["school"]

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
	    "UPDATE students SET name = %s, school = %s WHERE id = %s",
	    (name, school, student_id),
	)
    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
