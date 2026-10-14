import csv
import os
import shutil

from grades import calculate_grade
from student_service import (
    add_student as service_add_student,
    load_students,
    delete_student,
    update_student,
    sort_students,
    filter_students_by_grade,
    get_statistics,
    export_report
)


FILE_NAME = "students.csv"

HEADERS = [
    "Student ID",
    "Name",
    "Total",
    "Percentage",
    "Grade"
]


def setup_file():
    """Create the CSV file or migrate the old format."""

    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        return

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        old_headers = next(reader, [])

    if old_headers == HEADERS:
        return

    old_headers_without_id = [
        "Name", "Total", "Percentage", "Grade"
    ]

    if old_headers == old_headers_without_id:
        backup_file = FILE_NAME + ".bak"
        shutil.copy2(FILE_NAME, backup_file)

        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            old_students = list(csv.DictReader(file))

        migrated_students = []

        for number, student in enumerate(old_students, start=1):
            migrated_students.append({
                "Student ID": f"STU{number:03d}",
                "Name": student["Name"],
                "Total": student["Total"],
                "Percentage": student["Percentage"],
                "Grade": student["Grade"]
            })

        temp_file = FILE_NAME + ".tmp"

        with open(temp_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(migrated_students)

        os.replace(temp_file, FILE_NAME)

        print("CSV file updated successfully.")
        print(f"Backup saved as {backup_file}")
        return

    raise ValueError(
        "Unexpected CSV headers. Please check students.csv."
    )


def get_marks(subject):
    """Get valid marks between 0 and 100."""

    while True:
        try:
            marks = float(input(f"Enter {subject} marks (0-100): "))

            if 0 <= marks <= 100:
                return marks

            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def add_student():
    service_add_student(FILE_NAME, get_marks, calculate_grade)


def view_students():
    """Display all student records."""

    students = load_students(FILE_NAME)

    if not students:
        print("No student records found.")
        return

    print("\n--- All Student Records ---")

    for student in students:
        print(
            f'ID: {student["Student ID"]} | '
            f'Name: {student["Name"]} | '
            f'Total: {student["Total"]} | '
            f'Percentage: {student["Percentage"]}% | '
            f'Grade: {student["Grade"]}'
        )


def search_student():
    """Search by Student ID or name."""

    search_value = input(
        "Enter Student ID or student name to search: "
    ).strip()

    if not search_value:
        print("Please enter a Student ID or name.")
        return

    students = load_students(FILE_NAME)

    for student in students:
        student_id = student.get("Student ID", "").strip()
        student_name = student["Name"].strip()

        if (
            student_id.casefold() == search_value.casefold()
            or student_name.casefold() == search_value.casefold()
        ):
            print("\nStudent found!")

            for key in HEADERS:
                print(f"{key}: {student[key]}")

            return

    print("Student not found.")


def show_sorted_students():
    """Display students ranked by percentage."""

    students = sort_students(FILE_NAME)

    if not students:
        print("No student records found.")
        return

    print("\n--- Student Ranking ---")

    for rank, student in enumerate(students, start=1):
        print(
            f'{rank}. {student["Name"]} | '
            f'ID: {student["Student ID"]} | '
            f'Percentage: {student["Percentage"]}% | '
            f'Grade: {student["Grade"]}'
        )


def show_grade_filter():
    """Display students belonging to a particular grade."""

    grade = input("Enter grade to filter (e.g. A, B, A+): ").strip()

    if not grade:
        print("Grade cannot be empty.")
        return

    students = filter_students_by_grade(FILE_NAME, grade)

    if not students:
        print(f"No students found with grade {grade}.")
        return

    print(f"\n--- Students with Grade {grade} ---")

    for student in students:
        print(
            f'{student["Student ID"]} | '
            f'{student["Name"]} | '
            f'{student["Percentage"]}% | '
            f'{student["Grade"]}'
        )


def show_dashboard():
    """Display summary statistics."""

    stats = get_statistics(FILE_NAME)

    print("\n===== STUDENT STATISTICS DASHBOARD =====")
    print("Total Students:", stats["total_students"])
    print(f'Average Percentage: {stats["average_percentage"]}%')
    print(f'Highest Percentage: {stats["highest_percentage"]}%')
    print(f'Lowest Percentage: {stats["lowest_percentage"]}%')


def main():
    """Run the Student Management System."""

    setup_file()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Update Student Marks")
        print("6. Sort Students by Percentage")
        print("7. Filter Students by Grade")
        print("8. Statistics Dashboard")
        print("9. Export Student Report")
        print("10. Exit")

        choice = input("Choose an option (1-10): ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student(FILE_NAME)

        elif choice == "5":
            update_student(
                FILE_NAME,
                get_marks,
                calculate_grade
            )

        elif choice == "6":
            show_sorted_students()

        elif choice == "7":
            show_grade_filter()

        elif choice == "8":
            show_dashboard()

        elif choice == "9":
            export_report(FILE_NAME)

        elif choice == "10":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please select 1-10.")


if __name__ == "__main__":
    main()