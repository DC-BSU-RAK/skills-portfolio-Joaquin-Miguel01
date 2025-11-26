import tkinter as tk
from tkinter import messagebox, simpledialog

FILE_PATH = "Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt"


# ------------------ DATA HANDLING ------------------

def load_students():
    students = []
    try:
        with open(FILE_PATH, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

            if len(lines) < 2:
                return []

            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) != 6:
                    continue
                try:
                    sid = int(parts[0])
                    name = parts[1]
                    c1, c2, c3 = map(int, parts[2:5])
                    exam = int(parts[5])
                except:
                    continue

                students.append({
                    "id": sid,
                    "name": name,
                    "cw": c1 + c2 + c3,
                    "exam": exam
                })

        return students

    except FileNotFoundError:
        messagebox.showerror("Error", f"{FILE_PATH} not found.")
        return []


def save_students(students):
    with open(FILE_PATH, "w") as file:
        file.write(str(len(students)) + "\n")
        for s in students:
            c1 = s["cw"] // 3
            c2 = s["cw"] // 3
            c3 = s["cw"] - c1 - c2
            file.write(f"{s['id']},{s['name']},{c1},{c2},{c3},{s['exam']}\n")


# ------------------ CALCULATIONS ------------------

def calculate_percentage(cw, exam):
    return round((cw + exam) / 160 * 100, 2)


def grade_from_percentage(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"


def student_to_string(s):
    percentage = calculate_percentage(s["cw"], s["exam"])
    grade = grade_from_percentage(percentage)
    return (
        f"Name: {s['name']}\n"
        f"ID: {s['id']}\n"
        f"Coursework Total: {s['cw']} / 60\n"
        f"Exam Mark: {s['exam']} / 100\n"
        f"Overall %: {percentage}%\n"
        f"Grade: {grade}\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
    )


# ------------------ GUI ------------------

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")

        # ------------------ THEMES ------------------
        self.light_theme = {
            "bg_main": "#7034BC",
            "bg_menu": "#A05CFF",
            "text_bg": "#EDE3FF",
            "button": "#8A47D6",
            "button_hover": "#B56BFF",
            "fg": "#1A001F"
        }

        self.dark_theme = {
            "bg_main": "#2B0033",
            "bg_menu": "#1A001F",
            "text_bg": "#3A0B4A",
            "button": "#4B0082",
            "button_hover": "#FF3366",
            "fg": "white"
        }

        self.current_theme = "light"

        self.students = load_students()

        # Create frames & widgets first
        self.menu_frame = tk.Frame(root)
        self.output_box = tk.Text(root, width=65, height=30, bd=2, relief="groove", font=("Segoe UI", 11))

        self.output_box.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10)

        # Buttons list
        self.buttons = []
        buttons_info = [
            ("1. View all records", self.view_all),
            ("2. View individual", self.view_individual),
            ("3. Highest score", self.show_highest),
            ("4. Lowest score", self.show_lowest),
            ("5. Sort records", self.sort_records),
            ("6. Add record", self.add_record),
            ("7. Delete record", self.delete_record),
            ("8. Update record", self.update_record)
        ]

        for text, cmd in buttons_info:
            b = tk.Button(self.menu_frame, text=text, command=cmd, width=22, font=("Segoe UI", 10, "bold"))
            b.pack(pady=10)
            self.buttons.append(b)

        # Dark Mode Toggle Button
        self.theme_button = tk.Button(self.menu_frame, text="Dark Mode", command=self.toggle_theme, width=22)
        self.theme_button.pack(pady=10)
        self.buttons.append(self.theme_button)

        # Apply starting theme
        self.apply_theme()

    # ------------------ THEME CONTROL ------------------

    def apply_theme(self):
        theme = self.dark_theme if self.current_theme == "dark" else self.light_theme

        # Window + frames
        self.root.configure(bg=theme["bg_main"])
        self.menu_frame.configure(bg=theme["bg_menu"])

        # Text box
        self.output_box.configure(
            bg=theme["text_bg"], fg=theme["fg"], insertbackground=theme["fg"]
        )

        # Buttons (with hover)
        for button in self.buttons:
            button.configure(
                bg=theme["button"],
                fg=theme["fg"],
                activebackground=theme["button_hover"]
            )
            # Reset hover events each time
            button.bind("<Enter>", lambda e, b=button, t=theme: b.config(bg=t["button_hover"]))
            button.bind("<Leave>", lambda e, b=button, t=theme: b.config(bg=t["button"]))

        # Update theme button text
        if self.current_theme == "light":
            self.theme_button.config(text="🌙 Dark Mode")
        else:
            self.theme_button.config(text="☀️ Light Mode")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    # ------------------ Utility ------------------

    def clear_output(self):
        self.output_box.delete("1.0", tk.END)

    # ------------------ Menu Functions ------------------
    def view_all(self):
        self.clear_output()
        if not self.students:
            self.output_box.insert(tk.END, "❌ No students loaded.\n\n")
            return

        total = 0
        for s in self.students:
            self.output_box.insert(tk.END, student_to_string(s))
            total += calculate_percentage(s["cw"], s["exam"])

        avg = round(total / len(self.students), 2)
        self.output_box.insert(tk.END, f"\nTotal Students: {len(self.students)}")
        self.output_box.insert(tk.END, f"\nAverage Percentage: {avg}%\n")

    def view_individual(self):
        sid = simpledialog.askinteger("Find Student", "Enter student ID:")
        if sid is None: return

        for s in self.students:
            if s["id"] == sid:
                self.clear_output()
                self.output_box.insert(tk.END, student_to_string(s))
                return

        messagebox.showinfo("Not Found", "Student ID not found.")

    def show_highest(self):
        if not self.students: return
        best = max(self.students, key=lambda s: calculate_percentage(s["cw"], s["exam"]))
        self.clear_output()
        self.output_box.insert(tk.END, student_to_string(best))

    def show_lowest(self):
        if not self.students: return
        worst = min(self.students, key=lambda s: calculate_percentage(s["cw"], s["exam"]))
        self.clear_output()
        self.output_box.insert(tk.END, student_to_string(worst))

    def sort_records(self):
        if not self.students: return
        asc = messagebox.askyesno("Sort", "Sort ascending?\nNo = descending")
        self.students.sort(
            key=lambda s: calculate_percentage(s["cw"], s["exam"]),
            reverse=not asc
        )
        self.view_all()

    def add_record(self):
        try:
            sid = simpledialog.askinteger("Add", "Enter student ID:", parent=self.root)
            if sid is None: return

            name = simpledialog.askstring("Add", "Enter student name:", parent=self.root)
            if not name: return

            c1 = simpledialog.askinteger("CW1 (0–20)",  "Coursework 1 (0–20):", parent=self.root)
            c2 = simpledialog.askinteger("CW2 (0–20)", "Coursework 1 (0–20):", parent=self.root)
            c3 = simpledialog.askinteger("CW3 (0–20)" "Coursework 1 (0–20):", parent=self.root)
            exam = simpledialog.askinteger("Exam", "Enter exam mark (0–100):", parent=self.root)

        except:
            return

        self.students.append({
            "id": sid, "name": name, "cw": c1+c2+c3, "exam": exam
        })

        save_students(self.students)
        self.view_all()

    def delete_record(self):
        sid = simpledialog.askinteger("Delete", "Enter student ID:")
        if sid is None: return
        for s in self.students:
            if s["id"] == sid:
                self.students.remove(s)
                save_students(self.students)
                self.view_all()
                return
        messagebox.showinfo("Not Found", "Student ID not found.")

    def update_record(self):
        sid = simpledialog.askinteger("Update", "Enter student ID:")
        if sid is None: return

        for s in self.students:
            if s["id"] == sid:
                field = simpledialog.askstring("Field", "Update name / cw / exam:")
                if not field: return
                field = field.lower()

                if field == "name":
                    newname = simpledialog.askstring("Name", "New name:")
                    if newname: s["name"] = newname

                elif field == "cw":
                    c1 = simpledialog.askinteger("CW1", "Enter CW1:")
                    c2 = simpledialog.askinteger("CW2", "Enter CW2:")
                    c3 = simpledialog.askinteger("CW3", "Enter CW3:")
                    s["cw"] = c1 + c2 + c3

                elif field == "exam":
                    newexam = simpledialog.askinteger("Exam", "New exam (0-100):")
                    if newexam is not None:
                        s["exam"] = newexam
                else:
                    messagebox.showerror("Error", "Invalid field.")
                    return

                save_students(self.students)
                self.view_all()
                return

        messagebox.showinfo("Not Found", "Student ID not found.")


# ------------------ MAIN ------------------

root = tk.Tk()

try:
    icon = tk.PhotoImage(file="Exercise 3-Student Data/student.png")
    root.iconphoto(True, icon)
except Exception as e:
    print("Icon not loaded:", e)
app = StudentManager(root)
root.mainloop()
