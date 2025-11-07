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



if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
