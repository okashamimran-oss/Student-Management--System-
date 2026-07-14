import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="student_db",  # Agar koi naya DB banaya hai to uska naam likhein
        user="postgres",
        password="okasha",  
        port="1024"
    )
    cursor = conn.cursor()
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        roll_number VARCHAR(50) UNIQUE NOT NULL,
        marks NUMERIC(5, 2)
    );
    """)
    conn.commit()
    print("Database connected and table is ready!")

except Exception as e:
    print("Database not connected . Error:", e)
    exit()


# 2. STUDENT CLASS WITH DATABASE QUERIES
class Student:
    
    @classmethod
    def add_student(cls):
        name = input("Enter student name: ")
        roll_number = input("Enter student roll number: ")
        marks = float(input("Enter student marks: "))
        
        try:
            
            cursor.execute(
                "INSERT INTO students (name, roll_number, marks) VALUES (%s, %s, %s);",
                (name, roll_number, marks)
            )
            conn.commit() 
            print(f"Student {name} added to database successfully!")
        except Exception as e:
            conn.rollback() 
            print("Error! This roll number already exists:", e)

    @classmethod
    def update_student_marks(cls):
        roll = input("Enter student roll number: ")
        
        
        cursor.execute("SELECT * FROM students WHERE roll_number = %s;", (roll,))
        student_data = cursor.fetchone()
        
        if student_data:
            new_marks = float(input("Enter new marks: "))
            try:
                
                cursor.execute(
                    "UPDATE students SET marks = %s WHERE roll_number = %s;",
                    (new_marks, roll)
                )
                conn.commit()
                print("Marks successfully updated!")
            except Exception as e:
                conn.rollback()
                print("Failed to update the student record:", e)
        else:
            print("Student not found in database.")

    @classmethod
    def show_all_students(cls):
        
        cursor.execute("SELECT name, roll_number, marks FROM students;")
        all_data = cursor.fetchall()
        
        if not all_data:
            print("No students found in the database.")
        else:
            print("\n--- All Students ---")
            for row in all_data:
                print(f"Name: {row[0]}, Roll Number: {row[1]}, Marks: {row[2]}")


# 3. MAIN MENU LOOP
def menu():
    while True:
        print("\n==================Student Management System==================")
        print("1. Add Student")
        print("2. Update marks")
        print("3. Show all students")
        print("4. Exit")
        
        choice = input("Enter your choice (1/4): ")
        if choice == "1":
            Student.add_student()
        elif choice == "2":
            Student.update_student_marks()
        elif choice == "3":
            Student.show_all_students()
        elif choice == "4":
            print("Exiting and closing database connection. Good Bye!")
            
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

menu()





