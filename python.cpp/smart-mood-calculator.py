import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ---------------- MAIN WINDOW ---------------- #
root = tk.Tk()
root.title("Smart Mood Calculator")
root.geometry("420x650")
root.config(bg="#121212")

# ---------------- VARIABLES ---------------- #
expression = ""

# ---------------- FUNCTIONS ---------------- #

# Add value to screen
def press(value):
    global expression
    expression += str(value)
    equation.set(expression)

# Clear screen
def clear():
    global expression
    expression = ""
    equation.set("")
    mood_label.config(text="Calculator Cleared 😌", fg="cyan")

# Delete last character
def backspace():
    global expression
    expression = expression[:-1]
    equation.set(expression)

# Hover effect
def on_enter(e):
    e.widget['background'] = '#00ADB5'

def on_leave(e):
    e.widget['background'] = '#393E46'

# Calculate result
def calculate():
    global expression
    try:
        result = str(eval(expression))
        equation.set(result)

        # Save History
        history.insert(tk.END, expression + " = " + result)

        value = float(result)

        # Smart Mood Messages
        if value > 1000:
            mood_label.config(
                text="Wow! That's a huge value 😲",
                fg="orange"
            )

        elif value < 10:
            mood_label.config(
                text="Tiny but accurate 😄",
                fg="lightgreen"
            )

        else:
            mood_label.config(
                text="Perfect Calculation ✅",
                fg="cyan"
            )

        # Dynamic Colors
        if value > 0:
            entry.config(bg="#1B5E20")
        elif value < 0:
            entry.config(bg="#B71C1C")
        else:
            entry.config(bg="#37474F")

        expression = result

    except:
        equation.set("")
        expression = ""
        entry.config(bg="#B71C1C")

        mood_label.config(
            text="Invalid Operation ⚠️",
            fg="red"
        )

# Keyboard Support
def key_input(event):
    key = event.char

    if key in "0123456789+-*/.":
        press(key)

    elif key == "\r":
        calculate()

# ---------------- TITLE ---------------- #
title = tk.Label(
    root,
    text="SMART MOOD CALCULATOR",
    font=("Helvetica", 18, "bold"),
    bg="#121212",
    fg="#00FFF5"
)
title.pack(pady=10)

# ---------------- DATE & TIME ---------------- #
time_label = tk.Label(
    root,
    font=("Arial", 12),
    bg="#121212",
    fg="white"
)
time_label.pack()

def update_time():
    current = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
    time_label.config(text=current)
    root.after(1000, update_time)

update_time()

# ---------------- ENTRY BOX ---------------- #
equation = tk.StringVar()

entry = tk.Entry(
    root,
    textvariable=equation,
    font=("Arial", 24),
    bd=10,
    relief=tk.FLAT,
    justify="right",
    bg="#222831",
    fg="white",
    insertbackground="white"
)

entry.pack(fill="both", padx=15, pady=15, ipady=15)

# ---------------- MOOD LABEL ---------------- #
mood_label = tk.Label(
    root,
    text="Ready to Calculate 😎",
    font=("Arial", 12, "bold"),
    bg="#121212",
    fg="cyan"
)

mood_label.pack(pady=5)

# ---------------- BUTTON FRAME ---------------- #
frame = tk.Frame(root, bg="#121212")
frame.pack()

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '+', '=']
]

# Create Buttons
for row in buttons:
    row_frame = tk.Frame(frame, bg="#121212")
    row_frame.pack()

    for btn in row:

        if btn == "=":
            command = calculate
        else:
            command = lambda x=btn: press(x)

        button = tk.Button(
            row_frame,
            text=btn,
            width=6,
            height=2,
            font=("Arial", 18, "bold"),
            bg="#393E46",
            fg="white",
            bd=0,
            activebackground="#00ADB5",
            activeforeground="white",
            command=command
        )

        button.pack(side="left", padx=5, pady=5)

        # Hover Effects
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

# ---------------- EXTRA BUTTONS ---------------- #
extra_frame = tk.Frame(root, bg="#121212")
extra_frame.pack(pady=10)

clear_btn = tk.Button(
    extra_frame,
    text="CLEAR",
    font=("Arial", 14, "bold"),
    bg="#D32F2F",
    fg="white",
    width=10,
    command=clear
)
clear_btn.pack(side="left", padx=10)

back_btn = tk.Button(
    extra_frame,
    text="⌫ BACK",
    font=("Arial", 14, "bold"),
    bg="#FFA000",
    fg="black",
    width=10,
    command=backspace
)
back_btn.pack(side="left", padx=10)

# ---------------- HISTORY SECTION ---------------- #
history_title = tk.Label(
    root,
    text="Calculation History",
    font=("Arial", 14, "bold"),
    bg="#121212",
    fg="#00FFF5"
)
history_title.pack()

history = tk.Listbox(
    root,
    height=8,
    font=("Consolas", 12),
    bg="#1E1E1E",
    fg="lightgreen",
    bd=0
)

history.pack(fill="both", padx=15, pady=10)

# Keyboard Binding
root.bind("<Key>", key_input)

# ---------------- RUN APP ---------------- #
root.mainloop()