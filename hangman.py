from sqlalchemy import ForeignKey, Column, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import sessionmaker
import random
from words import word_list


Base = declarative_base()

class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    score = Column(Integer, nullable=False)


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    player_name = Column(String, nullable=False)

engine = create_engine('sqlite:///game_scores.db')
Base.metadata.create_all(engine)


def get_word(): 
    word= random.choice(word_list)
    return word.upper() # We'll be converting all user input to uppercase to make comparison logic simpler and easier to read. 
          

def play(word, selected_player): 
    # print("WORD: ", word)
    total = 0
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
                total = 1
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
    
        Session = sessionmaker(bind=engine)
        session = Session()
        score = Score(player_id=selected_player.id, score=total)
        session.add(score)
        session.commit()

        print("Your score has been saved.")

    else:
        print("Everybody is laughing at you, loser! You ran out of tries & lost the game. The word was " + word + ". Better luck next time!")



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

Session = sessionmaker(bind=engine)
session = Session()

def main(): # Main function that puts everything together 

    player_name = input("Enter your name: ")
    selected_player = session.query(Player).filter(Player.player_name == player_name).first()
    if not selected_player:
        selected_player = Player(player_name=player_name)
        session.add_all([selected_player])
        session.commit()

    def edit_player_id(selected_player):
        change = input("Enter your new name: ")
        selected_player.player_name = change
        session.add(selected_player)
        session.commit()

    def delete_player(selected_player):
        session.query(Player).filter_by(player_name=selected_player.id).delete()
        session.commit()

    def view_all_high_scores(selected_player):
        scores = session.query(Score).filter(Score.player_id == selected_player.id).all()
        for score in scores:
            print(f"Player: {selected_player.player_name} - Score: {score.score}")
    

    word = get_word()
    play(word, selected_player) 

    while True:
        choice = input("Play Again? (Y/N) / View All High Scores (V) / Delete Player? (D) / Edit Name (E) / Quit? (Q): ").upper() # Asks user if they want to play again. Program will run as long as user types "Y"
        
        if choice == "Y":
            word = get_word()
            play(word, selected_player)
        
        elif choice == "V":
            view_all_high_scores(selected_player)

        elif choice == "D":
            delete_player(selected_player)
            print("Your player name has been deleted.")
        elif choice == "E":
            edit_player_id(selected_player)
        elif choice == "Q" or choice == "N":
            break
        else: 
            print("Invalid option. Please choose one of the following: Y, N, D, E, or Q.")

if __name__ == "__main__": # This allows us to run the game from the command line
    main()





# def main(): # Main function that puts everything together 
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     selected_player = get_player(session)
#     while True:
#         word = get_word()
#         play(word, selected_player)
#         if input("Play Again? (Y/N) ").upper() != "Y":
#             break
#     word = get_word()
#     play(word) 
#     while input("Play Again? (Y/N) ").upper() == "Y": # Asks user if they want to play again. Program will run as long as user types "Y"
#         word = get_word()
#         play(word)

# if __name__ == "__main__": # This allows us to run the game from the command line
#     main()

