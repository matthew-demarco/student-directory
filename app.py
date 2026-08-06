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

if __name__ == "__main__":
    app.run(debug=True)
