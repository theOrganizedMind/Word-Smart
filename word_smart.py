import random
import tkinter as tk
from tkinter import messagebox
import json

from word_dict import word_dict

# =========================================================================== #
# ================================= INFO ==================================== #
# =========================================================================== #
#
# =========================================================================== #
# ================================= TODO ==================================== #
# =========================================================================== #
# TODO: 
# =========================================================================== #

FONT = "Arial"
WORDS_TO_LEARN_FILE = "words_to_learn.json"


class WordSmartApp:
    """
    A Tkinter-based vocabulary quiz application.

    Features:
    - Displays a random word from a dictionary and asks the user to select its 
      correct definition.
    - Presents five radio button options: the correct definition and four random
      incorrect ones.
    - Checks the user's answer when "Next" is clicked, shows a toast notification
      for correct/incorrect answers,
      and automatically moves to the next word.
    - Keeps the main window size fixed and wraps long definitions in radio buttons.
    - Tracks words already shown to avoid repetition until all words are used.
    - Saves incorrectly answered words and their definitions to 'words_to_learn.json'
      for later review.

    Args:
        master (tk.Tk): The root Tkinter window.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Word Smart")
        self.master.geometry("500x450")
        self.master.resizable(False, False) # Prevent resizing
        self.word_label = tk.Label(master, font=(FONT, 16))
        self.word_label.pack(pady=20)

        self.var = tk.StringVar()
        self.radio_buttons = []
        for _ in range(5):
            rb = tk.Radiobutton(master, text="", variable=self.var, value="", 
                                font=(FONT, 12), wraplength=400, justify="left")
            rb.pack(anchor="w", padx=40)
            self.radio_buttons.append(rb)

        self.next_button = tk.Button(master, text="Next", command=self.on_next)
        self.next_button.pack(pady=20)      

        # Add button for adding word/definition for review
        self.add_frame = tk.Frame(master)
        self.add_frame.pack(pady=10)
        self.add_button = tk.Button(self.add_frame, text="Add", command=self.on_add)
        self.add_button.pack()

        self.current_word = None
        self.correct_definition = None
        self.chosen_words = [] # Store chosen keys
        self.review_mode = False
        self.words_to_review = []
        self.next_word()

    def on_add(self):
        # Add the currently displayed word and its correct definition for review
        if self.current_word and self.correct_definition:
            self.save_word_to_learn(self.current_word, self.correct_definition)
            print(f"{self.current_word}: {self.correct_definition}")
            self.show_toast("Added for Review", "purple", lambda: None)
        else:
            self.show_toast("No word to add", "orange", lambda: None)

    def save_word_to_learn(self, word, definition):
        try:
            with open(WORDS_TO_LEARN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data[word] = definition
        with open(WORDS_TO_LEARN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_words_to_review(self):
        try:
            with open(WORDS_TO_LEARN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        self.words_to_review = list(data.items())

    def remove_word_from_review(self, word):
        try:
            with open(WORDS_TO_LEARN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if word in data:
            del data[word]
        with open(WORDS_TO_LEARN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_definitions(self):
            # Get correct definition and 4 random incorrect ones
            all_defs = list(word_dict.values())
            self.correct_definition = word_dict[self.current_word]
            incorrect_defs = [d for d in all_defs if d != self.correct_definition]
            options = random.sample(incorrect_defs, 4) + [self.correct_definition]
            random.shuffle(options)

            # Set radio button options
            for rb, definition in zip(self.radio_buttons, options):
                rb.config(text=definition, value=definition)
            self.var.set("")

    def next_word(self):
        if not self.review_mode:
        # If all words have been used, switch to review mode
            if len(self.chosen_words) == len(word_dict):
                self.review_mode = True
                self.load_words_to_review()
                if self.words_to_review:
                    self.show_toast("Words to Review", "blue", self.next_word)
                else:
                    self.show_toast("All Done!", "green", lambda: None)
                return

            # Choose a random key not already chosen
            remaining_words = [w for w in word_dict.keys() if w not in self.chosen_words]
            self.current_word = random.choice(remaining_words)
            self.chosen_words.append(self.current_word)
            self.word_label.config(text=self.current_word)

            self.get_definitions()
        else:
            # Review mode: show words from words_to_learn.json
            if not self.words_to_review:
                self.show_toast("Review complete!", "green", lambda: None)
                self.word_label.config(text="No more words to review.")
                for rb in self.radio_buttons:
                    rb.config(text="", value="")
                self.next_button.config(state="disabled")
                return
            
            self.current_word, self.correct_definition = self.words_to_review[0]
            self.word_label.config(text=self.current_word)

            self.get_definitions()

    def on_next(self):
        selected = self.var.get()
        if selected == self.correct_definition:
            if self.review_mode:
                self.remove_word_from_review(self.current_word)
                self.words_to_review.pop(0)
            self.show_toast("Correct", "green", self.next_word)
        else:
            if not self.review_mode:
                self.save_word_to_learn(self.current_word, self.correct_definition)
            print(f"{self.current_word}: {self.correct_definition}")
            self.show_toast("Incorrect", "red", self.next_word)

    def show_toast(self, message, color, callback):
        toast = tk.Toplevel(self.master)
        toast.overrideredirect(True)
        toast.geometry("200x50+{}+{}".format(self.master.winfo_x()+100, self.master.winfo_y()+100))
        label = tk.Label(toast, text=message, bg=color, fg="white", font=(FONT, 14))
        label.pack(fill="both", expand=True)
        # After 1 second, destroy toast and go to next question
        def after_toast():
            toast.destroy()
            callback()
        toast.after(1000, after_toast)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordSmartApp(root)
    root.mainloop()
