# ==========================================
# Advanced Password Generator - Python Project
# ==========================================

import random
import string
import tkinter as tk
from tkinter import messagebox


class PasswordGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("500x420")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        # Heading
        heading = tk.Label(
            root,
            text="Secure Password Generator",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        heading.pack(pady=20)

        # Password Length
        tk.Label(
            root,
            text="Password Length",
            font=("Arial", 12, "bold"),
            bg="#1e1e2f",
            fg="white"
        ).pack()

        self.length_entry = tk.Entry(
            root,
            font=("Arial", 14),
            justify="center",
            width=10
        )
        self.length_entry.pack(pady=10)

        # Options Frame
        option_frame = tk.Frame(root, bg="#1e1e2f")
        option_frame.pack(pady=10)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)

        tk.Checkbutton(
            option_frame,
            text="Uppercase",
            variable=self.upper_var,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#1e1e2f",
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Checkbutton(
            option_frame,
            text="Lowercase",
            variable=self.lower_var,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#1e1e2f",
            font=("Arial", 10)
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Checkbutton(
            option_frame,
            text="Numbers",
            variable=self.number_var,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#1e1e2f",
            font=("Arial", 10)
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Checkbutton(
            option_frame,
            text="Symbols",
            variable=self.symbol_var,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#1e1e2f",
            font=("Arial", 10)
        ).grid(row=1, column=1, padx=10, pady=5)

        # Generate Button
        generate_btn = tk.Button(
            root,
            text="Generate Password",
            font=("Arial", 13, "bold"),
            bg="#00b894",
            fg="white",
            padx=10,
            pady=5,
            command=self.generate_password
        )
        generate_btn.pack(pady=20)

        # Result Box
        self.password_box = tk.Entry(
            root,
            font=("Consolas", 16, "bold"),
            justify="center",
            width=30,
            bd=3
        )
        self.password_box.pack(pady=10)

        # Copy Button
        copy_btn = tk.Button(
            root,
            text="Copy Password",
            font=("Arial", 11, "bold"),
            bg="#0984e3",
            fg="white",
            command=self.copy_password
        )
        copy_btn.pack(pady=10)

    def generate_password(self):

        try:
            length = int(self.length_entry.get())

            if length < 4:
                messagebox.showwarning(
                    "Invalid Length",
                    "Password length should be at least 4"
                )
                return

            characters = ""

            if self.upper_var.get():
                characters += string.ascii_uppercase

            if self.lower_var.get():
                characters += string.ascii_lowercase

            if self.number_var.get():
                characters += string.digits

            if self.symbol_var.get():
                characters += string.punctuation

            if characters == "":
                messagebox.showerror(
                    "Selection Error",
                    "Select at least one option"
                )
                return

            password = "".join(random.choice(characters) for _ in range(length))

            self.password_box.delete(0, tk.END)
            self.password_box.insert(0, password)

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Enter a valid number"
            )

    def copy_password(self):

        password = self.password_box.get()

        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard"
            )


# Main Program
root = tk.Tk()
app = PasswordGenerator(root)
root.mainloop()