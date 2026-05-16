import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

FILE_NAME = "tasks.json"


class TodoApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart To-Do List")
        self.root.geometry("850x500")

        self.tasks = []

        self.load_tasks()

        # ================= TOP FRAME =================
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Task").grid(row=0, column=0, padx=5)

        self.task_entry = tk.Entry(top_frame, width=25)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Priority").grid(row=0, column=2, padx=5)

        self.priority = ttk.Combobox(
            top_frame,
            values=["High", "Medium", "Low"],
            width=10,
            state="readonly"
        )

        self.priority.grid(row=0, column=3, padx=5)
        self.priority.current(1)

        tk.Label(
            top_frame,
            text="Deadline (YYYY-MM-DD)"
        ).grid(row=0, column=4, padx=5)

        self.deadline_entry = tk.Entry(top_frame, width=15)
        self.deadline_entry.grid(row=0, column=5, padx=5)

        # ================= DATE =================
        tk.Label(
            root,
            text="Today's Date : " +
            datetime.now().strftime("%Y-%m-%d"),
            font=("Arial", 10, "bold")
        ).pack()

        # ================= BUTTONS =================
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Task",
            width=12,
            command=self.add_task
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update Task",
            width=12,
            command=self.update_task
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Delete Task",
            width=12,
            command=self.delete_task
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            text="Complete Task",
            width=12,
            command=self.complete_task
        ).grid(row=0, column=3, padx=5)

        # ================= TREEVIEW =================
        self.tree = ttk.Treeview(
            root,
            columns=("Task", "Priority", "Deadline", "Status"),
            show="headings"
        )

        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Status", text="Status")

        self.tree.column("Task", width=300)
        self.tree.column("Priority", width=100)
        self.tree.column("Deadline", width=150)
        self.tree.column("Status", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ================= COLORS =================
        self.tree.tag_configure("high", background="lightcoral")
        self.tree.tag_configure("medium", background="lightyellow")
        self.tree.tag_configure("low", background="lightblue")
        self.tree.tag_configure("done", background="lightgreen")
        self.tree.tag_configure("overdue", background="orange")

        # ================= SELECT EVENT =================
        self.tree.bind("<<TreeviewSelect>>", self.select_task)

        self.refresh()

    # ================= ADD TASK =================
    def add_task(self):

        task = self.task_entry.get().strip()
        priority = self.priority.get()
        deadline = self.deadline_entry.get().strip()

        if task == "":
            messagebox.showwarning(
                "Warning",
                "Task cannot be empty"
            )
            return

        # Date validation
        if deadline != "":
            try:
                datetime.strptime(deadline, "%Y-%m-%d")

            except:
                messagebox.showerror(
                    "Error",
                    "Date format must be YYYY-MM-DD"
                )
                return

        new_task = {
            "task": task,
            "priority": priority,
            "deadline": deadline,
            "completed": False
        }

        self.tasks.append(new_task)

        self.save_tasks()
        self.refresh()
        self.clear_fields()

    # ================= UPDATE TASK =================
    def update_task(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a task to update"
            )
            return

        index = self.tree.index(selected[0])

        task = self.task_entry.get().strip()
        priority = self.priority.get()
        deadline = self.deadline_entry.get().strip()

        if task == "":
            messagebox.showwarning(
                "Warning",
                "Task cannot be empty"
            )
            return

        self.tasks[index]["task"] = task
        self.tasks[index]["priority"] = priority
        self.tasks[index]["deadline"] = deadline

        self.save_tasks()
        self.refresh()
        self.clear_fields()

    # ================= DELETE TASK =================
    def delete_task(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a task to delete"
            )
            return

        index = self.tree.index(selected[0])

        self.tasks.pop(index)

        self.save_tasks()
        self.refresh()
        self.clear_fields()

    # ================= COMPLETE TASK =================
    def complete_task(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a task"
            )
            return

        index = self.tree.index(selected[0])

        self.tasks[index]["completed"] = True

        self.save_tasks()
        self.refresh()

    # ================= SELECT TASK =================
    def select_task(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        index = self.tree.index(selected[0])

        task = self.tasks[index]

        self.task_entry.delete(0, tk.END)
        self.task_entry.insert(0, task["task"])

        self.priority.set(task["priority"])

        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, task["deadline"])

    # ================= REFRESH =================
    def refresh(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for t in self.tasks:

            tags = []

            status = "Pending"

            # Priority color
            if t["priority"] == "High":
                tags.append("high")

            elif t["priority"] == "Medium":
                tags.append("medium")

            elif t["priority"] == "Low":
                tags.append("low")

            # Completed task
            if t["completed"]:
                tags.append("done")
                status = "Completed"

            # Overdue check
            if t.get("deadline","") != "":

                try:
                    deadline_date = datetime.strptime(
                        t["deadline"],
                        "%Y-%m-%d"
                    ).date()

                    if (
                        deadline_date < datetime.now().date()
                        and not t["completed"]
                    ):
                        tags.append("overdue")

                except:
                    pass

            self.tree.insert(
                "",
                tk.END,
                values=(
                    t.get("task", ""),
                    t.get("priority", ""),
                    t.get("deadline", ""),
                    status
                ),
                tags=tuple(tags)
            )

    # ================= SAVE TASKS =================
    def save_tasks(self):

        try:
            with open(FILE_NAME, "w") as f:
                json.dump(self.tasks, f, indent=4)

        except:
            messagebox.showerror(
                "Error",
                "Could not save tasks"
            )

    # ================= LOAD TASKS =================
    def load_tasks(self):

        try:
            with open(FILE_NAME, "r") as f:
                self.tasks = json.load(f)

        except:
            self.tasks = []

    # ================= CLEAR FIELDS =================
    def clear_fields(self):

        self.task_entry.delete(0, tk.END)

        self.priority.current(1)

        self.deadline_entry.delete(0, tk.END)


# ================= MAIN =================
root = tk.Tk()

app = TodoApp(root)

root.mainloop()