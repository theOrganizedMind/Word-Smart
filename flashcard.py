import random
import tkinter as tk
from tkinter import messagebox

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

class FlashCardApp:
    """
    A simple flashcard application for reviewing vocabulary words and their definitions.

    Features:
        - Displays a word (front) or its definition (back) using a Tkinter GUI.
        - 'Front' button shows the word.
        - 'Back' button shows the definition.
        - 'Next' button advances to a new, random word that has not yet been reviewed.
        - When all words have been reviewed, notifies the user and stops advancing.

    Attributes:
        root (tk.Tk): The main Tkinter window.
        words (list): List of all words from the word_dict.
        reviewed_words (set): Set of words that have already been shown.
        current_word (str): The word currently being displayed.
        showing_front (bool): Whether the front (word) is currently shown.
        card_label (tk.Label): The label widget displaying the word or definition.
        front_button (tk.Button): Button to show the front.
        back_button (tk.Button): Button to show the back.
        next_button (tk.Button): Button to advance to the next word.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Word Smart Flashcards")

        self.words = list(word_dict.keys())
        self.reviewed_words = set()
        self.current_word = None
        self.showing_front = True

        self.card_label = tk.Label(self.root, text="", font=("Arial", 24), 
                                   wraplength=400, width=30, height=5)
        self.card_label.pack(pady=30)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.front_button = tk.Button(button_frame, text="Front", 
                                      command=self.show_front)
        self.front_button.grid(row=0, column=0, padx=10, pady=10)

        self.back_button = tk.Button(button_frame, text="Back", 
                                     command=self.show_back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10)

        self.next_button = tk.Button(button_frame, text="Next", 
                                     command=self.next_card)
        self.next_button.grid(row=0, column=2, padx=10, pady=10)

        self.next_card()
        self.root.mainloop()

    def show_front(self):
        if self.current_word:
            self.card_label.config(text=self.current_word)
            self.showing_front = True

    def show_back(self):
        if self.current_word:
            definition = word_dict[self.current_word]
            self.card_label.config(text=definition)
            self.showing_front = False

    def next_card(self):
        remaining_words = [w for w in self.words if w not in self.reviewed_words]
        if not remaining_words:
            self.card_label.config(text="All words reviewed!")
            self.showing_front = True
            return
        self.current_word = random.choice(remaining_words)
        self.reviewed_words.add(self.current_word)
        self.show_front()


if __name__ == "__main__":
    app = FlashCardApp()
