#Student management system 
import sqlite3

def Search_Feature(cursor):
        #this connects to the database
        conn = sqlite3.connect("Student_Records.db")
        cursor = conn.cursor()

        #gets the search term from the user
        term = input("\nEnter Student Name or ID to search:").strip()

        query = "SELECT * FROM students WHERE ID = ? OR name LIKE ? OR last_name Like ?"
        search_pattern = f"%{term}%"

        #We pass the search terms as a tuple to match the two '?' placeholders
        cursor.execute(query, (term, search_pattern, search_pattern))

        results = cursor.fetchall()
        #helps with error handling2
        if not results:
            print(f"\n No student records found matching '{term}'.")
        else:
            print("\n Match is found !")
            #This loops through the results (in case multiple names end up matching)

            for row in results: 
            #this unpacks the tuple data type into clear variables
                f_name, l_name, s_id, crs, grd = row
                print(f"ID: {s_id} | Name: {f_name} {l_name} | Course: {crs} | Grade: {grd}")

#Conn and cursor parameters so changes save permanently
def Delete_Feature(conn, cursor):
    #the conn is there to connect the database
    conn = sqlite3.connect("Student_Records.db")
    cursor = conn.cursor()
    target_ID = input("\nEnter Student name or ID to delete:").strip()

    check_query = "DELETE FROM students WHERE ID = ?"
    cursor.execute(check_query, (target_ID))
    #we only need to provide one match
    student = cursor.fetchone() 

    #The safety check is there to check whether the student actually exists
    #Its the safest to delete by ID because IDs are very uniue to each student
    if not student:
        print(f"\n Error: No student found with ID {target_ID}.")
    else:
        #this will unoack the found record to show the user who they are deleting
        s_id, f_name, l_name, crs, grd = student 
        print(f"\n Record Found: {f_name} {l_name}| (Course: {crs})")

        #The confirmation will double check with the user before wiping data
        confirm = input(f"Are you sure you want to permanently delete the {f_name} {l_name}? (yes/no):").strip().lower()
        if confirm == "yes":

            #the 'DELETE' is to run the deletion query
            delete_query = "DELETE FROM student WHERE ID = ?"

            cursor.execute(delete_query, (target_ID,))

            #The commit is there to permanently save the changes to the database file
            conn.commit()

            print(f"\n Sucess: Student record for '{f_name}{l_name}' has been deleted.")
        else: 
            print("\n Deletion cancelled. Record was not changed.")

# Creates the database to store student records and also creates cursor to execute SQL commands
def create_database():
    conn = sqlite3.connect("Student_Records.db")  # Creates/connects to database file
    cursor = conn.cursor()  # Allows execution of SQL commands
    return conn, cursor

def Update_feature(conn, cursor):
    conn = sqlite3.connect("Student_Records.db") #connects the database
    cursor = conn.cursor()
    target_ID = input("\nEnter Student ID  to update:").strip()
    check_query = "SELECT * FROM students WHERE ID = ?"
    cursor.execute(check_query, (target_ID,))
    student = cursor.fetchone()

    if not student:
        print(f"\n Error: No student found with ID {target_ID}.")
    else:
        f_name, l_name, crs, grd = student
        print(f"\n CUrrent Record: {f_name} {l_name} | Course: {crs} | Grade: {grd}")
        print(f"Leabe blank and press Enter to keep the current information")

        #If the user presses enter without typing, using the or to operator to keep old data make it easy
        new_first = input(f"Enter new first name ({f_name}): ").strip() or f_name
        new_last = input(f"Enter new first name ({l_name}): ").strip() or l_name
        new_course = input(f"Enter new first name ({crs}): ").strip() or crs
        new_grade = input(f"Enter new first name ({grd}): ").strip() or grd

        #? = to the placeholders to store information
        update_query = """
        UPDATE students
        SET first_name = ?, last_name = ?, course = ?, graden = ?
        WHERE ID = ?
        """
        cursor.execute(update_query, (new_first, new_last, new_course, new_grade, target_ID))

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

            insert_studentrecords(cursor, first_name, last_name, course, grade)
            connect.commit()
            print("Student added successfully")

        elif choice == "2": 
            #calls for all student records here
            view_students(cursor)

        elif choice == "3":
            Search_Feature(cursor)
            #calls the student search function
            
        elif choice == "4":
            #calls the student function here
            print("Opening student's information...")
        
        elif choice == "5":
            Delete_Feature(connect, cursor)
            #calls the delete function here
        
        elif choice == "6":
            print("Goodbye ! :)")
            break #will stop the while loop ande exits the program

        else: 
            print("Choice is invalid please retry. :(")
            #it will validate code and make sure the user puts the correct code
    connect.close()
   
if __name__ == "__main__":
    mainProgram()
#it will call the whole main program function
