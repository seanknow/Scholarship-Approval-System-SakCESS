from PIL import Image, ImageTk
import tkinter as tk
import mysql.connector
from tkinter import messagebox, simpledialog, ttk

# ----------------------
# DATABASE CONNECTION
# ----------------------
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

# ----------------------
# MAIN WINDOW
# ----------------------
root = tk.Tk()
root.title("SakCESS: Education to Success")
root.geometry("1280x720")
root.configure(bg="light blue")
root.resizable(False, False)

# BACKGROUND
bg_image = Image.open("background.png")
bg_photo = ImageTk.PhotoImage(bg_image.resize((1280, 720)))
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# INTRO FRAME
frame_box = tk.Frame(root, width=800, height=350, bg="white", highlightbackground="black", highlightthickness=2)
frame_box.pack(pady=200)

intro = tk.Label(
    frame_box,
    text="The SakCESS Program supports students by offering guidance and resources that help them succeed academically. "
         "It also provides scholarships to deserving learners, giving them access to valuable opportunities. "
         "Overall, the program aims to help students build a brighter and more successful future.",
    font=("Georgia", 20), bg="white", fg="black",
    wraplength=750
)
intro.place(relx=0.5, rely=0.5, anchor="center")

# ----------------------
# SHOW FORM
# ----------------------
def show_form():
    frame_box.pack_forget()
    apply_btn.place_forget()
    
    form_bg_image = Image.open("form.png")
    form_bg_photo = ImageTk.PhotoImage(form_bg_image.resize((1280, 720)))
    bg_label.config(image=form_bg_photo)
    bg_label.image = form_bg_photo

    form_frame.place(relx=0.5, rely=0.5, anchor="center")

apply_btn = tk.Button(root, text="Apply Now", font=("Georgia", 18), bg="light blue", width=15, height=1, command=show_form)
apply_btn.place(relx=0.5, rely=0.8, anchor="center")

# ----------------------
# FORM FRAME
# ----------------------
form_frame = tk.Frame(root, bg="lightskyblue", width=1000, height=700, highlightbackground="black", highlightthickness=2)

fields = [
    "SCODE", "FULL NAME", "AGE", "BIRTHDATE", "ADDRESS", "EMAIL ADDRESS",
    "CONTACT NO.", "SCHOOL/UNIVERSITY", "COURSE", "YEAR LEVEL", "GWA"
]

entries = {}
label_font = ("Georgia", 14)

for idx, field in enumerate(fields):
    tk.Label(form_frame, text=f"{field}:", font=label_font, bg="white", anchor="e", width=20, relief="solid").grid(row=idx, column=0, sticky="e", padx=(10,5), pady=3)
    entry = tk.Entry(form_frame, font=label_font, width=80, bg="white", relief="sunken")
    entry.grid(row=idx, column=1, sticky="we", padx=(10,10), pady=3)
    entries[field] = entry

# ----------------------
# SUBMIT FORM
# ----------------------
def submit_form():
    for field, entry in entries.items():
        if entry.get().strip() == "":
            messagebox.showwarning("Invalid Input", f"Please fill in {field}!")
            return

    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO scholar_info (
                scode, student_name, student_age, student_bday,
                student_address, email_address, contact_no,
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
        show_list()
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        cursor.close()
        db.close()

submit_btn = tk.Button(form_frame, text="SUBMIT", font=("Georgia", 18), bg="light blue", width=20, command=submit_form)
submit_btn.grid(row=len(fields), column=1, pady=15)

# ----------------------
# LIST FRAME
# ----------------------
list_frame = tk.Frame(root, bg="white")

list_container = tk.Frame(list_frame, bg="white")
list_container.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("scode", "student_name", "student_address", "school", "course", "year_lvl", "gwa")
tree = ttk.Treeview(list_container, columns=columns, show="headings", height=15)

for col, heading in zip(columns, ["SCODE", "FULL NAME", "ADDRESS", "SCHOOL/UNIV", "COURSE", "YEAR LEVEL", "GWA"]):
    tree.heading(col, text=heading, anchor="center")
    tree.column(col, width=150 if col != "gwa" else 80, anchor="center")

tree.pack(fill="both", expand=True)

# ----------------------
# LOAD LIST (SCODE MASKED)
# ----------------------
def load_list():
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
            masked_scode = '*' * len(row[0])
            row_to_insert = (masked_scode,) + row[1:]
            tree.insert("", "end", values=row_to_insert)
    
    db.close()

def show_list():
    form_frame.place_forget()
    list_frame.pack(fill="both", expand=True)
    list_frame.lift()
    load_list()

# ----------------------
# SCODE ENTRY
# ----------------------
scode_entry = tk.Entry(list_frame, font=("Arial", 16), width=40)
scode_entry.pack(pady=20)

# ----------------------
# DELETE FUNCTION
# ----------------------
def delete_scode():
    scode_to_delete = scode_entry.get().strip()

    if scode_to_delete == "":
        messagebox.showwarning("Invalid Input", "Enter SCODE to delete!")
        return

    db = connect_db()
    if not db:
        return

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM scholar_info WHERE scode = %s", (scode_to_delete,))
        db.commit()
        messagebox.showinfo("Deleted", "Record deleted successfully!")
        load_list()
    except Exception as e:
        messagebox.showerror("Error", f"Delete failed: {e}")
    finally:
        cursor.close()
        db.close()

delete_button = tk.Button(list_frame, text="Delete", font=("Arial", 16), bg="lightblue", command=delete_scode)
delete_button.pack(pady=10)

# ----------------------
# UPDATE FUNCTION (Name, Address, School, Course, Year, GWA)
# ----------------------
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
    update_win.resizable(False, False)

    # Background image
    try:
        bg_image = Image.open("updatebg.png").resize((500, 500), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(update_win, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load background image: {e}")

    # Frame for entries
    form_frame = tk.Frame(update_win, bg="white")
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Fields dictionary to simplify
    fields = {
        "Name": curr_name,
        "Address": curr_address,
        "School": curr_school,
        "Course": curr_course,
        "Year Level": curr_year,
        "GWA": curr_gwa
    }

    entries = {}
    for label, value in fields.items():
        tk.Label(form_frame, text=label + ":", bg="white").pack(pady=5)
        entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
        entry.insert(0, value)
        entry.pack()
        entries[label] = entry

    def save_update():
        new_values = [entry.get().strip() for entry in entries.values()]
        try:
            cursor.execute("""
                UPDATE scholar_info
                SET student_name=%s, student_address=%s, school=%s, course=%s, year_lvl=%s, gwa_=%s
                WHERE scode=%s
            """, (*new_values, scode_to_update))
            db.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            load_list()
            update_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")
        finally:
            cursor.close()
            db.close()

    tk.Button(form_frame, text="Save Changes", bg="lightgreen", font=("Arial", 14), command=save_update).pack(pady=15)

update_button = tk.Button(list_frame, text="Update", font=("Arial", 16), bg="lightgreen", command=update_scode)
update_button.pack(pady=10)


# ----------------------
# MAIN LOOP
# ----------------------
root.mainloop()
