import tkinter as tk
from tkinter import messagebox, simpledialog

FILE_PATH = "Assessment 1 - Skills Portfolio\A1 - Resources\studentMarks.txt"


# ------------------ DATA HANDLING ------------------

def load_students():
    """Safely load students from file, skipping blank or invalid lines."""
    students = []
    try:
        with open(FILE_PATH, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

            if len(lines) < 2:
                return []

            # Skip first line (student count)
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) != 6:
                    continue  # skip bad lines

                try:
                    sid = int(parts[0])
                    name = parts[1]
                    c1, c2, c3 = map(int, parts[2:5])
                    exam = int(parts[5])
                except:
                    continue  # skip malformed rows

                students.append({
                    "id": sid,
                    "name": name,
                    "cw": c1 + c2 + c3,
                    "exam": exam
                })

        return students

    except FileNotFoundError:
        messagebox.showerror("Error", f"{FILE_PATH} not found.\n\n")
        return []


def save_students(students):
    """Save students to the file, breaking coursework back into 3 marks."""
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
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    )


# ------------------ GUI ------------------

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")

        self.students = load_students()

        self.output_box = tk.Text(root, width=65, height=30)
        self.output_box.grid(row=0, column=1, padx=10, sticky="n")

        menu_frame = tk.Frame(root)
        menu_frame.grid(row=0, column=0, padx=10, pady=10)

        buttons = [
            ("1. View all records", self.view_all),
            ("2. View individual", self.view_individual),
            ("3. Highest score", self.show_highest),
            ("4. Lowest score", self.show_lowest),
            ("5. Sort records", self.sort_records),
            ("6. Add record", self.add_record),
            ("7. Delete record", self.delete_record),
            ("8. Update record", self.update_record)
        ]

        for text, cmd in buttons:
            tk.Button(menu_frame, text=text, width=22, command=cmd).pack(pady=5)

    # ------------------ Utility ------------------

    def clear_output(self):
        self.output_box.delete("1.0", tk.END)

    # ------------------ Menu Functions ------------------

    def view_all(self):
        self.clear_output()

        # SAFETY CHECK - prevents ZeroDivisionError
        if len(self.students) == 0:
            self.output_box.insert(tk.END, "❌ No students loaded.\n\n")
            self.output_box.insert(tk.END,)
            return

        total_percentage = 0

        for s in self.students:
            self.output_box.insert(tk.END, student_to_string(s))
            total_percentage += calculate_percentage(s["cw"], s["exam"])

        avg = round(total_percentage / len(self.students), 2)

        self.output_box.insert(tk.END, f"\nTotal Students: {len(self.students)}")
        self.output_box.insert(tk.END, f"\nAverage Percentage: {avg}%\n")

    def view_individual(self):
        sid = simpledialog.askinteger("Find Student", "Enter student ID:", parent=self.root)
        if sid is None:
            return

        for s in self.students:
            if s["id"] == sid:
                self.clear_output()
                self.output_box.insert(tk.END, student_to_string(s))
                return

        messagebox.showinfo("Not Found", "Student ID not found.", parent=self.root)

    def show_highest(self):
        if not self.students:
            return

        best = max(self.students, key=lambda s: calculate_percentage(s["cw"], s["exam"]))
        self.clear_output()
        self.output_box.insert(tk.END, student_to_string(best))

    def show_lowest(self):
        if not self.students:
            return

        worst = min(self.students, key=lambda s: calculate_percentage(s["cw"], s["exam"]))
        self.clear_output()
        self.output_box.insert(tk.END, student_to_string(worst))

    def sort_records(self):
        if not self.students:
            return

        asc = messagebox.askyesno("Sort", "Sort ascending?\nNo = descending")

        self.students.sort(
            key=lambda s: calculate_percentage(s["cw"], s["exam"]),
            reverse=not asc
        )

        self.view_all()

    def add_record(self):
        try:
            sid = simpledialog.askinteger("Add", "Enter student ID:", parent=self.root)
            if sid is None:
                return
            
            name = simpledialog.askstring("Add", "Enter student name:", parent=self.root)
            if not name:
                return
            
            c1 = simpledialog.askinteger("CW", "Coursework 1 (0–20):", parent=self.root)
            if c1 is None:
                return
            
            c2 = simpledialog.askinteger("CW", "Coursework 2 (0–20):", parent=self.root)
            if c2 is None:
                return
            
            c3 = simpledialog.askinteger("CW", "Coursework 3 (0–20):", parent=self.root)
            if c3 is None:
                return
            
            exam = simpledialog.askinteger("Exam", "Exam mark (0–100):", parent=self.root)
            if exam is None:
                return
            
        except:
            return

        self.students.append({
            "id": sid,
            "name": name,
            "cw": c1 + c2 + c3,
            "exam": exam
        })

        save_students(self.students)
        self.view_all()

    def delete_record(self):
        sid = simpledialog.askinteger("Delete", "Enter student ID:")
        if sid is None:
            return

        for s in self.students:
            if s["id"] == sid:
                self.students.remove(s)
                save_students(self.students)
                self.view_all()
                return

        messagebox.showinfo("Not Found", "Student ID not found.")

    def update_record(self):
        sid = simpledialog.askinteger("Update", "Enter student ID:")
        if sid is None:
            return

        for s in self.students:
            if s["id"] == sid:
                field = simpledialog.askstring("Update", "What do you want to update? (name / cw / exam)")

                if not field:
                    return

                field = field.lower().strip()

                if field == "name":
                    newname = simpledialog.askstring("Update", "Enter new name:")
                    if newname:
                        s["name"] = newname

                elif field == "cw":
                    c1 = simpledialog.askinteger("CW", "Coursework 1 (0–20):")
                    c2 = simpledialog.askinteger("CW", "Coursework 2 (0–20):")
                    c3 = simpledialog.askinteger("CW", "Coursework 3 (0–20):")
                    s["cw"] = c1 + c2 + c3

                elif field == "exam":
                    newexam = simpledialog.askinteger("Update", "Enter new exam mark (0–100):")
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
app = StudentManager(root)
root.mainloop()