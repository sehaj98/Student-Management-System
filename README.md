# Student Management System

A Python-based Student Management System that helps manage student records, calculate grades, update student information, and generate reports using CSV file storage.

## Features

- Add new student records
- View all student records
- Search students
- Update student information
- Delete student records
- Sort students by percentage
- Filter students by grade
- View a statistics dashboard
- Export student reports
- Store records in a CSV file
- Automated testing with pytest

## Technologies Used

- Python
- CSV File Handling
- Pytest
- Git and GitHub

## Project Structure

```text
01_student_grade_calculator/
├── main.py
├── grades.py
├── student_service.py
├── students.csv
├── students.csv.bak
├── student_report.csv
├── test/
│   ├── test_grades.py
│   └── test_student_service.py
├── README.md
└── .gitignore
```

*Note: The files listed above should match the actual files in your project.*

## Requirements

- Python 3
- Pytest for running automated tests

## Installation

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Open the project folder:

   ```bash
   cd Student-Management-System
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Run Tests

Run the following command to execute the automated tests:

```bash
python -m pytest -v
```

## Data Storage

Student records are stored in a CSV file. The application supports adding, searching, updating, deleting, and viewing student records.

**Privacy note:** Do not upload real student personal information or confidential academic records to a public repository.

## Learning Outcomes

This project demonstrates practical knowledge of:

- Python functions and modules
- File handling with CSV
- CRUD operations
- Exception handling and input validation
- Automated testing using pytest
- Version control with Git and GitHub

## Future Improvements

- Add a graphical user interface
- Use SQLite for database storage
- Add login and authentication
- Improve input validation
- Generate advanced student performance reports

## Author

**Sehajdeep Kaur**

MCA Student | Aspiring Python Developer