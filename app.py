import getpass
from datetime import date

import psycopg2

# The connection is opened once when the application starts.
connection = None


# Display all students currently in the database.
def getAllStudents():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students ORDER BY student_id;")
        students = cursor.fetchall()
        cursor.close()

        if not students:
            print("No students found.")
        else:
            print("\nID | Name | Email | Enrollment Date")
            for student in students:
                print(f"{student[0]} | {student[1]} {student[2]} | {student[3]} | {student[4]}")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error getting students:", error)


# Add a new student using the information entered by the user.
def addStudent(first_name, last_name, email, enrollment_date):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (first_name, last_name, email, enrollment_date) "
            "VALUES (%s, %s, %s, %s) RETURNING student_id;",
            (first_name, last_name, email, enrollment_date)
        )
        student_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        print(f"Student added with ID {student_id}.")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error adding student:", error)


# Change the email address of an existing student.
def updateStudentEmail(student_id, new_email):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET email = %s WHERE student_id = %s;",
            (new_email, student_id)
        )
        changed = cursor.rowcount
        connection.commit()
        cursor.close()

        if changed > 0:
            print("Student email updated.")
        else:
            print("No student found with that ID.")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error updating email:", error)


# Remove a student using their student ID.
def deleteStudent(student_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM students WHERE student_id = %s;",
            (student_id,)
        )
        deleted = cursor.rowcount
        connection.commit()
        cursor.close()

        if deleted > 0:
            print("Student deleted.")
        else:
            print("No student found with that ID.")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error deleting student:", error)


# Show the menu and call the correct function for each choice.
def main():
    global connection
    password = getpass.getpass("Enter your PostgreSQL password: ")

    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="students_db",
            user="postgres",
            password=password
        )
        print("Connected to the students_db database.")
    except psycopg2.Error as error:
        print("Could not connect to PostgreSQL:", error)
        return

    try:
        while True:
            print("\nStudent Management")
            print("1. View all students")
            print("2. Add a student")
            print("3. Update a student's email")
            print("4. Delete a student")
            print("5. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                getAllStudents()

            elif choice == "2":
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                email = input("Email: ").strip()
                date_text = input("Enrollment date (YYYY-MM-DD): ").strip()

                if not first_name or not last_name or not email:
                    print("First name, last name and email are required.")
                    continue

                try:
                    enrollment_date = date.fromisoformat(date_text) if date_text else None
                except ValueError:
                    print("Invalid date. Use YYYY-MM-DD.")
                    continue

                addStudent(first_name, last_name, email, enrollment_date)

            elif choice == "3":
                try:
                    student_id = int(input("Student ID: "))
                except ValueError:
                    print("Student ID must be a number.")
                    continue

                new_email = input("New email: ").strip()
                if not new_email:
                    print("Email cannot be empty.")
                    continue
                updateStudentEmail(student_id, new_email)

            elif choice == "4":
                try:
                    student_id = int(input("Student ID: "))
                except ValueError:
                    print("Student ID must be a number.")
                    continue
                deleteStudent(student_id)

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Enter a number from 1 to 5.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
