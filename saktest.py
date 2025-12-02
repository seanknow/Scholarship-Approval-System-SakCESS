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


from PIL import Image, ImageTk # for image bg
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
root.resizable(False, False)

# background
bg_image = Image.open("background.png")
bg_photo = ImageTk.PhotoImage(bg_image.resize((1280, 720)))
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# intro 
frame_box = tk.Frame(root, width=800, height=350, bg="white", highlightbackground="black", highlightthickness=2)
frame_box.pack(pady=200) # center of frame

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
    frame_box.pack_forget()  # to hide intro frame
    apply_btn.place_forget() # tp hide apply button
    
    # bg for frame 2
    form_bg_image = Image.open("form.png")
    form_bg_photo = ImageTk.PhotoImage(form_bg_image.resize((1280, 720)))
    bg_label.config(image=form_bg_photo)
    bg_label.image = form_bg_photo 

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
    

    # automatic saved into connected database
def submit_form():
    for field, entry in entries.items():
        if entry.get().strip() == "": # check if meron laman
            messagebox.showwarning("Invalid Input", f"Please fill in {field}!")
            return  # stop function kung empty
    
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




# load student list
# plain white bg

# function for delete
# scode to delete


# function for update
# scode to update
# background for update format


root.mainloop()