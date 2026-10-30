#==================================================
#        STUDENT MANAGEMENT SYSTEM
#==================================================
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")
conn.commit()

print("Database connected successfully!")

courses = ["ai", "ds", "da", "java", "full stack"]

while True:
    print("------------------------------------------------------")
    print("Student Management System")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Count Students")
    print("7. Filter Students by Course")
    print("8. Sort Students by Name")
    print("9. Display Age Statistics")
    print("10. Display Course Statistics")
    print("11. Save Student Data")
    print("12. Exit")
    print("-----------------------------------------------------")

    choice = input("Enter your choice: ")
    if not choice.isdigit():
        print("Please enter a number.")
        continue
    choice = int(choice)

    # ===================== 1. Add Student =====================
    if choice == 1:
        name = input("Enter student name: ")
        if len(name) < 2:
            print("Invalid name")
            continue

        age = input("Enter student age: ")
        if not age.isdigit():
            print("Age must be a number.")
            continue
        age = int(age)
        if age < 18:
            print("Student must be at least 18 years old.")
            continue
        if age > 30:
            print("Student must be at most 30 years old.")
            continue

        print("We have courses like")
        for i in range(len(courses)):
            print(i + 1, ":", courses[i])
        course = input("Enter student course: ").lower()
        if course not in courses:
            print("Invalid course. Please select from the available courses.")
            continue

        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                       (name, age, course))
        conn.commit()
        print("Student added successfully!")

    # ===================== 2. View Students =====================
    elif choice == 2:
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        if len(records) == 0:
            print("No students found.")
        else:
            for student in records:
                print("___________________________________________________________")
                print("Student ID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Course:", student[3])
                print("___________________________________________________________")

    # ===================== 3. Search Student =====================
    elif choice == 3:
        search_name = input("Enter student name to search: ")

        cursor.execute("SELECT * FROM students WHERE name LIKE ?",
                       ("%" + search_name + "%",))
        records = cursor.fetchall()

        if len(records) == 0:
            print("Student not found.")
        else:
            print("Student Found!")
            for student in records:
                print("________________________________________")
                print("Student ID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Course:", student[3])
                print("________________________________________")

    # ===================== 4. Update Student =====================
    elif choice == 4:
        student_id = input("Enter the ID of the student to update: ")
        if not student_id.isdigit():
            print("ID must be a number.")
            continue

        cursor.execute("SELECT * FROM students WHERE id = ?", (int(student_id),))
        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
        else:
            print("Current details -> Name:", student[1], "| Age:", student[2], "| Course:", student[3])

            new_name = input("Enter new name: ")
            if len(new_name) < 2:
                print("Invalid name")
                continue

            new_age = input("Enter new age: ")
            if not new_age.isdigit():
                print("Age must be a number.")
                continue
            new_age = int(new_age)
            if new_age < 18 or new_age > 30:
                print("Age must be between 18 and 30.")
                continue

            print("Available courses:", courses)
            new_course = input("Enter new course: ").lower()
            if new_course not in courses:
                print("Invalid course.")
                continue

            cursor.execute("UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
                           (new_name, new_age, new_course, int(student_id)))
            conn.commit()
            print("Student updated successfully!")

    # ===================== 5. Delete Student =====================
    elif choice == 5:
        student_id = input("Enter the ID of the student to delete: ")
        if not student_id.isdigit():
            print("ID must be a number.")
            continue

        cursor.execute("SELECT * FROM students WHERE id = ?", (int(student_id),))
        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
        else:
            print("You are about to delete:", student[1], "| Age:", student[2], "| Course:", student[3])
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == "yes":
                cursor.execute("DELETE FROM students WHERE id = ?", (int(student_id),))
                conn.commit()
                print("Student deleted successfully!")
            else:
                print("Delete cancelled.")

    # ===================== 6. Count Students =====================
    elif choice == 6:
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]
        print("Total number of students:", total)

    # ===================== 7. Filter Students by Course =====================
    elif choice == 7:
        print("Available courses:", courses)
        course = input("Enter course to filter: ").lower()
        if course not in courses:
            print("Invalid course.")
            continue

        cursor.execute("SELECT * FROM students WHERE course = ?", (course,))
        records = cursor.fetchall()

        if len(records) == 0:
            print("No students found in this course.")
        else:
            print("Students in", course, ":")
            for student in records:
                print("___________________________________________________________")
                print("Student ID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Course:", student[3])
                print("___________________________________________________________")

    # ===================== 8. Sort Students by Name =====================
    elif choice == 8:
        cursor.execute("SELECT * FROM students ORDER BY name COLLATE NOCASE")
        records = cursor.fetchall()

        if len(records) == 0:
            print("No students found.")
        else:
            for student in records:
                print("___________________________________________________________")
                print("Student ID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Course:", student[3])
                print("___________________________________________________________")

    # ===================== 9. Age Statistics =====================
    elif choice == 9:
        cursor.execute("SELECT MIN(age), MAX(age), AVG(age) FROM students")
        stats = cursor.fetchone()

        if stats[0] is None:
            print("No students found.")
        else:
            print("Youngest student age:", stats[0])
            print("Oldest student age:", stats[1])
            print("Average age:", round(stats[2], 2))

    # ===================== 10. Course Statistics =====================
    elif choice == 10:
        cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course")
        records = cursor.fetchall()

        if len(records) == 0:
            print("No students found.")
        else:
            print("Students per course:")
            for row in records:
                print(row[0], ":", row[1])

    # ===================== 11. Save Student Data =====================
    elif choice == 11:
        # Data is already stored in the database after every change.
        # This option also saves a readable copy in a text file.
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        file = open("students.txt", "w")
        file.write("ID,Name,Age,Course\n")
        for student in records:
            file.write(str(student[0]) + "," + student[1] + "," + str(student[2]) + "," + student[3] + "\n")
        file.close()

        print("Student data saved to students.txt")

    # ===================== 12. Exit =====================
    elif choice == 12:
        conn.close()
        print("Exiting the program...")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 12.")

    input("\nPress Enter to return to the menu...")