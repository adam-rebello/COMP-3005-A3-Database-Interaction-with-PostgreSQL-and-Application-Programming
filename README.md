# COMP 3005 - Assignment 3: Student Management Adam Rebello 

This is a Python application connected to a PostgreSQL database. It lets the user view, add, update and delete student records from the `students` table.

## Requirements

- Python 3.10 or newer
- PostgreSQL and pgAdmin 4
- The `psycopg2-binary` Python package (see `requirements.txt`)

## Database setup

1. Open pgAdmin 4 and connect to your local PostgreSQL server.
2. Right-click **Databases** and choose **Create > Database**.
3. Name the database `students_db` and save it.
4. Select `students_db`, then open **Tools > Query Tool**.
5. Open the file `database/setup.sql` using the folder icon in Query Tool.
6. Click **Execute** to create the `students` table and insert the three starting students.
7. To check the data, run:

   ```sql
   SELECT * FROM students ORDER BY student_id;
   ```

Run `setup.sql` only once on a new database. The table has an auto-incrementing primary key, required names and email, and a unique email constraint.

## Running the application

Open a terminal inside this project folder and run:

```powershell
py -m pip install -r requirements.txt
py app.py
```

The app assumes PostgreSQL runs on `localhost`, port `5432`, and the database is named `students_db`. Change these values in `app.py` if your setup is different.

## Application functions

- `getAllStudents()` shows all student records.
- `addStudent(first_name, last_name, email, enrollment_date)` inserts a student.
- `updateStudentEmail(student_id, new_email)` changes a student's email.
- `deleteStudent(student_id)` removes a student.

The menu allows you to call each function. For dates, enter `YYYY-MM-DD`; leave the date blank if it is unknown. Changes are committed so they appear in pgAdmin.

## Video demonstration

**Video link:** https://drive.google.com/file/d/192mb5r_e93L3ejg7J-Wzcttge_sI60z0/view?usp=drive_link

```sql
SELECT * FROM students ORDER BY student_id;
```

## Project files

- `app.py`: Python application and menu
- `database/setup.sql`: Table creation and initial data
- `requirements.txt`: Python dependency
- `README.md`: Setup and running instructions
