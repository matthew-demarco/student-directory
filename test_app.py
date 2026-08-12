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
