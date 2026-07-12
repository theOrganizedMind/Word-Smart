# Word Smart
 
 A Python/Tkinter vocabulary study app inspired by The Princeton Review's Word Smart.
 
 This repository provides a small desktop study tool for practicing vocabulary 
 through multiple-choice quizzes, spelling prompts, and flashcards.
 
 ## Features
 
 - Multiple-choice vocabulary quiz
 - Spelling practice mode
 - Flashcard review mode
 - Review list saved to JSON for missed or manually added words
 - Simple desktop UI built with Tkinter
 
 ## Study Modes
 
 ### Multiple-Choice Quiz
 
 Run [word_smart.py](word_smart.py) to practice matching words to their definitions.
 
 - Shows one word at a time
 - Presents five possible definitions
 - Saves missed words to a review list
 - Lets you manually add the current word for later review
 
 ### Spelling Practice
 
 Run [spelling.py](spelling.py) to practice recalling the word from its definition.
 
 - Shows a definition
 - Prompts you to type the matching word
 - Saves missed words for later review
 - Supports manual review additions
 
 ### Flashcards
 
 Run [flashcard.py](flashcard.py) for simple word-definition flashcards.
 
 - Front shows the word
 - Back shows the definition
 - Next advances to another unreviewed word
 
 ## Project Structure
 
 - [word_smart.py](word_smart.py): Main multiple-choice quiz app
 - [spelling.py](spelling.py): Spelling practice app
 - [flashcard.py](flashcard.py): Flashcard app
 - [word_dict.py](word_dict.py): Vocabulary word and definition source
 - [words_to_learn.json](words_to_learn.json): Saved review words
 - [LICENSE.txt](LICENSE.txt): Repository license
 
 ## Requirements
 
 This project uses Python 3 and the standard library.
 
 Main modules used:
 
 - tkinter
 - random
 - json
 
 No third-party dependencies are currently required.
 
 ## Getting Started
 
 1. Install Python 3.
 2. Clone or download this repository.
 3. Open a terminal in the project folder.
 4. Run one of the study modes below.
 
 ### Run the Quiz App
 
 ```bash
 python word_smart.py
 ```
 
 ### Run the Spelling App
 
 ```bash
 python spelling.py
 ```
 
 ### Run the Flashcard App
 
 ```bash
 python flashcard.py
 ```
 
 ## Review Data
 
 Words you miss, or manually mark for later study, are stored in 
 [words_to_learn.json](words_to_learn.json).
 
 That file acts as the app's review queue across the quiz and spelling modes.
 
 ## Attribution
 
 This project is based on The Princeton Review Word Smart.
 
 The vocabulary and definitions used in this repository are derived from 
 The Princeton Review Word Smart book. Full credit for the source material 
 belongs to The Princeton Review and the book's authors and publishers.
 
 This repository is an independent study project and is not affiliated with, 
 endorsed by, or sponsored by The Princeton Review.
 
 ## License
 
 The code in this repository is licensed under the MIT License. 
 See [LICENSE.txt](LICENSE.txt).
 
 ## Notes
 
 - This project is intended for educational and personal study use.
 - The current [requirements.txt](requirements.txt) file is empty because 
 no external packages are required.
 