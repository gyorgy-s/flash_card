"""
Card module for the flash card app.

The sides of the cards are read from an external CSV, where each line consists
of a pair of strings. Each line represents a card, with the first value being
on the "front", the second on the "back" side of the card.

The first line of the file represents the title for the values. In the example
these being the French and English word pairs.

The app reads the source CSV as to be able to handle the manipulation of the
source file, as long as it adhedes the above mentioned rules.

The user can flip the card by clicking on it to check their answer.
If the user clicks on the "correct" button, the word is then removed from the
pool, as it is already known. If the user clicks on the "wrong" button, the
card will stay in the pool. In both cases, a new card will be picked from the
pool.

The user is able to switch the "front" and "back" of the cards by clicking the
"switch" button. (The default order is given by the occurrence in the source CSV.
This can be changed in the "card.py", by swapping the values of the
"FRONT" and "BACK" globals (note that the only viable values are 0 and 1, and
the two must be different, else the program will run on an error)

THERE IS NO ERROR HANDLING CURRENTLY, THE FILES MUST BE PRESENT IN THE
CORRECT FOLDERS FOR THE PROGRAM TO RUN PROPERLY.
"""


import os
import random
import pandas as pd


# Global variables, colors and source file name
BACKGROUND_COLOR = "#B1DDC6"
FOREGROUND_COLOR = "#FFFFFF"

if os.path.exists(os.path.join("", "data", "to_learn.csv")):
    DATA_SOURCE = "to_learn.csv"
else:
    DATA_SOURCE = "source.csv"

# Front - back direction, if the default order should be switched, swap the
# values of these. The default values are:
# FRONT = 0
# BACK = 1
# Representing the order in which the word pairs are present in the CSV.
FRONT = 0
BACK = 1

class Card:
    """Card class for the flash cards. Implements the main functions and features of the flsh card."""

    def __init__(self, titletext, wordtext, cardimg, cardfrontimg, cardbackimg, frontback):
        # Initializing the dictionary. First reading the first row of the CSV,
        # getting the header for the values. Then reaping the rest of the CSV,
        # and compiling it into a dict.
        df_header = pd.read_csv(
            os.path.join("", "data", DATA_SOURCE),
            index_col=None,
            header=None,
            nrows=1
        )

        self.title_front = df_header.iat[0,FRONT]
        self.title_back = df_header.iat[0,BACK]

        self.dictionary = pd.read_csv(
            os.path.join("", "data", DATA_SOURCE),
            index_col=0,
            header=None,
            skiprows=1,
            names=[self.title_front, self.title_back]
        )

        self.current_word = self.get_random_word()
        self.side = -1

        # Attributes solely to handle the external widgets from TKinter.
        self.title_text = titletext
        self.word_text = wordtext
        self.card_img = cardimg
        self.card_front_img = cardfrontimg
        self.card_back_img = cardbackimg
        self.front_back = frontback


    def get_random_word(self):
        """Gets a random key-value pair from the dicitionary."""
        if not self.dictionary.empty :
            if FRONT:
                word = list(self.dictionary.sample(1).to_dict(orient="dict")[self.title_front].items())[0]
            else:
                word = list(self.dictionary.sample(1).to_dict(orient="dict")[self.title_back].items())[0]
        else:
            word = ("THE END","THE END")
        self.current_word = word
        return word

    def pop_word(self):
        """Removes the current word from the dicitionary."""
        if len(self.dictionary) > 0:
            self.dictionary = self.dictionary.drop(self.current_word[0])
            self.dictionary.to_csv(os.path.join("", "data", "to_learn.csv"))

    def set_word(self, canv):
        """Updates the Tk widgets according the current words."""
        if self.side < 0:
            canv.itemconfig(self.title_text, text=self.title_front, fill=BACKGROUND_COLOR)
            canv.itemconfig(self.word_text, text=self.current_word[FRONT], fill=BACKGROUND_COLOR)
            canv.itemconfig(self.card_img, image=self.card_front_img)
        elif self.side > 0:
            canv.itemconfig(self.title_text, text=self.title_back, fill=FOREGROUND_COLOR)
            canv.itemconfig(self.word_text, text=self.current_word[BACK], fill=FOREGROUND_COLOR)
            canv.itemconfig(self.card_img, image=self.card_back_img)

    def flip(self, event, canv):
        """Flips the card's front and back, then updates the widgets."""
        self.side *= -1
        self.set_word(canv)

    def correct(self, canv):
        """If the user was correct, removes the current word from the pool,
        then gets a new one and updates the widgets."""
        self.pop_word()
        self.get_random_word()
        self.side = -1
        self.set_word(canv)

    def wrong(self, canv):
        """Id the user was wrong, gets a new card from the pool and updates the widgets."""
        self.get_random_word()
        self.side = -1
        self.set_word(canv)

    def change_order(self, canv):
        """Swaps the cards' front and back."""
        global FRONT
        global BACK

        FRONT, BACK = BACK, FRONT
        self.title_front, self.title_back = self.title_back, self.title_front
        self.front_back.config(text=f"{self.title_front} <-> {self.title_back}")
        self.set_word(canv)
