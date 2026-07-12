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
#
# =========================================================================== #

FONT = "Arial"
WORDS_TO_LEARN_FILE = "words_to_learn.json"


class WordSmartSpellingApp:
    """
    A Tkinter-based spelling quiz application.

    Features:
    - Displays a random definition from the dictionary and asks the user to type
      the correct word.
    - Checks the user's answer when "Next" is clicked, shows a toast notification
      for correct/incorrect answers,
      and automatically moves to the next definition.
    - Keeps the main window size fixed and wraps long definitions.
    - Tracks definitions already shown to avoid repetition until all are used.
    - Saves incorrectly answered words and their definitions to
      'words_to_learn.json' for later review.

    Args:
        master (tk.Tk): The root Tkinter window.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Word Smart Spelling")
        self.master.geometry("500x300")
        self.master.resizable(False, False) # Prevent resizing

        self.definition_label = tk.Label(master, font=(FONT, 12), 
                                         wraplength=400, justify="left")
        self.definition_label.pack(pady=20)

        self.word_entry = tk.Entry(master, font=(FONT, 16), width=30)
        self.word_entry.pack(pady=10)

        self.next_button = tk.Button(master, text="Next", command=self.on_next)
        self.next_button.pack(pady=20)

        # Bind Enter key to trigger the Next Button
        self.word_entry.bind("<Return>", lambda event: self.on_next())     

        # Add button for adding word/definition for review
        self.add_frame = tk.Frame(master)
        self.add_frame.pack(pady=10)
        self.add_button = tk.Button(self.add_frame, text="Add", command=self.on_add)
        self.add_button.pack()

        self.current_word = None
        self.correct_definition = None
        self.chosen_defs = [] # Store chosen definitions
        self.review_mode = False
        self.words_to_review = []
        self.next_definition()

    def on_add(self):
        # Add the currently displayed word and its correct definition for review
        if self.current_word and self.correct_definition:
            self.save_word_to_learn(self.current_word, self.correct_definition)
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

    def next_definition(self):
        self.word_entry.delete(0, tk.END)
        if not self.review_mode:
            # If all definition have been used, switch to review mode
            if len(self.chosen_defs) == len(word_dict):
                self.review_mode = True
                self.load_words_to_review()
                if self.words_to_review:
                    self.show_toast("Words to Review", "blue", self.next_definition)
                else:
                    self.show_toast("All Done!", "green", lambda: None)
                return
            
            # Choose a random definition not already chosen
            remaining_items = [(w, d) for w, d in word_dict.items() if d not in self.chosen_defs]
            self.current_word, self.current_definition = random.choice(remaining_items)
            self.chosen_defs.append(self.current_definition)
            self.definition_label.config(text=self.current_definition)
        else:
            # Review mode: show words from words_to_learn.json
            if not self.words_to_review:
                self.show_toast("Review complete!", "green", lambda: None)
                self.definition_label.config(text="No more words to review.")
                self.word_entry.config(state="disabled")
                self.next_button.config(state="disabled")
                return
            
            self.current_word, self.current_definition = self.words_to_review[0]
            self.definition_label.config(text=self.current_definition)

    def on_next(self):
        user_word = self.word_entry.get().strip()
        # if not user_word:
        #     self.show_toast("Please enter a word", "orange", lambda: None)
        #     return
        if user_word.lower() == self.current_word.lower():
            if self.review_mode:
                self.remove_word_from_review(self.current_word)
                self.words_to_review.pop(0)
            self.show_toast("Correct", "green", self.next_definition)
        else:
            if not self.review_mode:
                self.save_word_to_learn(self.current_word, self.current_definition)
            print(f"{self.current_word}: {self.current_definition}")                
            self.show_toast(f"{self.current_word}", "red", self.next_definition)

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
    app = WordSmartSpellingApp(root)
    root.mainloop()

