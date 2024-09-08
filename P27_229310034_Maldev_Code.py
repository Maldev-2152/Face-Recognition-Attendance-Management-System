import cv2
import mysql.connector
import face_recognition
import numpy
import pandas
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Maldev$1',
    database = 'student_attendance'

)

cursor = connection.cursor()

#Functions

def edit_data():
    entity = clicked3.get()
    ID = id_entry.get()
    value = value_entry.get()
    frame4.pack_forget()


    #entity = input("Enter entity: ")
    #ID = input("Enter ID: ")
    #value = input("Enter Value: ")
    
    try:
        if entity == "Attendance":
            cursor.execute('''UPDATE ATTENDANCE SET TODAY_ATTENDANCE=%s WHERE S_ID=%s;''',(value,ID))
            display_result_label.config(text="Attendance Updated Succesfully", bg='#333333', fg='#FFFFFF', font=("Ariel",30))

        elif entity == "Name":
            cursor.execute('''UPDATE STUDENTS SET NAME=%s WHERE S_ID=%s;''',(value,ID))
            display_result_label.config(text="Name Updated Succesfully", bg='#333333', fg='#FFFFFF', font=("Ariel",30))

        elif entity == "Email ID":
            cursor.execute('''UPDATE STUDENTS SET EMAIL_ID=%s WHERE S_ID=%s;''',(value,ID))
            display_result_label.config(text="Email ID Updated Succesfully", bg='#333333', fg='#FFFFFF', font=("Ariel",30))

        else:
            #print("FAIL")
            display_result_label.config(text="Updated not Succesful", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
    except:
        display_result_label.config(text="ERROR", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
    finally:
        connection.commit()
        frame4.pack()

    id_entry.delete(0, tk.END)
    value_entry.delete(0, tk.END)


def show_data_1():
    # Fetch data from the table
    try:
        cursor.execute('''SELECT S_ID AS ID, TODAY_ATTENDANCE, TOTAL_PRESENT,TOTAL_DAYS FROM ATTENDANCE''')
    except:
        display_result_label.config(text="ERROR", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
        frame4.pack()
        return
        
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    # Create a pandas DataFrame to hold the data
    data = pandas.DataFrame(rows, columns=columns)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Display Table Data")

    # Create a treeview widget with scrollbars
    tree = ttk.Treeview(root, columns=tuple(data.columns), show="headings")
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Insert table columns and data into the treeview
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, stretch=True, width=100)
    for index, row in data.iterrows():
        tree.insert("", "end", values=tuple(row))

    # Place the treeview and scrollbars in the window
    tree.grid(column=0, row=0, sticky="nsew")
    vsb.grid(column=1, row=0, sticky="ns")
    hsb.grid(column=0, row=1, sticky="ew")

    root.mainloop()


def show_data_2():
    # Fetch data from the table
    try:
        cursor.execute("SELECT S_ID AS ID, NAME, EMAIL_ID FROM STUDENTS")
    except:
        display_result_label.config(text="ERROR", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
        frame4.pack()
        return
        
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    # Create a pandas DataFrame to hold the data
    data = pandas.DataFrame(rows, columns=columns)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Display Table Data")

    # Create a treeview widget with scrollbars
    tree = ttk.Treeview(root, columns=tuple(data.columns), show="headings")
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Insert table columns and data into the treeview
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, stretch=True, width=100)
    for index, row in data.iterrows():
        tree.insert("", "end", values=tuple(row))

    # Place the treeview and scrollbars in the window
    tree.grid(column=0, row=0, sticky="nsew")
    vsb.grid(column=1, row=0, sticky="ns")
    hsb.grid(column=0, row=1, sticky="ew")

    root.mainloop()


def login():
    username = username_entry.get()
    password = password_entry.get()
    user = clicked.get()


    if user == "Faculty":       #Check Faculty Login
            
        cursor.execute('''SELECT * FROM TEACHER_LOGIN;''')
        #a=input("Enter Username: ")
        #b=input("Enter Password: ")
        result = cursor.fetchall()
        flag=-1

        for row in result:
            ID,pwd = row
            if ID==username and pwd==password:
                #print("Login Succesful")
                flag=0
                break
        

        if flag==0:     #If Faculty Login succesful
            #print("Login Succesful")

            frame1.pack_forget()
            messagebox.showinfo(title="Success", message="Logged in Succesfully")


            message_label.config(text="Welcome Faculty", bg='#333333', fg='#FFFFFF', font=("Ariel",30))

            mark_attendance_button.grid(row=1, column=5, columnspan=2, pady=10, padx=50)
            #edit_attendance_button.grid(row=1, column=5, columnspan=2, pady=10, padx=50)
            #check_attendance_button.grid(row=0, column=2, columnspan=2, pady=10, padx=50)
            edit_data_button.grid(row=1, column=3, columnspan=2, pady=10, padx=50)
            register_student_button.grid(row=1, column=1, columnspan=2, pady=10, padx=50)
            #logout_button.grid(row=0, column=4, columnspan=2, pady=10, padx=50)

            '''
            db_operation_lable.grid(row=0, column=0, pady=10, padx=50)
            table_lable.grid(row=1, column=0, pady=10, padx=50)
            column_lable.grid(row=2, column=0, pady=10, padx=50)
            id_lable.grid(row=3, column=0, pady=10, padx=50)
            value_lable.grid(row=4, column=0, pady=10, padx=50)

            db_operation_drop.grid(row=0, column=1)
            table_drop.grid(row=1, column=1)
            column_drop.grid(row=2, column=1)
            id_entry.grid(row=3, column=1)
            value_entry.grid(row=4, column=1)'''
            frame3.pack()
            frame2.pack()
            
        else:       #If faculty Login Fail
            #print("Username or Password is invalid")
            messagebox.showerror(title="Error", message="Username or Password is incorrect")


    else:      #Check Student Login
        
        cursor.execute('''SELECT * FROM STUDENT_LOGIN;''')
        #a=int(input("Enter Username: "))
        #b=input("Enter Password: ")
        result = cursor.fetchall()
        flag=-1
        
        for row in result:
            ID,pwd = row
            if str(ID)==username and pwd==password:
                #print("Login Succesful")
                flag=0
                break
        
        if flag==0:     #If Student Login Succesful
            #print("Login Succesful")

            frame1.pack_forget()
            message_label.config(text="Welcome Student", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
            
            mark_attendance_button.grid_forget()
            #edit_attendance_button.grid_forget()
            #check_attendance_button.grid_forget()
            edit_data_button.grid_forget()
            register_student_button.grid_forget()
            #logout_button.grid_forget()

            '''
            #db_operation_lable.grid_forget()
            #table_lable.grid_forget()
            column_lable.grid_forget()
            id_lable.grid_forget()
            value_lable.grid_forget()

            #db_operation_drop.grid_forget()
            #table_drop.grid_forget()
            column_drop.grid_forget()
            id_entry.grid_forget()
            value_entry.grid_forget()'''
            frame3.pack_forget()
            frame2.pack()

            
        else:       #If Student Login Fail
            #print("Username or Password is invalid")
            messagebox.showerror(title="Error", message="Username or Password is incorrect")

    #frame3.pack()
    #frame2.pack()
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    clicked.set("Student")


def logout():
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    message_label.config(text="Login", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
    frame1.pack()

def get_encodings():
    
    # Execute a query to retrieve all arrays
    cursor.execute("SELECT name,image_array FROM students")

    # Fetch all the results
    results = cursor.fetchall()    

    # Process each row to extract and deserialize the arrays
    array_dict = {}

    for row in results:
        name,array = row
        array = json.loads(array)
        array = numpy.array(array)
        array_dict[name] = array

    return array_dict


def capture_image():
    #this function captures image from webcam and return the face encodings, numpy array, for the following image
     
    cap = cv2.VideoCapture(0)  # Setup camera
   
    while True: 
        ret, frame = cap.read()    # Capture frame-by-frame, frame will store the image         
        cv2.imshow('WebCam', frame)    # Show the captured image
        if cv2.waitKey(1) == ord('q'):    # wait for the key and come out of the loop
            break

    #Closes webcam for the capturing device and destroys all the windows we created.
    cap.release()
    cv2.destroyAllWindows()

    #get the encodings for image stored in frame as a numpy array
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    encodings = numpy.array(encodings)

    return encodings   #return the encodings


def compare_two_images(encodings1,encodings2):
    # Compare the encodings of both faces
    matches = face_recognition.compare_faces(encodings1, encodings2)
    
    return matches[0]


def mark_attendance(name):
    cursor.execute('''SELECT S_ID FROM STUDENTS WHERE NAME=%s;''', (name,))
    ID = cursor.fetchone()[0]  # Extract the value from the tuple

    cursor.execute('''SELECT TOTAL_PRESENT FROM ATTENDANCE WHERE S_ID=%s;''', (ID,))
    x = cursor.fetchone()[0] + 1  # Extract the value from the tuple

    cursor.execute('''SELECT TOTAL_DAYS FROM ATTENDANCE WHERE S_ID=%s;''', (ID,))
    y = cursor.fetchone()[0] + 1  # Extract the value from the tuple

    #print(ID, x, y)
    connection.commit()
    
    try:
        cursor.execute('''UPDATE ATTENDANCE SET TODAY_ATTENDANCE="P" WHERE S_ID=%s;''', (ID,))
        #print("SUCCESS!")

        cursor.execute('''UPDATE ATTENDANCE SET TOTAL_PRESENT=%s WHERE S_ID=%s;''', (x, ID))
        #print("SUCCESS!")

        cursor.execute('''UPDATE ATTENDANCE SET TOTAL_DAYS=%s WHERE S_ID=%s;''', (y, ID))
        #print("SUCCESS!")

        connection.commit()
    except:
        connection.rollback()

def submit_attendance():
    try:
        cursor.execute('''UPDATE ATTENDANCE SET TODAY_ATTENDANCE="A" WHERE TODAY_ATTENDANCE IS NULL;''')
        #connection.commit()

        cursor.execute('''SELECT S_ID FROM ATTENDANCE WHERE TODAY_ATTENDANCE="A";''')
        result = cursor.fetchall()

        x=len(result)
        
        for ID in result:
            student_id = ID[0]  # Extracting the student ID from the tuple

            cursor.execute('''SELECT TOTAL_DAYS FROM ATTENDANCE WHERE S_ID=%s;''', (student_id,))
            days = cursor.fetchone()[0] + 1

            cursor.execute('''UPDATE ATTENDANCE SET TOTAL_DAYS=%s WHERE S_ID=%s;''', (days, student_id))
            #print(student_id, "has been marked absent")

        cursor.execute('''UPDATE ATTENDANCE SET TODAY_ATTENDANCE=NULL WHERE S_ID>2000;''') 

        connection.commit()
        display_result_label.config(text=f"Attendance Submitted, {x} Students have been marked Absent", bg='#333333', fg='#FFFFFF', font=("Ariel",30))


    except:
        connection.rollback()
        display_result_label.config(text="ERROR while updating attendance, TRY AGAIN", bg='#333333', fg='#FFFFFF', font=("Ariel",30))

    frame4.pack()

def face_compare():
    database_encodings = get_encodings()
    encodings = capture_image()
    matched_person = 0
    lowest_distance = 1

    #frame4.pack_forget()
    try:
        for key,value in database_encodings.items():
            
            if compare_two_images(encodings,value) == True:
                distance = numpy.linalg.norm(encodings[0] - value[0])
                #print(key, distance)

                if distance<0.4 and distance<lowest_distance:
                    matched_person = key
                    lowest_distance = distance
                    #print(key, distance)
                    #print(matched_person)

            else:
                continue

    except:
        matched_person = -1

    finally:
        if isinstance(matched_person,str) == True:
            mark_attendance(matched_person)
            display_result_label.config(text=f"Face Detected,{matched_person} has been marked present", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
            #print(f"Face Matched\n{matched_person} has been marked present")

        elif matched_person == 0:
            display_result_label.config(text="No Face Matched", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
            #print("No Face Matched")

        else:
            display_result_label.config(text="No Face Detected", bg='#333333', fg='#FFFFFF', font=("Ariel",30))
            #print("No Face Detected")

        frame4.pack()    

#Create window
window = tk.Tk()
window.title("Login Page")
window.geometry('900x400')
window.configure(bg='#333333')

message_label = tk.Label(window, text="Login", bg='#333333', fg='#FFFFFF', font=("Ariel",30)) #in the window and not in Farme 1,2 or 3
message_label.pack()


#Frames 1
frame1 = tk.Frame(window, bg='#333333')    #Frame for Login

#Creating Widgets for Frame 1
user_label = tk.Label(frame1, text="Login As", bg='#333333', fg='#FFFFFF', font=("Ariel",16))
username_label = tk.Label(frame1, text="Username", bg='#333333', fg='#FFFFFF', font=("Ariel",16))
password_label = tk.Label(frame1, text="Password", bg='#333333', fg='#FFFFFF', font=("Ariel",16))

clicked = tk.StringVar()
clicked.set("Student")  # Set the default value to "Student"
drop = tk.OptionMenu(frame1, clicked, "Student", "Faculty")
drop.config(width=17, font=("Arial", 16))

username_entry = tk.Entry(frame1, font=("Ariel",16))
password_entry = tk.Entry(frame1, show="*", font=("Ariel",16))
login_button = tk.Button(frame1, text="Login", font=("Ariel",16), command=login)


#Placing Widgets for Frame 1
user_label.grid(row=1, column=0, pady=10, padx=50)
drop.grid(row=1, column=1)
username_label.grid(row=2, column=0, pady=10, padx=50)
username_entry.grid(row=2, column=1)
password_label.grid(row=3, column=0, pady=10, padx=50)
password_entry.grid(row=3, column=1)
login_button.grid(row=4, column=0, columnspan=2, pady=25, padx=150)

frame1.pack()


#Frame 2
frame2 = tk.Frame(window, bg='#333333')    #Frame for Database Operations Buttons

#Creating Widgets for Frame 2
mark_attendance_button = tk.Button(frame2, text="Mark Attendance", font=("Ariel",16), width=15, command=face_compare)
#edit_attendance_button = tk.Button(frame2, text="Edit Attendance", font=("Ariel",16), width=15)
check_attendance_button = tk.Button(frame2, text="Check Attendance", font=("Ariel",16), width=15, command=show_data_1)
edit_data_button = tk.Button(frame2, text="Edit Data", font=("Ariel",16), width=15, command=edit_data)
register_student_button = tk.Button(frame2, text="Submit", font=("Ariel",16), width=15, command=submit_attendance)
logout_button = tk.Button(frame2, text="Logout", font=("Ariel",16), width=15, command=logout)
student_info_button = tk.Button(frame2, text="Student Info", font=("Ariel",16), width=15, command=show_data_2)

'''display_result_label = tk.Label(frame4, text="", bg='#333333', fg='#FFFFFF', font=("Ariel",16))'''

#Placing Widgets for Frame 2
#mark_attendance_button.grid(row=1, column=5, columnspan=2, pady=10, padx=50)       change to - row=1, column=5
#edit_attendance_button.grid(row=1, column=5, columnspan=2, pady=10, padx=50)
check_attendance_button.grid(row=0, column=2, columnspan=2, pady=10, padx=50)
#edit_data_button.grid(row=1, column=3, columnspan=2, pady=10, padx=50)
#register_student_button.grid(row=1, column=1, columnspan=2, pady=10, padx=50)
logout_button.grid(row=0, column=4, columnspan=2, pady=10, padx=50)
student_info_button.grid(row=0, column=0, columnspan=2, pady=10, padx=50)           #change to - row=0, column=0
'''display_result_label.grid(row=2, column=6, pady=10, padx=50)'''

#frame2.pack()

#Frame 3
frame3 = tk.Frame(window, bg='#333333')     #Frame for input value

#Creating Widgets for Frame 3
#db_operation_lable = tk.Label(frame3, text="DB Operation", bg='#333333', fg='#FFFFFF', font=("Ariel",16))
#table_lable = tk.Label(frame3, text="Table", bg='#333333', fg='#FFFFFF', font=("Ariel",16))
column_lable = tk.Label(frame3, text="Entity", bg='#333333', fg='#FFFFFF', font=("Ariel",16))
id_lable = tk.Label(frame3, text="ID", bg='#333333', fg='#FFFFFF', font=("Ariel",16))
value_lable = tk.Label(frame3, text="New Value", bg='#333333', fg='#FFFFFF', font=("Ariel",16))

id_entry = tk.Entry(frame3, font=("Ariel",16))
value_entry = tk.Entry(frame3, font=("Ariel",16))

'''clicked1 = tk.StringVar()
db_operation_drop = tk.OptionMenu(frame3, tk.StringVar(), "Update", "Select")
db_operation_drop.config(width=17, font=("Arial", 16))

clicked2 = tk.StringVar()
table_drop = tk.OptionMenu(frame3, clicked2, "Student", "Attendance")
table_drop.config(width=17, font=("Arial", 16))'''

clicked3 = tk.StringVar()
column_drop = tk.OptionMenu(frame3, clicked3, "Name", "Email ID", "Attendance")
column_drop.config(width=17, font=("Arial", 16))


#Placing Widgets for Frame 3
#db_operation_lable.grid(row=0, column=0, pady=10, padx=50)
#table_lable.grid(row=1, column=0, pady=10, padx=50)
column_lable.grid(row=2, column=0, pady=10, padx=50)
id_lable.grid(row=3, column=0, pady=10, padx=50)
value_lable.grid(row=4, column=0, pady=10, padx=50)

#db_operation_drop.grid(row=0, column=1)
#table_drop.grid(row=1, column=1)
column_drop.grid(row=2, column=1)
id_entry.grid(row=3, column=1)
value_entry.grid(row=4, column=1)

#frame3.pack()


#Frame 4
frame4 = tk.Frame(window, bg='#333333')     #Frame for display result

#Create Widgets for Frame 4
display_result_label = tk.Label(frame4, text="", bg='#333333', fg='#FFFFFF', font=("Ariel",16))

#Placing Widgets for Frame 4
display_result_label.grid(row=2, column=6, pady=10, padx=50)

#frame4.pack()

window.mainloop()
connection.close()
