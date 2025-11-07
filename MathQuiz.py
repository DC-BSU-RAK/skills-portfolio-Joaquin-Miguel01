import tkinter as tk
from PIL import Image, ImageTk
import random

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("800x600")

        # Load original image
        self.original_image = Image.open("chalkboard.png")
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Background label
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Update background when window resizes
        self.root.bind("<Configure>", self.resize_bg)

        # Variables
        self.score = 0
        self.question_count = 0
        self.attempt = 1
        self.difficulty = None  # Will store chosen difficulty

        # Create menu frame (shown first)
        self.menu_frame = tk.Frame(root, bg="white", bd=5)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.display_menu()

    def resize_bg(self, event):
        """Dynamically resize background image when window changes size"""
        new_width = event.width
        new_height = event.height
        resized = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_image)
        self.bg_label.image = self.bg_image

    def display_menu(self):
        """Show difficulty selection menu"""
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        tk.Label(self.menu_frame, text="Select Difficulty", font=("Arial", 20), bg="white").pack(pady=20)

        tk.Button(self.menu_frame, text="1. Easy", font=("Arial", 16),
                  command=lambda: self.start_quiz("Easy")).pack(pady=10)

        tk.Button(self.menu_frame, text="2. Moderate", font=("Arial", 16),
                  command=lambda: self.start_quiz("Moderate")).pack(pady=10)

        tk.Button(self.menu_frame, text="3. Advanced", font=("Arial", 16),
                  command=lambda: self.start_quiz("Advanced")).pack(pady=10)
        
    def start_quiz(self, difficulty):
        """Initialize quiz based on chosen difficulty"""
        self.difficulty = difficulty
        self.menu_frame.destroy()  # Remove menu screen

        # Create main content frame
        self.frame = tk.Frame(self.root, bg="white", bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # UI elements
        self.score_label = tk.Label(self.frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.difficulty_label = tk.Label(self.frame, text=f"Difficulty: {difficulty}", font=("Arial", 12), fg="black")
        self.difficulty_label.pack(pady=5)

        self.question_label = tk.Label(self.frame, text="", font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(self.frame, text="Submit", font=("Arial", 14), command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.generate_question()

    def generate_question(self):
        """Generate a new math question based on difficulty"""
        if self.difficulty == "Easy":
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
            self.operator = random.choice(['+', '-'])

        elif self.difficulty == "Moderate":
            self.num1 = random.randint(10, 50)
            self.num2 = random.randint(10, 50)
            self.operator = random.choice(['+', '-'])

        else:  # Advanced
            self.num1 = random.randint(1000, 9999)
            self.num2 = random.randint(1000, 9999)
            self.operator = random.choice(['+', '-'])

        self.attempt = 1
        self.update_question_label()

    def update_question_label(self):
        """Update the question label"""
        question_number = self.question_count + 1
        self.question_label.config(
            text=f"{question_number}) {self.num1} {self.operator} {self.num2}?"
        )
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
