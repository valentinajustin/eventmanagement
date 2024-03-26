import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import *

conn = mysql.connector.connect (
    host="localhost",
    user="root",
    password="tina123",
    database="event"
)

cursor = conn.cursor ()

# Create tables for events and attendees if they don't exist
cursor.execute ("""
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        date DATE,
        location VARCHAR(255)
    )
""")

cursor.execute ("""
    CREATE TABLE IF NOT EXISTS attendees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT,
        name VARCHAR(255),
        email VARCHAR(255),
        FOREIGN KEY (event_id) REFERENCES events(id)
    )
""")


# Functions for managing events
def create_event():
    name = event_name.get ()
    date = event_date.get ()
    location = event_location.get ()
    cursor.execute ("INSERT INTO events (name, date, location) VALUES (%s, %s, %s)", (name, date, location))
    conn.commit ()
    messagebox.showinfo ("Success", "Event created successfully.")
    clear_event_fields ()
    load_event_list ()


def load_event_list():
    cursor.execute ("SELECT * FROM events")
    events = cursor.fetchall ()
    event_listbox.delete (0, tk.END)
    for event in events:
        event_listbox.insert (tk.END, event)


def delete_selected_event():
    selected_index = event_listbox.curselection ()
    if selected_index:
        event_id = event_listbox.get (selected_index[0])[0]
        cursor.execute ("DELETE FROM events WHERE id=%s", (event_id,))
        conn.commit ()
        load_event_list ()
        messagebox.showinfo ("Success", "Event deleted successfully.")


# Functions for managing attendees
def add_attendee():
    selected_event = event_listbox.get (event_listbox.curselection ())
    if not selected_event:
        messagebox.showerror ("Error", "Select an event to add an attendee.")
        return

    event_id = selected_event[0]
    name = attendee_name.get ()
    email = attendee_email.get ()
    cursor.execute ("INSERT INTO attendees (event_id, name, email) VALUES (%s, %s, %s)", (event_id, name, email))
    conn.commit ()
    messagebox.showinfo ("Success", "Attendee added successfully.")
    clear_attendee_fields ()
    load_attendee_list (event_id)


def load_attendee_list(event_id):
    cursor.execute ("SELECT * FROM attendees WHERE event_id=%s", (event_id,))
    attendees = cursor.fetchall ()
    attendee_listbox.delete (0, tk.END)
    for attendee in attendees:
        attendee_listbox.insert (tk.END, attendee)


def delete_selected_attendee():
    selected_index = attendee_listbox.curselection ()
    if selected_index:
        attendee_id = attendee_listbox.get (selected_index[0])[0]
        cursor.execute ("DELETE FROM attendees WHERE id=%s", (attendee_id,))
        conn.commit ()
        load_attendee_list (event_listbox.get (event_listbox.curselection ())[0][0])
        messagebox.showinfo ("Success", "Attendee deleted successfully.")


# Clear input fields
def clear_event_fields():
    event_name.set ("")
    event_date.set ("")
    event_location.set ("")


def clear_attendee_fields():
    attendee_name.set ("")
    attendee_email.set ("")


# Function to search for events by name
def search_event_by_name():
    search_query = event_name_search.get ()
    cursor.execute ("SELECT * FROM events WHERE name LIKE %s", (f"%{search_query}%",))
    events = cursor.fetchall ()
    event_listbox.delete (0, tk.END)
    for event in events:
        event_listbox.insert (tk.END, event)


def calculate_total_attendees():
    selected_event = event_listbox.get (event_listbox.curselection ())
    if not selected_event:
        messagebox.showerror ("Error", "Select an event to calculate the total number of attendees.")
        return

    event_id = selected_event[0]
    cursor.execute ("SELECT COUNT(*) FROM attendees WHERE event_id = %s", (event_id,))
    total_attendees = cursor.fetchone ()[0]

    # Display total attendees in a messagebox
    messagebox.showinfo ("Total Attendees", f"Total Attendees for the selected event: {total_attendees}")


# Create the main application window
app = tk.Tk ()
app.title ("Event Management System")
app.geometry ("1200x800")
app.config (bg="black")

# Add image file
bg = PhotoImage (file="Management.png")

# Create a label widget to display the background image
background_label = Label (app, image=bg)
background_label.place (relwidth=1, relheight=1)  # Cover the entire window with the image

# Create event management section
event_name = tk.StringVar ()
event_date = tk.StringVar ()
event_location = tk.StringVar ()

event_label = tk.Label (app, text="Event Name:", font=("Franklin Gothic Demi", 20), bg="white")
event_label.place (x=50, y=30)
event_entry = tk.Entry (app, textvariable=event_name, font=("Times New Roman", 15))
event_entry.place (x=80, y=80, width=250, height=40)

date_label = tk.Label (app, text="Event Date (YYYY-MM-DD):", font=("Franklin Gothic Demi", 20), bg="white")
date_label.place (x=50, y=150)
date_entry = tk.Entry (app, textvariable=event_date, font=("Times New Roman", 15))
date_entry.place (x=80, y=190, width=250, height=40)

location_label = tk.Label (app, text="Event Location:", font=("Franklin Gothic Demi", 20), bg="white")
location_label.place (x=50, y=250)
location_entry = tk.Entry (app, textvariable=event_location, font=("Times New Roman", 15))
location_entry.place (x=80, y=290, width=250, height=40)

create_event_button = tk.Button (app, text="Create Event", command=create_event, font=("Impact", 17))
create_event_button.place (x=125, y=350)

event_listbox = tk.Listbox (app)
event_listbox.place (x=50, y=420, width=300, height=250)
event_listbox.place ()
load_event_list ()

delete_event_button = tk.Button (app, text="Delete Event", command=delete_selected_event, font=("Impact", 17))
delete_event_button.place (x=125, y=700)

# Create attendee management section
attendee_name = tk.StringVar ()
attendee_email = tk.StringVar ()

attendee_name_label = tk.Label (app, text="Attendee Name:", font=("Franklin Gothic Demi", 20), bg="white")
attendee_name_label.place (x=700, y=30)
attendee_name_entry = tk.Entry (app, textvariable=attendee_name, font=("Times New Roman", 15))
attendee_name_entry.place (x=730, y=80, width=250, height=40)

attendee_email_label = tk.Label (app, text="Attendee Email:", font=("Franklin Gothic Demi", 20), bg="white")
attendee_email_label.place (x=700, y=140)
attendee_email_entry = tk.Entry (app, textvariable=attendee_email, font=("Times New Roman", 15))
attendee_email_entry.place (x=730, y=200, width=250, height=40)

add_attendee_button = tk.Button (app, text="Add Attendee", command=add_attendee, font=("Impact", 17))
add_attendee_button.place (x=790, y=280)

attendee_listbox = tk.Listbox (app)
attendee_listbox.place (x=700, y=360, width=300, height=250)

delete_attendee_button = tk.Button (app, text="Delete Attendee", command=delete_selected_attendee, font=("Impact", 17))
delete_attendee_button.place (x=790, y=650)

# Create a label for total attendees
total_attendees_label = tk.Label (app, text="", font=("Franklin Gothic Demi", 20), bg="white")
total_attendees_label.place (x=1100, y=300)

# Create a label and entry field for event name search
event_name_search = tk.StringVar ()
search_label = tk.Label (app, text="Search Event by Name:", font=("Franklin Gothic Demi", 20), bg="white")
search_label.place (x=1100, y=30)
search_entry = tk.Entry (app, textvariable=event_name_search, font=("Times New Roman", 15))
search_entry.place (x=1150, y=80, width=250, height=40)

# Button to perform event name search
search_button = tk.Button (app, text="Search", command=search_event_by_name, font=("Impact", 17))
search_button.place (x=1250, y=150)

calculate_total_button = tk.Button (app, text="Calculate Total Attendees", command=calculate_total_attendees,
                                    font=("Impact", 17))
calculate_total_button.place (x=1100, y=250)

app.mainloop ()