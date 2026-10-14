import csv
from unittest.mock import patch

from student_service import (
    delete_student,
    update_student,
    sort_students,
    filter_students_by_grade,
    get_statistics,
    export_report
)


HEADERS = [
    "Student ID",
    "Name",
    "Total",
    "Percentage",
    "Grade"
]


def create_test_csv(file_name):
    students = [
        {
            "Student ID": "STU001",
            "Name": "Aman",
            "Total": "240",
            "Percentage": "80.0",
            "Grade": "A"
        },
        {
            "Student ID": "STU002",
            "Name": "Simran",
            "Total": "270",
            "Percentage": "90.0",
            "Grade": "A+"
        }
    ]

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(students)


def read_students(file_name):
    with open(file_name, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def test_delete_student_success(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    with patch("builtins.input", side_effect=["STU001", "yes"]):
        delete_student(file_name)

    students = read_students(file_name)

    assert len(students) == 1
    assert students[0]["Student ID"] == "STU002"


def test_delete_student_cancelled(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    with patch("builtins.input", side_effect=["STU001", "no"]):
        delete_student(file_name)

    assert len(read_students(file_name)) == 2


def test_delete_student_not_found(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    with patch("builtins.input", return_value="STU999"):
        delete_student(file_name)

    assert len(read_students(file_name)) == 2


def test_update_student_success(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    marks = iter([100, 90, 80])

    def fake_get_marks(subject):
        return next(marks)

    def fake_calculate_grade(percentage):
        return "A+" if percentage >= 90 else "A"

    with patch("builtins.input", side_effect=["STU001", "yes"]):
        update_student(file_name, fake_get_marks, fake_calculate_grade)

    students = read_students(file_name)
    updated = students[0]

    assert updated["Total"] == "270"
    assert updated["Percentage"] == "90.0"
    assert updated["Grade"] == "A+"


def test_sort_students(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    students = sort_students(file_name)

    assert students[0]["Name"] == "Simran"
    assert students[1]["Name"] == "Aman"


def test_filter_students_by_grade(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    students = filter_students_by_grade(file_name, "a+")

    assert len(students) == 1
    assert students[0]["Name"] == "Simran"


def test_get_statistics(tmp_path):
    file_name = str(tmp_path / "students.csv")
    create_test_csv(file_name)

    stats = get_statistics(file_name)

    assert stats["total_students"] == 2
    assert stats["average_percentage"] == 85
    assert stats["highest_percentage"] == 90
    assert stats["lowest_percentage"] == 80


def test_get_statistics_empty_file(tmp_path):
    file_name = str(tmp_path / "students.csv")

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()

    stats = get_statistics(file_name)

    assert stats["total_students"] == 0
    assert stats["average_percentage"] == 0


def test_export_report(tmp_path):
    file_name = str(tmp_path / "students.csv")
    report_file = str(tmp_path / "student_report.csv")
    create_test_csv(file_name)

    export_report(file_name, report_file)

    report = read_students(report_file)

    assert len(report) == 2
    assert report[0]["Name"] == "Aman"