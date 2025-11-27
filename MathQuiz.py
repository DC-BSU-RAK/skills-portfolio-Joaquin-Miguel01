import tkinter as tk
from tkinter import messagebox
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

        # NEW: Instructions button
        tk.Button(self.menu_frame, text="Instructions", font=("Arial", 16),
                  command=self.show_instructions).pack(pady=10)

    def show_instructions(self):
        """Show instructions *inside* the background image"""

        # Hide the menu
        self.menu_frame.place_forget()

        # Create instruction frame centered on image
        self.instructions_frame = tk.Frame(self.root, bg="white", bd=5)
        self.instructions_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.instructions_frame, text="Instructions",
                 font=("Arial", 22, "bold"), bg="white").pack(pady=10)

        instructions = (
            "1. Select a difficulty level (Easy, Moderate, Advanced).\n"
            "2. You will be given 10 math questions.\n"
            "3. Type your answer and click Submit.\n"
            "4. You get 2 attempts per question:\n"
            "       • 1st attempt correct = 10 points\n"
            "       • 2nd attempt correct = 5 points\n"
            "       • 3nd wrong attempt = 0 points\n"
            "5. If both attempts are wrong, the correct answer is shown.\n"
            "6. After 10 questions, you get a final score and grade.\n"
            "7. You can choose to play again or exit."
        )

        tk.Label(self.instructions_frame, text=instructions,
                 font=("Arial", 14), bg="white", justify="left").pack(padx=20, pady=10)

        # Back Button to return to the main menu
        tk.Button(self.instructions_frame, text="Back", font=("Arial", 14),
                  command=self.back_to_menu).pack(pady=20)

    def back_to_menu(self):
        """Return to difficulty menu from instructions"""
        self.instructions_frame.destroy()

        self.menu_frame = tk.Frame(self.root, bg="white", bd=5)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.display_menu()

    def start_quiz(self, difficulty):
        """Initialize quiz based on chosen difficulty"""
        self.difficulty = difficulty
        self.menu_frame.destroy()  # Remove menu screen

        # Reset values
        self.score = 0
        self.question_count = 0
        self.attempt = 1

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

    def check_answer(self):
        try:
            user_answer = float(self.answer_entry.get())

            if self.operator == '+':
                correct_answer = self.num1 + self.num2
            elif self.operator == '-':
                correct_answer = self.num1 - self.num2

            # Correct answer
            if abs(user_answer - correct_answer) < 0.01:
                points = 10 if self.attempt == 1 else 5
                self.score += points
                self.result_label.config(text=f"Correct! You earned {points} points.", fg="green")
                self.score_label.config(text=f"Score: {self.score}")

                self.question_count += 1
                self.answer_entry.delete(0, tk.END)

                if self.question_count < 10:
                    self.generate_question()
                else:
                    self.end_quiz()

            else:
                if self.attempt == 1:
                    self.attempt = 2
                    self.result_label.config(text="Wrong! Try again for 5 points.", fg="orange")
                    self.answer_entry.delete(0, tk.END)
                else:
                    self.result_label.config(
                        text=f"Wrong again! The correct answer was {correct_answer}. Moving to next question.",
                        fg="red"
                    )
                    self.answer_entry.delete(0, tk.END)
                    self.question_count += 1
                    if self.question_count < 10:
                        self.generate_question()
                    else:
                        self.end_quiz()
                    self.attempt = 1

        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")
            self.answer_entry.delete(0, tk.END)

    def end_quiz(self):
        """End of quiz prompt with grade"""
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"

        self.result_label.config(text=f"Quiz over! Final score: {self.score} | Grade: {grade}", fg="blue")
        self.submit_button.config(state=tk.DISABLED)

        play_again = messagebox.askyesno("Play?", "Quiz over! Would you like to play again?")
        if play_again:
            self.frame.destroy()
            self.menu_frame = tk.Frame(self.root, bg="white", bd=5)
            self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.display_menu()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("logo.ico")
    app = MathQuizApp(root)
    root.mainloop()