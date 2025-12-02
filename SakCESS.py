#                GOAL
# CONNECTED SA mysql database (scholar_db)
# INTO - apply button
# SUBMIT BUTTON DON SA APPLICATION FORM
# TAPOS PAG KA SUBMIT AY PUPUNTA DON SA MGA LIST NG ISKOLAR
# SA KALIWANG BABA MAY NAKALAGAY NA BUTTON NG UPDATE AND DELETE TAS SA KANAN AY EXIT
# PAG PININDOT ANG UPDATE MAY MAG POP UP NA MESSAGE NA KUNG ANONG SCODE NYA NA IUUPATE, TAS PAG NALAGAY SCODE AY PWEDE NA NYA I-EDIT AND SUBMIT
# PAG PININDOT ANG DELETE AY MAY MAG POP UP DIN NA MESSAGE KUNG ANO ANG SCODE NA IDEDELETE, TAS PAG NACONFIRM ANG SCODE AY AUTOMATIC DELETE.
# EXIT 
# 


from PIL import Image, ImageTk
import tkinter as tk
import mysql.connector
from tkinter import messagebox, simpledialog, ttk

def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="scholar_db"
        )
        return db
    except:
        messagebox.showerror("Database Error", "ERROR!")
        return None

# main window frame 1
root = tk.Tk()
root.title("SakCESS: Education to Success")
root.geometry("1280x720")
root.configure(bg="light blue")
root.resizable(False, False)

# background
bg_image = Image.open("background.png")
bg_photo = ImageTk.PhotoImage(bg_image.resize((1280, 720)))
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# intro 
frame_box = tk.Frame(root, width=800, height=350, bg="white", highlightbackground="black", highlightthickness=2)
frame_box.pack(pady=200) #center of frame

intro = tk.Label(
    frame_box,
    text="The SakCESS Program offers scholarships to deserving students. "
         "These scholarships help learners access quality education and opportunities. "
         "By supporting students financially, the program removes barriers to success." 
         "Its goal is to help students build a brighter future",
    font=("System", 22), bg="white", fg="black",
    wraplength=750 # to make the text compress
)
intro.place(relx=0.5, rely=0.5, anchor="center") #text format

# new frame 2 function
def show_form():
    frame_box.pack_forget()  # hide intro frame
    apply_btn.place_forget() # hide apply button
    
    # bg for frame 2
    form_bg_image = Image.open("form.png")
    form_bg_photo = ImageTk.PhotoImage(form_bg_image.resize((1280, 720)))
    bg_label.config(image=form_bg_photo)
    bg_label.image = form_bg_photo   # keep reference

    form_frame.place(relx=0.5, rely=0.5, anchor="center")

# apply button
apply_btn = tk.Button(root, text="Apply Now", font=("System", 18), bg="white", width=15, height=1, command=show_form)
apply_btn.place(relx=0.5, rely=0.8, anchor="center")

# properties and attr of frame 2
form_frame = tk.Frame(root, bg="lightskyblue", width=1000, height=700, highlightbackground="black", highlightthickness=2)

fields = [
    "SCODE", "FULL NAME", "AGE", "BIRTHDATE", "ADDRESS", "EMAIL ADDRESS",
    "CONTACT NO.", "SCHOOL/UNIVERSITY", "COURSE", "YEAR LEVEL", "GWA"
] # list of fields (nakabase sa database. )

entries = {}
label_font = ("System", 14)

# formation of fields 
for idx, field in enumerate(fields):
    # label
    label = tk.Label(form_frame, text=f"{field}:", font=label_font, bg="white", anchor="e", width=20, relief ="solid")
    label.grid(row=idx, column=0, sticky="e", padx=(10, 5), pady=3)
    
    # entry
    entry = tk.Entry(form_frame, font=label_font, width=80, bg="white", relief="sunken")
    entry.grid(row=idx, column=1, sticky="we", padx=(10,10), pady=3)
    entries[field] = entry
    
def submit_form():
    for field, entry in entries.items():
        if entry.get().strip() == "": # check if meron laman
            messagebox.showwarning("Invalid Input", f"Please fill in {field}!")
            return  # stop function kung may empty
    

    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    try:
        # insert sa database
        cursor.execute("""
            INSERT INTO scholar_info ( scode, student_name, student_age, student_bday,  student_address, email_address, contact_no,
            school, course, year_lvl, gwa_
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            entries["SCODE"].get(),
            entries["FULL NAME"].get(),
            entries["AGE"].get(),
            entries["BIRTHDATE"].get(),
            entries["ADDRESS"].get(),
            entries["EMAIL ADDRESS"].get(),
            entries["CONTACT NO."].get(),
            entries["SCHOOL/UNIVERSITY"].get(),
            entries["COURSE"].get(),
            entries["YEAR LEVEL"].get(),
            entries["GWA"].get()
        ))
        db.commit()
        messagebox.showinfo("APPLICATION SUBMITTED", "SUBMITTED! Your Application is under Evaluation.")
        show_list()  # punta sa list of students frame

    except Exception as e: # ito ay kapag erro sa database
        messagebox.showerror("Error", f"Database error: {e}")
    finally: # close (para masiguro)
        cursor.close()
        db.close()

# submit button 
submit_btn = tk.Button(form_frame, text="SUBMIT", font=("System", 18), bg="light blue", width=20, command=submit_form)
submit_btn.grid(row=len(fields), column=1, pady=15)



# list of students (frame 3)

list_frame = tk.Frame(root, bg="white")

list_container = tk.Frame(list_frame, bg="white")
list_container.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("scode", "student_name", "student_address", "school", "course", "year_lvl", "gwa")
tree = ttk.Treeview(list_container, columns=columns, show="headings", height=15)

for col, heading in zip(columns, ["SCODE", "FULL NAME", "ADDRESS", "SCHOOL/UNIV", "COURSE", "YEAR LEVEL", "GWA"]):
    tree.heading(col, text=heading, anchor="center")
    tree.column(col, width=150 if col != "gwa" else 80, anchor="center")

tree.pack(fill="both", expand=True)

# load list of student 

def load_list():
    """Load all student records into the Treeview"""
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    db = connect_db()
    if not db:
        return
    
    with db.cursor() as cursor:  
        cursor.execute("""
            SELECT scode, student_name, student_address, school, course, year_lvl, gwa_
            FROM scholar_info
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    
    db.close()  # close the connection

# function of show list
def show_list():
    form_frame.place_forget()
    list_frame.pack(fill="both", expand=True)
    list_frame.lift()
    load_list()

#delete ffunction
def delete_scode():
    scode_to_delete = scode_entry.get().strip()

    if scode_to_delete == "":
        messagebox.showwarning("Invalid Input", "Enter SCODE to delete!")
        return

    db = connect_db()
    if not db:
        return

    cursor = db.cursor()

    cursor.execute("DELETE FROM scholar_info WHERE scode = %s", (scode_to_delete,))
    db.commit()

    if cursor.rowcount == 0:
        messagebox.showwarning("Not Found", "No record found with SCODE. Try again!")
    else:
        messagebox.showinfo("Deleted", "Record deleted successfully!")

    cursor.close()
    db.close()
    load_list()  # reload table


# scode entry box for delete
scode_entry = tk.Entry(list_frame, font=("System", 16), width=30)
scode_entry.pack(pady=10)

# delete button
delete_button = tk.Button(list_frame, text="Delete", font=("System", 16), bg="lightblue", command=delete_scode)
delete_button.pack(pady=10)


# update function
def update_scode():
    scode_to_update = scode_entry.get().strip()

    if scode_to_update == "":
        messagebox.showwarning("INVALID", "Enter SCODE to update!")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor()

    cursor.execute("SELECT student_name, student_address, school, course, year_lvl, gwa_ FROM scholar_info WHERE scode=%s", (scode_to_update,))
    record = cursor.fetchone()

    if not record:
        messagebox.showwarning("Not Found", "No student found with that SCODE.")
        cursor.close()
        db.close()
        return

    curr_name, curr_address, curr_school, curr_course, curr_year, curr_gwa = record

    update_win = tk.Toplevel()
    update_win.title("Update Record")
    update_win.geometry("500x500")
    update_win.configure(bg="white")
    update_win.resizable(False, False)  # Prevent resizing to keep image fit

    # Load background image with error handling
    try:
        bg_image = Image.open("updatebg.png")
        bg_image = bg_image.resize((500, 500), Image.LANCZOS)  
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load background image: {e}")
        bg_photo = None  # faallback if image fails

    if bg_photo:
        bg_label = tk.Label(update_win, image=bg_photo)
        bg_label.image = bg_photo 
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    tk.Label(update_win, text="Name:", bg="white", fg="black", relief="raised", bd=2).place(relx=0.3, rely=0.25, anchor="e")
    name_entry = tk.Entry(update_win, font=("Arial", 14), width=20, bg="white", fg="black", relief="sunken", bd=2)
    name_entry.insert(0, curr_name)
    name_entry.place(relx=0.6, rely=0.25, anchor="c")

    tk.Label(update_win, text="Address:", bg="white", fg="black", relief="raised", bd=2).place(relx=0.3, rely=0.35, anchor="e")
    address_entry = tk.Entry(update_win, font=("Arial", 14), width=20, bg="white", fg="black", relief="sunken", bd=2)
    address_entry.insert(0, curr_address)
    address_entry.place(relx=0.6, rely=0.35, anchor="c")

    tk.Label(update_win, text="School:", bg="white", fg="black", relief="raised", bd=2).place(relx=0.3, rely=0.45, anchor="e")
    school_entry = tk.Entry(update_win, font=("Arial", 14), width=20, bg="white", fg="black", relief="sunken", bd=2)
    school_entry.insert(0, curr_school)
    school_entry.place(relx=0.6, rely=0.45, anchor="c")

    tk.Label(update_win, text="Course:", bg="white", fg="black", relief="raised", bd=2).place(relx=0.3, rely=0.55, anchor="e")
    course_entry = tk.Entry(update_win, font=("Arial", 14), width=20, bg="white", fg="black", relief="sunken", bd=2)
    course_entry.insert(0, curr_course)
    course_entry.place(relx=0.6, rely=0.55, anchor="c")

    tk.Label(update_win, text="Year Level:", bg="white", fg="black", relief="raised", bd=2).place(relx=0.3, rely=0.65, anchor="e")
    year_entry = tk.Entry(update_win, font=("Arial", 14), width=20, bg="white", fg="black", relief="sunken", bd=2)
    year_entry.insert(0, curr_year)
    year_entry.place(relx=0.6, rely=0.65, anchor="c")

    tk.Label(update_win, text="GWA:", bg="white", fg="black", relief="raised", bd=2).place(relx=0.3, rely=0.75, anchor="e")
    gwa_entry = tk.Entry(update_win, font=("Arial", 14), width=20, bg="white", fg="black", relief="sunken", bd=2)
    gwa_entry.insert(0, curr_gwa)
    gwa_entry.place(relx=0.6, rely=0.75, anchor="c")

    # SAVE FUNCTION
    def save_update():
        new_name = name_entry.get().strip()
        new_address = address_entry.get().strip()
        new_school = school_entry.get().strip()
        new_course = course_entry.get().strip()
        new_year = year_entry.get().strip()
        new_gwa = gwa_entry.get().strip()

        try:
            cursor.execute("""
                UPDATE scholar_info
                SET student_name=%s, student_address=%s, school=%s, course=%s, year_lvl=%s, gwa_=%s
                WHERE scode=%s
            """, (new_name, new_address, new_school, new_course, new_year, new_gwa, scode_to_update))

            db.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            load_list()
            update_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")
        finally:
            cursor.close()
            db.close()

    tk.Button(update_win, text="Save Changes", bg="lightgreen", fg="black", font=("Arial", 14),
               relief="raised", bd=2, command=save_update).place(relx=0.5, rely=0.86, anchor="center")

# UPDATE BUTTON
update_button = tk.Button(list_frame, text="Update", font=("Arial", 16), bg="lightgreen", command=update_scode)
update_button.pack(pady=10)


root.mainloop()