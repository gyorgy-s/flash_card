# flash_card
Implementation of a flash card app with GUI that gets the card from a CSV.

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

To install requirtements, run from the main folder:


```
pip install -r requirements.txt 
```
