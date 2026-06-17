import sqlite3

def search_feature(cursor, term=None, return_data=False):
    if term is None:
        term = input("\nEnter Student Name or ID to search: ").strip()

    query = "SELECT * FROM students WHERE ID = ? OR first_name LIKE ? OR last_name LIKE ?"
    search_pattern = f"%{term}%"

    if term.isdigit():
        cursor.execute(query, (int(term), search_pattern, search_pattern))
    else:
        cursor.execute(query, (-1, search_pattern, search_pattern))

    results = cursor.fetchall()

    if return_data:
        return results

    if not results:
        print(f"\nNo student records found matching '{term}'.")
    else:
        print("\nMatch(es) found!")
        for row in results:
            f_name, l_name, s_id, crs, grd = row
            print(f"ID: {s_id} | Name: {f_name} {l_name} | Course: {crs} | Grade: {grd}")


def delete_feature(conn, cursor, target_id=None, confirm_delete=True):
    if target_id is None:
        target_id = input("\nEnter Student ID to delete: ").strip()

    if not str(target_id).isdigit():
        return False

    cursor.execute("SELECT * FROM students WHERE ID = ?", (target_id,))
    student = cursor.fetchone()

    if not student:
        return False

    f_name, l_name, s_id, crs, grd = student

    if confirm_delete:
        confirm = input(f"Are you sure you want to delete {f_name} {l_name}? (yes/no): ").strip().lower()
        if confirm != "yes":
            return False

    cursor.execute("DELETE FROM students WHERE ID = ?", (target_id,))
    conn.commit()
    return True


def update_feature(conn, cursor, target_id=None, new_data=None):
    if target_id is None:
        target_id = input("\nEnter Student ID to update: ").strip()

    if not str(target_id).isdigit():
        return False

    cursor.execute("SELECT * FROM students WHERE ID = ?", (target_id,))
    student = cursor.fetchone()

    if not student:
        return False

    f_name, l_name, s_id, crs, grd = student

    if new_data:
        new_first, new_last, new_course, new_grade = new_data
    else:
        new_first = input(f"Enter new first name ({f_name}): ").strip() or f_name
        new_last = input(f"Enter new last name ({l_name}): ").strip() or l_name
        new_course = input(f"Enter new course ({crs}): ").strip() or crs
        new_grade = input(f"Enter new grade ({grd}): ").strip() or grd

    cursor.execute("""
        UPDATE students
        SET first_name = ?, last_name = ?, course = ?, grade = ?
        WHERE ID = ?
    """, (new_first, new_last, new_course, new_grade, target_id))

    conn.commit()
    return True


def create_database():
    conn = sqlite3.connect("Student_Records.db")
    cursor = conn.cursor()
    return conn, cursor


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        first_name TEXT,
        last_name TEXT,
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        grade TEXT 
    )
    """)


def insert_students(cursor, first_name, last_name, course, grade):
    cursor.execute(
        "INSERT INTO students (first_name, last_name, course, grade) VALUES (?, ?, ?, ?)",
        (first_name, last_name, course, grade)
    )


def view_students(cursor, return_data=False):
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if return_data:
        return records

    print("\nStudent Records:")
    if not records:
        print("[Database is currently empty]")
        return

    for row in records:
        f_name, l_name, s_id, crs, grd = row
        print(f"ID: {s_id} | Name: {f_name} {l_name} | Course: {crs} | Grade: {grd}")


def mainProgram():
    conn, cursor = create_database()
    create_table(cursor)

    while True:
        print("\n=== STUDENT RECORDS ===")
        print("1. Add new student")
        print("2. View all students")
        print("3. Search for a student")
        print("4. Update a student")
        print("5. Delete a student")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            course = input("Enter course: ")
            grade = input("Enter grade: ")

            insert_students(cursor, first_name, last_name, course, grade)
            conn.commit()

        elif choice == "2":
            view_students(cursor)

        elif choice == "3":
            search_feature(cursor)

        elif choice == "4":
            update_feature(conn, cursor)

        elif choice == "5":
            delete_feature(conn, cursor)

        elif choice == "6":
            break

    conn.close()


if __name__ == "__main__":
    mainProgram()