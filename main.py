"""
Main module for the flash card app.

It is an app with a GUI to implement a flash card app. The sides of the cards
are read from an external CSV, where each line consists of a pair of strings.
Each line represents a card, with the first value being on the "front", the
second on the "back" side of the card.

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
This can be changed in the "card.py" as well, by swapping the values of the
"FRONT" and "BACK" globals (note that the only viable values are 0 and 1, and
the two must be different, else the program will run on an error)

THERE IS NO ERROR HANDLING CURRENTLY, THE FILES MUST BE PRESENT IN THE
CORRECT FOLDERS FOR THE PROGRAM TO RUN PROPERLY.
"""


import os
import tkinter as tk

import card

# Global variables, colors and fonts
BACKGROUND_COLOR = "#B1DDC6"
FOREGROUND_COLOR = "#FFFFFF"

FONT_NAME = ""
FONT_SIZE = 40

FONT_TITLE = (FONT_NAME, FONT_SIZE, "normal")
FONT_WORD = (FONT_NAME, FONT_SIZE * 2, "bold")
FONT_SWITCH = (FONT_NAME, FONT_SIZE // 3, "bold")


if __name__ == "__main__":

    # Creating the main window for the app.
    window = tk.Tk()
    window.title("Flash Cards")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


    # Loading the images.
    card_front_img = tk.PhotoImage(file=os.path.join("", "images", "card_front.png"))
    card_back_img = tk.PhotoImage(file=os.path.join("", "images", "card_back.png"))
    correct_img = tk.PhotoImage(file=os.path.join("", "images", "correct.png"))
    wrong_img = tk.PhotoImage(file=os.path.join("", "images", "wrong.png"))
    switch_img = tk.PhotoImage(file=os.path.join("", "images", "switch.png"))


    # Creating the canvas, to place the "card" in the window.
    canvas = tk.Canvas(
        window, height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0
    )
    card_img = canvas.create_image(400, 263, image=card_front_img)
    canvas.bind("<Button-1>",func=lambda x: flash_card.flip(x, canvas))
    title_text = canvas.create_text(400, 150, font=FONT_TITLE)
    word_text = canvas.create_text(400, 263, font=FONT_WORD)

    # The front and back direction label.
    front_back = tk.Label(
        text=f"",
        bg=BACKGROUND_COLOR,
        foreground=FOREGROUND_COLOR,
        border=0,
        font=FONT_SWITCH
    )

    # Creating the card class, passing the canvas elements as argument, as these
    # will be modified within the class methods.
    flash_card = card.Card(
        titletext=title_text,
        wordtext=word_text,
        cardimg=card_img,
        cardfrontimg=card_front_img,
        cardbackimg=card_back_img,
        frontback=front_back
    )

    # Buttons for the correct, wrong guess and the switch direction.
    wrong_button = tk.Button(
        image=wrong_img,
        highlightthickness=0,
        command=lambda: flash_card.wrong(canvas),
        border=0
    )

    correct_button = tk.Button(
        image=correct_img,
        highlightthickness=0,
        command=lambda: flash_card.correct(canvas),
        border=0,
    )

    switch_button = tk.Button(
        image=switch_img,
        highlightthickness=0,
        command=lambda: flash_card.change_order(canvas),
        border=0
    )


    # Placement of the elements to the window.
    canvas.grid(column=0, row=0, columnspan=2)
    wrong_button.grid(column=0, row=1)
    correct_button.grid(column=1, row=1)
    switch_button.grid(column=0, row=3, columnspan=2)
    front_back.grid(column=0, row=4, columnspan=2)


    # Initial setup for the words on the card and the direction indicator.
    flash_card.set_word(canvas)
    front_back.config(text=f"{flash_card.title_front} <-> {flash_card.title_back}")


    window.mainloop()
