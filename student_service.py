import csv
import os


HEADERS = [
    "Student ID",
    "Name",
    "Total",
    "Percentage",
    "Grade"
]


def load_students(file_name):
    """Load student records from a CSV file."""

    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        return []

    with open(file_name, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_students(file_name, students):
    """Save all student records to a CSV file."""

    temp_file = file_name + ".tmp"

    with open(temp_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(students)

    os.replace(temp_file, file_name)


def generate_student_id(file_name):
    """Generate the next available student ID."""

    students = load_students(file_name)
    highest_id = 0

    for student in students:
        student_id = student.get("Student ID", "").strip()

        if student_id.startswith("STU"):
            try:
                number = int(student_id[3:])
                highest_id = max(highest_id, number)
            except ValueError:
                continue

    return f"STU{highest_id + 1:03d}"


def add_student(file_name, get_marks, calculate_grade):
    """Add a student with a unique ID."""

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    students = load_students(file_name)

    for student in students:
        if student["Name"].strip().casefold() == name.casefold():
            print("A student with this name already exists!")
            return

    marks = [
        get_marks("Subject 1"),
        get_marks("Subject 2"),
        get_marks("Subject 3")
    ]

    total = sum(marks)
    percentage = total / len(marks)
    grade = calculate_grade(percentage)
    student_id = generate_student_id(file_name)

    students.append({
        "Student ID": student_id,
        "Name": name,
        "Total": str(total),
        "Percentage": str(round(percentage, 2)),
        "Grade": grade
    })

    save_students(file_name, students)

    print("\nStudent added successfully!")
    print("Student ID:", student_id)
    print("Name:", name)
    print("Total:", total)
    print(f"Percentage: {percentage:.2f}%")
    print("Grade:", grade)


def delete_student(file_name):
    """Delete a student using Student ID."""

    student_id = input("Enter Student ID to delete: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    students = load_students(file_name)

    for student in students:
        if student.get("Student ID", "").casefold() == student_id.casefold():
            print("\nStudent found!")
            print("Student ID:", student["Student ID"])
            print("Name:", student["Name"])

            confirm = input(
                "Are you sure you want to delete this student? (yes/no): "
            ).strip().casefold()

            if confirm != "yes":
                print("Deletion cancelled.")
                return

            students.remove(student)
            save_students(file_name, students)

            print("Student deleted successfully!")
            return

    print("Student not found.")


def update_student(file_name, get_marks, calculate_grade):
    """Update a student's marks and calculated grade."""

    student_id = input("Enter Student ID to update: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    students = load_students(file_name)

    for student in students:
        if student.get("Student ID", "").casefold() == student_id.casefold():
            print("\nStudent found!")
            print("Name:", student["Name"])
            print("Current Total:", student["Total"])
            print("Current Grade:", student["Grade"])

            confirm = input(
                "Do you want to update marks? (yes/no): "
            ).strip().casefold()

            if confirm != "yes":
                print("Update cancelled.")
                return

            marks = [
                get_marks("Subject 1"),
                get_marks("Subject 2"),
                get_marks("Subject 3")
            ]

            total = sum(marks)
            percentage = total / len(marks)
            grade = calculate_grade(percentage)

            student["Total"] = str(total)
            student["Percentage"] = str(round(percentage, 2))
            student["Grade"] = grade

            save_students(file_name, students)

            print("Student record updated successfully!")
            print("New Total:", total)
            print(f"New Percentage: {percentage:.2f}%")
            print("New Grade:", grade)
            return

    print("Student not found.")


def sort_students(file_name):
    """Return students sorted from highest to lowest percentage."""

    students = load_students(file_name)

    return sorted(
        students,
        key=lambda student: float(student["Percentage"]),
        reverse=True
    )


def filter_students_by_grade(file_name, grade):
    """Return students matching a particular grade."""

    students = load_students(file_name)

    return [
        student for student in students
        if student["Grade"].strip().casefold() == grade.strip().casefold()
    ]


def get_statistics(file_name):
    """Calculate summary statistics for student records."""

    students = load_students(file_name)

    if not students:
        return {
            "total_students": 0,
            "average_percentage": 0,
            "highest_percentage": 0,
            "lowest_percentage": 0
        }

    percentages = [
        float(student["Percentage"])
        for student in students
    ]

    return {
        "total_students": len(students),
        "average_percentage": round(
            sum(percentages) / len(percentages), 2
        ),
        "highest_percentage": max(percentages),
        "lowest_percentage": min(percentages)
    }


def export_report(file_name, report_file="student_report.csv"):
    """Export student records to a separate CSV report."""

    students = load_students(file_name)

    if not students:
        print("No student records available to export.")
        return

    with open(
        report_file, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(students)

    print("Report exported successfully!")
    print("Report file:", os.path.abspath(report_file))