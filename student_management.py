#Student management system 
import sqlite3

def Search_Feature():
        #this connects to the database
        conn = sqlite3.connect("Student_Records.db")
        cursor = conn.cursor()

        #gets the search term from the user
        term = input("\nEnter Student Name or ID to search:").strip()

        query = "SELECT * FROM students WHERE id = ? OR name LIKE ?"
        search_pattern = f"%{term}%"

        #We pass the search terms as a tuple to match the two '?' placeholders
        cursor.execute(query, (term, search_pattern))

        results = cursor.fetchall()
        #helps with error handling
        if not results:
            print(f"\n No student records found matching '{term}'.")
        else:
            print("\n Match is found !")
            #This loops through the results (in case multiple names end up matching)

            for row in results: 
            #this unpacks the tuple data type into clear variables
                student_id, name, course, grades = row
                print(f"ID:{student_id} | Name {first_name} {last_name} | Course: {course} | Grade: {grade}")
        #Closing the connection when done reading
        conn.close()

def Delete_Feature():
    #the conn is there to connect the database
    conn = sqlite3.connect("Student_Records.db")
    cursor = conn.cursor()
    target_ID = input("\nEnter Student name or ID to delete:").strip()

    check_query = "DELETE FROM students WHERE id = ?"
    cursor.execute(check_query, (target_ID))
    #we only need to provide one match
    student = cursor.fetchone() 

    #The safety check is there to check whether the student actually exists
    #Its the safest to delete by ID because IDs are very uniue to each student
    if not student:
        print(f"\n Error: No student found with ID {target_ID}.")
    else:
        #this will unoack the found record to show the user who they are deleting
        student_id, name, course, grade = student 
        print(f"\n Record Found: {first_name} {last_name}| (Course: {course})")

        #The confirmation will double check with the user before wiping data
        confirm = input(f"Are you sure you want to permanently delete the {first_name} {last_name}? (yes/no):").strip().lower()
        if confirm == "yes":

            #the 'DELETE' is to run the deletion query
            delete_query = "DELETE FROM student WHERE ID = ?"

            cursor.execute(delete_query, (target_ID,))

            #The commit is there to premanently save the changes to the datavase file
            conn.commit()

            print(f"\n Sucess: Student record for '{first_name}{last_name}' has been deleted.")
        else: 
            print("\n Deletion cancelled. Record was not changed.")

    # always close the connection so no errors are involved
    conn.close()


    
# Creates the database to store student records and also creates cursor to execute SQL commands
def create_database():
    connect = sqlite3.connect("Student_Records.db")  # Creates/connects to database file
    cursor = connect.cursor()  # Allows execution of SQL commands
    return connect, cursor

# Creates the table of student records
def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (   -- prevents error if table already exists
        first_name TEXT,
        last_name TEXT,
        ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-generates unique ID
        course TEXT,
        grade TEXT 
        )
    """)

# Inserts a student record into the table
def insert_studentrecords(cursor, first_name, last_name, course, grade):
    cursor.execute(
        "INSERT INTO students (first_name, last_name, course, grade) VALUES (?, ?, ?, ?)",
        (first_name, last_name, course, grade)
    )

# Displays all records in the table
def view_students(cursor):
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()  # Gets all rows
    
    print("\nStudent Records:")
    if not records: 
        print("[Database is currently empty]")
    for row in records:
        f_name, l_name, s_id, crs, grd = row
        print(f"ID: {s_id} | Name: {f_name} {l_name} | COurse: {crs} | Grade: {grd}")
def mainProgram():
    #this is the main User interface
    
    connect, cursor = create_database()
    create_table(cursor)

    while True: 
        print("\n === STUDENT RECORDS ===")
        print("1. Add new student records")
        print("2. View all student records")
        print("3. Search for a student")
        print("4. Update a student's information")
        print("5. Delete a student record")
        print("6. Exit")

        choice = input("please enter your choice (1-6)").strip()

        if choice == "1" :
            # Step 3: get user input
            print("\n--- Add New Student ---")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            course = input("Enter course: ")
            grade = input("Enter grade: ")

        elif choice == "2": 
            #calls for all student records here
            view_students(cursor)

        elif choice == "3":
            Search_Feature()
            #calls the student search function
            
        elif choice == "4":
            #calls the student function here
            print("Opening student's information...")
        
        elif choice == "5":
            Delete_Feature()
            #calls the delete function here
        
        elif choice == "6":
            print("Goodbye ! :)")
            break #will stop the while loop ande exits the program

        else: 
            print("Choice is invalid please retry. :(")
            #it will validate code and make sure the user puts the correct code

    
    # Step 3: get user input
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    course = input("Enter course: ")
    grade = input("Enter grade: ")
    
    # Step 4: insert data
    insert_studentrecords(cursor, first_name, last_name, course, grade)
    
    # Step 5: save changes
    connect.commit()
    
    # Step 6: display records
    view_students(cursor)
    
    # Step 7: close connection
    connect.close()
if __name__ == "__main__":
    mainProgram()
#it will call the whole main program function
