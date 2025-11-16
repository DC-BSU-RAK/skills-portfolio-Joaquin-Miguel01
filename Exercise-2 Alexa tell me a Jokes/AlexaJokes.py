import tkinter as tk
import random
from PIL import Image, ImageTk, ImageSequence

# --- JOKES LIST ---
jokes = [
    "Why did the chicken cross the road?To get to the other side.",
    "What happens if you boil a clown?You get a laughing stock.",
    "Why did the car get a flat tire?Because there was a fork in the road!",
    "How did the hipster burn his mouth?He ate his pizza before it was cool.",
    "What did the janitor say when he jumped out of the closet?SUPPLIES!!!!",
    "Have you heard about the band 1023MB?It's probably because they haven't got a gig yet…",
    "Why does the golfer wear two pants?Because he's afraid he might get a 'Hole-in-one.'",
    "Why should you wear glasses to maths class?Because it helps with division.",
    "Why does it take pirates so long to learn the alphabet?Because they could spend years at C.",
    "Why did the woman go on the date with the mushroom?Because he was a fun-ghi.",
    "Why do bananas never get lonely?Because they hang out in bunches.",
    "What did the buffalo say when his kid went to college?Bison.",
    "Why shouldn't you tell secrets in a cornfield?Too many ears.",
    "What do you call someone who doesn't like carbs?Lack-Toast Intolerant.",
    "Why did the can crusher quit his job?Because it was soda pressing.",
    "Why did the birthday boy wrap himself in paper?He wanted to live in the present.",
    "What does a house wear?A dress.",
    "Why couldn't the toilet paper cross the road?Because it got stuck in a crack.",
    "Why didn't the bike want to go anywhere?Because it was two-tired!",
    "Want to hear a pizza joke?Nahhh, it's too cheesy!",
    "Why are chemists great at solving problems?Because they have all of the solutions!",
    "Why is it impossible to starve in the desert?Because of all the sand which is there!",
    "What did the cheese say when it looked in the mirror?Halloumi!",
    "Why did the developer go broke?Because he used up all his cache.",
    "Did you know that ants are the only animals that don't get sick?It's true! It's because they have little antibodies.",
    "Why did the donut go to the dentist?To get a filling.",
    "What do you call a bear with no teeth?A gummy bear!",
    "What does a vegan zombie like to eat?Graaains.",
    "What do you call a dinosaur with only one eye?A Do-you-think-he-saw-us!",
    "Why should you never fall in love with a tennis player?Because to them... love means NOTHING!",
    "What did the full glass say to the empty glass?You look drunk.",
    "What's a potato's favorite form of transportation?The gravy train.",
    "What did one ocean say to the other?Nothing, they just waved.",
    "What did the right eye say to the left eye?Honestly, between you and me something smells.",
    "What do you call a dog that's been run over by a steamroller?Spot!",
    "What's the difference between a hippo and a zippo?One's pretty heavy and the other's a little lighter.",
    "Why don't scientists trust Atoms?They make up everything."
]

current_joke = ""
animation_running = False  # CODE TO CONTROL THE ANIMATION

def show_joke(joke):
    if '?' in joke:
        setup = joke.split('?', 1)[0] + '?'
    else:
        setup = joke
    joke_label.config(text=setup)
    punchline_label.config(text="")

def tell_joke():
    global current_joke, animation_running
    animation_running = False  # STOP ANIMATION
    current_joke = random.choice(jokes)
    show_joke(current_joke)

def reveal_joke():
    global animation_running
    if current_joke:
        if '?' in current_joke:
            punchline = current_joke.split('?', 1)[1]
            punchline_label.config(text=punchline)
        else:
            punchline_label.config(text=current_joke)
        animation_running = True
        animate_sticker()  # START ANIMATION
    else:
        punchline_label.config(text="Click 'Tell me a joke' first!")

def next_joke():
    global current_joke, animation_running
    animation_running = False  # STOP ANIMATION
    new_joke = random.choice(jokes)
    while new_joke == current_joke and len(jokes) > 1:
        new_joke = random.choice(jokes)
    current_joke = new_joke
    show_joke(current_joke)

# --- ROOT WINDOW ---
root = tk.Tk()
root.title("Alexa tell me a joke")
root.geometry("600x440")

# --- JOKE LABELS ---
joke_label = tk.Label(root, text="Click 'Tell me a joke' to start!", wraplength=500, font=("Arial", 14))
joke_label.pack(pady=10)

punchline_label = tk.Label(root, text="", wraplength=500, font=("Arial", 14, "bold"), fg="blue")
punchline_label.pack(pady=5)

# --- BUTTONS ---
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

root.mainloop()