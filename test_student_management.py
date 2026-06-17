import sqlite3

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            course TEXT,
            grade TEXT
        )
    """)

def insert_students(cursor, first_name, last_name, course, grade):
    cursor.execute("""
        INSERT INTO students (first_name, last_name, course, grade)
        VALUES (?, ?, ?, ?)
    """, (first_name, last_name, course, grade))

# ONLY parameter names changed here
def update_feature(conn, cursor, target_id, new_data):
    cursor.execute("SELECT * FROM students WHERE ID = ?", (target_id,))
    if cursor.fetchone() is None:
        return False

    cursor.execute("""
        UPDATE students
        SET first_name = ?, last_name = ?, course = ?, grade = ?
        WHERE ID = ?
    """, (*new_data, target_id))

    conn.commit()
    return True

# ONLY parameter names changed here
def delete_feature(conn, cursor, target_id, confirm_delete):
    cursor.execute("SELECT * FROM students WHERE ID = ?", (target_id,))
    if cursor.fetchone() is None:
        return False

    cursor.execute("DELETE FROM students WHERE ID = ?", (target_id,))
    conn.commit()
    return True