# Previously __init__.py

# import sqlite3
# CONN = sqlite3.connect('company.db')
# CURSOR = CONN.cursor()

from sqlalchemy import ForeignKey, Column, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import sessionmaker
import random
from words import word_list


Base = declarative_base()


def get_word(): 
    word= random.choice(word_list)
    return word.upper() # We'll be converting all user input to uppercase to make comparison logic simpler and easier to read. 
          

def play(word): 
    word_completion = "_" * len(word) # This will be the word that the user sees.
    guessed = False # This will be used to keep track of whether the game has been won or lost.
    guessed_letters = [] # Holds the letter the user guessed
    guessed_words = [] # Holds the word the user guessed
    tries = 6 # The # of tries the user has to guess the word.
    print("Let's play Hangman!") # Initial Output to help guide the user when the game starts
    print(display_hangman(tries)) # Displays the initial state of Hangman 
    print(word_completion) # Displays the intial state of the word w/ all underscores 
    print("\n") # Prints a new line for readability 


    while not guessed and tries > 0: # Loop that'll run until the word is guessed or user runs out of tries
        guess = input("Please guess a letter or word: ").upper() # Prompts user to guess a letter/word & converts input to uppercase
        if len(guess) == 1 and guess.isalpha(): # If user's guess is a single letter & alphabetical
            if guess in guessed_letters: # Checks if letter has already been guessed, not in the word, or it is in the word.
                print("You already guessed the letter", guess) 
            elif guess not in word: 
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else: 
                print("Nice job", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion: # If no more underscores are in the word, the user has guessed the word.
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha(): # Guess is a word & alphabetical
            if guess in guessed_words: # Checks if word has already been guessed, not in the word, or if it is in the word.
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1 # Decrement the num of tries by 1
                guessed_words.append(guess)
            else:            # The user correctly guessed the word
                guessed = True 
                word_completion = word
        else: 
            print("Not a valid guess.")
        print(display_hangman(tries)) # Prints current state of Hangman & the word
        print(word_completion)
        print("\n") # Prints new line for readability
    if guessed: 
        print("FLAWLESS VICTORY. Congrats, you guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries & lost the game. The word was " + word + ". Better luck next time!")



def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]

def main(): # Main function that puts everything together 
    word = get_word()
    play(word) 
    while input("Play Again? (Y/N) ").upper() == "Y": # Asks user if they want to play again. Program will run as long as user types "Y"
        word = get_word()
        play(word)

if __name__ == "__main__": # This allows us to run the game from the command line
    main()

