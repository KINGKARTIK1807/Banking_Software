import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('banking.db')
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    balance REAL
)''')

# Function to clear entry fields
def clear_entries():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Function to perform user registration
def register():
    username = username_entry.get()
    password = password_entry.get()
    try:
        c.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, 0)', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
        clear_entries()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

# Function to perform user login
def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    if (user := c.fetchone()):
        current_user = user[0]
        messagebox.showinfo("Success", "Login successful")
        clear_entries()
        show_main_menu()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to show the main menu after successful login
def show_main_menu():
    main_menu_frame.pack(fill=tk.BOTH, expand=True)
    login_frame.pack_forget()

# Function to check balance
def check_balance():
    c.execute('SELECT balance FROM users WHERE username=?', (current_user,))
    balance = c.fetchone()[0]
    messagebox.showinfo("Balance", f"Your balance is ${balance:.2f}")

# Function to deposit money
def deposit():
    amount = float(amount_entry.get())
    c.execute('UPDATE users SET balance=balance+? WHERE username=?', (amount, current_user))
    conn.commit()
    messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")
    clear_entries()

# Function to withdraw money
def withdraw():
    amount = float(amount_entry.get())
    c.execute('SELECT balance FROM users WHERE username=?', (current_user,))
    balance = c.fetchone()[0]
    if amount <= balance:
        c.execute('UPDATE users SET balance=balance-? WHERE username=?', (amount, current_user))
        conn.commit()
        messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully")
    else:
        messagebox.showerror("Error", "Insufficient funds")
    clear_entries()

# Main application window
root = tk.Tk()
root.title("Banking Software")

# Frames
login_frame = tk.Frame(root)
main_menu_frame = tk.Frame(root)

# Login frame widgets
tk.Label(login_frame, text="Username:").pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()
tk.Label(login_frame, text="Password:").pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()
tk.Button(login_frame, text="Login", command=login).pack()
tk.Button(login_frame, text="Register", command=register).pack()

# Main menu frame widgets
tk.Button(main_menu_frame, text="Check Balance", command=check_balance).pack()
tk.Label(main_menu_frame, text="Amount:").pack()
amount_entry = tk.Entry(main_menu_frame)
amount_entry.pack()
tk.Button(main_menu_frame, text="Deposit", command=deposit).pack()
tk.Button(main_menu_frame, text="Withdraw", command=withdraw).pack()

# Packing frames
login_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()

# Close the database connection
conn.close()