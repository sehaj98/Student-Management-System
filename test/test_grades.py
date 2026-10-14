
from main import calculate_grade


def test_grade_a_plus():
    assert calculate_grade(95) == "A+"


def test_grade_a():
    assert calculate_grade(85) == "A"


def test_grade_b():
    assert calculate_grade(75) == "B"


def test_grade_c():
    assert calculate_grade(65) == "C"


def test_grade_d():
    assert calculate_grade(45) == "D"


def test_grade_fail():
    assert calculate_grade(30) == "F"


def test_grade_boundary_90():
    assert calculate_grade(90) == "A+"


def test_grade_boundary_40():
    assert calculate_grade(40) == "D"


from unittest.mock import patch
from main import get_marks


def test_get_marks_valid_input():
    with patch("builtins.input", return_value="85"):
        assert get_marks("Math") == 85.0


def test_get_marks_rejects_negative_marks():
    with patch("builtins.input", side_effect=["-5", "50"]):
        assert get_marks("Math") == 50.0


def test_get_marks_rejects_marks_above_100():
    with patch("builtins.input", side_effect=["120", "80"]):
        assert get_marks("Math") == 80.0


def test_get_marks_rejects_text_input():
    with patch("builtins.input", side_effect=["abc", "75"]):
        assert get_marks("Math") == 75.0


import csv
import main


def test_setup_file_creates_csv_header(tmp_path, monkeypatch):
    csv_file = tmp_path / "students.csv"
    monkeypatch.setattr(main, "FILE_NAME", str(csv_file))

    main.setup_file()

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        assert next(reader) == [
    "Student ID", "Name", "Total", "Percentage", "Grade"
]

def test_add_student_saves_record(tmp_path, monkeypatch):
    csv_file = tmp_path / "students.csv"
    monkeypatch.setattr(main, "FILE_NAME", str(csv_file))
    main.setup_file()

    inputs = iter(["Sehaj", "90", "98", "97"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    main.add_student()

    with open(csv_file, newline="", encoding="utf-8") as file:
        students = list(csv.DictReader(file))

    assert len(students) == 1
    assert students[0]["Name"] == "Sehaj"
    assert students[0]["Total"] == "285.0"
    assert students[0]["Percentage"] == "95.0"
    assert students[0]["Grade"] == "A+"


def test_add_student_preserves_existing_records(tmp_path, monkeypatch):
    csv_file = tmp_path / "students.csv"
    monkeypatch.setattr(main, "FILE_NAME", str(csv_file))
    main.setup_file()

    inputs = iter([
        "Sehaj", "90", "98", "97",
        "Aman", "89", "87", "88"
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    main.add_student()
    main.add_student()

    with open(csv_file, newline="", encoding="utf-8") as file:
        students = list(csv.DictReader(file))

    assert len(students) == 2
    assert students[0]["Name"] == "Sehaj"
    assert students[1]["Name"] == "Aman"
