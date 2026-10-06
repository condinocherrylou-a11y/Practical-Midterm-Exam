import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("directory.db")
cursor = conn.cursor()

# Create table with Name, Age, and Genre columns
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    genre TEXT
)
"""
)

conn.commit()


# =========================
# FUNCTIONS
# =========================


# CREATE
def add_record():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    genre = genre_entry.get().strip()

    if name == "" or age == "":
        messagebox.showwarning(
            "Warning", "Please fill in Name and Age fields."
        )
        return

    cursor.execute(
        "INSERT INTO records (name, age, genre) VALUES (?, ?, ?)",
        (name, age, genre),
    )
    conn.commit()

    messagebox.showinfo("Success", "Record added successfully.")
    clear_fields()
    display_records()


# READ
def display_records():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT id, name, age, genre FROM records")
    records = cursor.fetchall()

    for i, record in enumerate(records):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert(
            "",
            tk.END,
            iid=record[0],
            values=(record[1], record[2], record[3] or ""),
            tags=(tag,),
        )


# UPDATE
def update_record():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a record to update.")
        return

    record_id = selected[0]
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    genre = genre_entry.get().strip()

    if name == "" or age == "":
        messagebox.showwarning(
            "Warning", "Please fill in Name and Age fields."
        )
        return

    cursor.execute(
        """
        UPDATE records
        SET name = ?, age = ?, genre = ?
        WHERE id = ?
    """,
        (name, age, genre, record_id),
    )

    conn.commit()

    messagebox.showinfo("Success", "Record updated successfully.")
    clear_fields()
    display_records()


# DELETE
def delete_record():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return

    record_id = selected[0]

    confirm = messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this record?"
    )

    if confirm:
        cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()

        messagebox.showinfo("Success", "Record deleted successfully.")
        clear_fields()
        display_records()


# CLEAR INPUTS
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)

    if tree.selection():
        tree.selection_remove(tree.selection())


# SELECT RECORD
def select_record(event):
    selected = tree.selection()

    if selected:
        record = tree.item(selected[0])["values"]
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        genre_entry.delete(0, tk.END)

        name_entry.insert(0, record[0])
        age_entry.insert(0, record[1])
        genre_entry.insert(0, record[2] if len(record) > 2 else "")


# EXIT APP
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        conn.close()
        root.destroy()


# =========================
# GUI SETUP
# =========================

root = tk.Tk()
root.title("Directory Manager")
root.geometry("650x580")
root.configure(bg="#F4ECF7")
root.protocol("WM_DELETE_WINDOW", exit_app)

# =========================
# LIGHT PURPLE PALETTE
# =========================

BG_COLOR = "#F4ECF7"  # Soft Light Purple Background
TITLE_COLOR = "#512E5F"  # Deep Purple
LABEL_COLOR = "#6C3483"  # Medium Dark Purple
ENTRY_BG = "#FFFFFF"

ADD_COLOR = "#8E44AD"  # Vibrant Purple
UPDATE_COLOR = "#AF7AC5"  # Soft Violet
DELETE_COLOR = "#C0392B"  # Muted Red
CLEAR_COLOR = "#A6ACAF"  # Neutral Grey
EXIT_COLOR = "#34495E"  # Dark Slate Blue/Grey

BUTTON_TEXT = "white"

# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="Song Artist Information",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR,
)
title_label.pack(pady=15)

# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
input_frame.pack(pady=5, padx=20, fill="x")

# NAME INPUT
tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR,
).grid(row=0, column=0, padx=10, pady=5, sticky="e")

name_entry = tk.Entry(
    input_frame,
    width=40,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1,
)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# AGE INPUT
tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR,
).grid(row=1, column=0, padx=10, pady=5, sticky="e")

age_entry = tk.Entry(
    input_frame,
    width=40,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1,
)
age_entry.grid(row=1, column=1, padx=10, pady=5)

# GENRE INPUT
tk.Label(
    input_frame,
    text="Genre:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR,
).grid(row=2, column=0, padx=10, pady=5, sticky="e")

genre_entry = tk.Entry(
    input_frame,
    width=40,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1,
)
genre_entry.grid(row=2, column=1, padx=10, pady=8)

# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Add",
    width=10,
    font=("Arial", 10, "bold"),
    bg=ADD_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#76448A",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=add_record,
).grid(row=0, column=0, padx=4)

tk.Button(
    button_frame,
    text="Update",
    width=10,
    font=("Arial", 10, "bold"),
    bg=UPDATE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#9B59B6",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=update_record,
).grid(row=0, column=1, padx=4)

tk.Button(
    button_frame,
    text="Delete",
    width=10,
    font=("Arial", 10, "bold"),
    bg=DELETE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#922B21",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=delete_record,
).grid(row=0, column=2, padx=4)

tk.Button(
    button_frame,
    text="Clear",
    width=10,
    font=("Arial", 10, "bold"),
    bg=CLEAR_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#7F8C8D",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=clear_fields,
).grid(row=0, column=3, padx=4)

tk.Button(
    button_frame,
    text="Exit",
    width=10,
    font=("Arial", 10, "bold"),
    bg=EXIT_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#2C3E50",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=exit_app,
).grid(row=0, column=4, padx=4)

# =========================
# TREEVIEW STYLE
# =========================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    background="#6C3483",
    foreground="white",
    font=("Arial", 10, "bold"),
    padding=8,
)

style.configure(
    "Treeview",
    background="white",
    foreground="#212121",
    rowheight=30,
    fieldbackground="white",
    font=("Arial", 10),
)

style.map(
    "Treeview",
    background=[("selected", "#BB8FCE")],
    foreground=[("selected", "black")],
)

# =========================
# TABLE
# =========================

tree = ttk.Treeview(
    root, columns=("Name", "Age", "Genre"), show="headings"
)

tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Genre", text="Genre")

tree.column("Name", width=200, anchor="w")
tree.column("Age", width=120, anchor="w")
tree.column("Genre", width=200, anchor="w")

tree.tag_configure("evenrow", background="#F5EEF8")
tree.tag_configure("oddrow", background="#E8DAEF")

tree.pack(fill="both", expand=True, padx=20, pady=10)

# =========================
# EVENTS & INITIALIZATION
# =========================

tree.bind("<<TreeviewSelect>>", select_record)

display_records()

root.mainloop()
