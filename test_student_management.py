#Ensures that the test file can access the student_management_4.py file in the same directory
import os
import sys
import sqlite3
import pytest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from student_management import Update_feature, Delete_Feature, create_table, insert_studentrecords


@pytest.fixture
#Tests database setup and returns a connection and cursor for use in tests
def setup_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    create_table(cursor)
    insert_studentrecords(cursor, "John", "Doe", "Python 101", "A")
    conn.commit()
    return conn, cursor

#Makes sure that update student function works 
def test_update_student_works(setup_db):
    conn, cursor = setup_db
    result = Update_feature(conn, cursor, target_id="1", new_data=("John", "Doe", "Python 102", "A+"))
    
    assert result == True
    
    cursor.execute("SELECT course, grade FROM students WHERE ID = 1")
    row = cursor.fetchone()
    assert row[0] == "Python 102"
    assert row[1] == "A+"

#tests the delete student function
def test_delete_student_works(setup_db):
    conn, cursor = setup_db
    result = Delete_Feature(conn, cursor, target_id="1", confirm_delete=False)
    
    assert result == True
    
    cursor.execute("SELECT * FROM students WHERE ID = 1")
    row = cursor.fetchone()
    assert row == None

#tests the update student function when the student is not found
def test_update_student_not_found(setup_db):
    conn, cursor = setup_db
    result = Update_feature(conn, cursor, target_id="999", new_data=("Fake", "Name", "Class", "F"))
    assert result == False