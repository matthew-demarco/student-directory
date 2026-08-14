import os
import pytest

os.environ["DB_NAME"] = "practice_test"

from app import app, get_connection


@pytest.fixture
def clean_test_student():
    yield

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM students WHERE name IN (%s, %s);",
            ("Test Student","Updated Student"),
        )

    connection.commit()
    connection.close()


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_missing_student_returns_404():
    client = app.test_client()

    response = client.get("/edit/99999")

    assert response.status_code == 404


def test_add_student_rejects_blank_name():
    client = app.test_client()

    response = client.post(
        "/add",
        data={
            "name": "   ",
            "school": "FSU",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Name and school are required." in response.data


def test_add_student_valid_input(clean_test_student):
    client = app.test_client()

    response = client.post(
        "/add",
        data={
            "name": "Test Student",
            "school": "Test School",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name, school FROM students WHERE name = %s;",
            ("Test Student",),
        )

        student = cursor.fetchone()

    connection.close()

    assert student is not None
    assert student[0] == "Test Student"
    assert student[1] == "Test School"
def test_update_student(clean_test_student):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO students (name, school) VALUES (%s, %s) RETURNING id;",
            ("Test Student", "Test School"),
        )
        student_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    client = app.test_client()

    response = client.post(
        f"/update/{student_id}",
        data={
            "name": "Updated Student",
            "school": "Updated School",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name, school FROM students WHERE id = %s;",
            (student_id,),
        )
        student = cursor.fetchone()

    connection.close()

    assert student[0] == "Updated Student"
    assert student[1] == "Updated School"

def test_delete_student(clean_test_student):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO students (name, school) VALUES (%s, %s) RETURNING id;",
            ("Test Student", "Test School"),
        )
        student_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    client = app.test_client()

    response = client.post(
        f"/delete/{student_id}",
        follow_redirects=False,
    )

    assert response.status_code == 302

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM students WHERE id = %s;",
            (student_id,),
        )
        student = cursor.fetchone()

    connection.close()

    assert student is None

def test_api_get_students():
    client = app.test_client()

    response = client.get("/api/students")

    assert response.status_code == 200
    assert response.is_json

def test_api_get_missing_student():
    client = app.test_client()

    response = client.get("/api/students/99999")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["error"] == "Student not found"
def test_api_get_student(clean_test_student):
    client = app.test_client()

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO students (name, school)
            VALUES (%s, %s)
            RETURNING id;
            """,
            ("Test Student", "Test School")
        )

        student_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    response = client.get(f"/api/students/{student_id}")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert data["id"] == student_id
    assert data["name"] == "Test Student"
    assert data["school"] == "Test School"
def test_api_add_student(clean_test_student):
    client = app.test_client()

    response = client.post(
        "/api/students",
        json={
            "name": "Test Student",
            "school": "Test School"
        }
    )

    assert response.status_code == 201
    assert response.is_json

    data = response.get_json()

    assert data["name"] == "Test Student"
    assert data["school"] == "Test School"

def test_api_update_student(clean_test_student):
    client = app.test_client()

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO students (name, school)
            VALUES (%s, %s)
            RETURNING id;
            """,
            ("Test Student", "Test School")
        )
        student_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    response = client.put(
        f"/api/students/{student_id}",
        json={
            "name": "Updated Student",
            "school": "Updated School"
        }
    )

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert data["name"] == "Updated Student"
    assert data["school"] == "Updated School"

def test_api_delete_student(clean_test_student):
    client = app.test_client()

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO students (name, school)
            VALUES (%s, %s)
            RETURNING id;
            """,
            ("Test Student", "Test School")
        )
        student_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    response = client.delete(f"/api/students/{student_id}")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert data["message"] == "Student deleted"
def test_api_add_student_rejects_blank_name():
    client = app.test_client()

    response = client.post(
        "/api/students",
        json={
            "name": "",
            "school": "Test School"
        }
    )

    assert response.status_code == 400
    assert response.is_json

    data = response.get_json()

    assert data["error"] == "Name and school are required."
