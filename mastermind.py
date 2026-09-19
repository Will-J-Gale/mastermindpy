import subprocess
from typing import List
from random import choices
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--turns", type=int, default=8)
parser.add_argument("--pins", type=int, default=4)
parser.add_argument("--target", type=str, default=None)
parser.add_argument("--colours", type=int, default=6)

COLOURS = ["R", "G", "B", "Y", "W", "P", "O", "V"]
EXIT_COMMANDS = ["exit", "quit"]
CORRECT_PLACE = "X"
CORRECT_COLOUR = "O"
INCORRECT = "_"
IGNORE = "&"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[34m"
PINK = "\033[95m"
CYAN = "\033[96m"
ORANGE = "\033[33m"
WHITE = "\033[97m"
RESET = "\033[39m"

COLOUR_TO_CODE = {
    "R": RED,
    "G": GREEN,
    "B": BLUE,
    "Y": YELLOW,
    "P": PINK,
    "W": WHITE,
    "O": ORANGE,
    "V": "\033[38;5;56m",
}

def print_game(
        target:str, 
        guess_correct:bool, 
        turns:int, 
        pins:int,
        player_guesses:List=[], 
        clues:List=[], 
        end_game=False):

    assert(len(player_guesses) == len(clues))

    print()
    subprocess.run(["clear"], check=False)
    colours_text = "" 
    for colour in COLOURS:
        colours_text += f"{COLOUR_TO_CODE[colour]}{colour}{RESET} "
    print(colours_text)
    if(guess_correct or end_game):
        print("Target: ", target)
    else:
        target_text = " " .join(["?"] * pins)
        print("Target:", target_text)

    for i in range(turns - 1, -1, -1):
        if(i < len(player_guesses)):
            player_guess = player_guesses[i]
            clue = clues[i]
            player_guess_text = ""
            # player_guess_text = " ".join(player_guess)

            for colour in player_guess:
                text_colour = COLOUR_TO_CODE[colour]
                player_guess_text += f"{text_colour}{colour} {RESET}"

            clue_text = " ".join(clue)
            print(i, "\t", clue_text, "|", player_guess_text)
        else:
            blank = " ".join(["_"] * pins)
            print(i,"\t",  blank, "|", blank)
    
    if(end_game):
        target_text = ""
        for colour in target:
            target_text += f"{COLOUR_TO_CODE[colour]}{colour}{RESET}"

        print("Game Ended:", target_text)

        if(guess_correct):
            print("Player wins!")
        else:
            print("Player loses...")

    print()
        
def compare(guess:str, target:str):
    clue = []
    guess = list(guess)
    target = list(target)
    indexes_to_ignore = []

    correct = True
    for i, colour in enumerate(guess):
        if(target[i] == colour):
            clue.append(CORRECT_PLACE)
            correct &= True
            target[i] = IGNORE
            indexes_to_ignore.append(i)
        else:
            correct &= False
        
    if(correct):
        return clue, correct

    for i, colour in enumerate(guess):
        if(i in indexes_to_ignore):
            continue
        
        if(colour in target):
            clue.append(CORRECT_COLOUR)
            index = target.index(colour)
            target[index] = IGNORE
    
    for i in range(len(clue), len(guess)):
        clue.append(INCORRECT)

    return clue, correct

def get_player_input(pins:int):
    while(True):
        player_input = input("Guess: ")

        if(player_input in EXIT_COMMANDS):
            exit()

        player_input = player_input.upper()

        if(len(player_input) != pins):
            continue

        valid_colours = True
        for colour in player_input:
            if(colour not in COLOURS):
                valid_colours &= colour in COLOURS
        
        if(valid_colours):
            return player_input

def main():
    args = parser.parse_args()
    global COLOURS
    COLOURS = COLOURS[:args.colours]
    target = "".join(choices(COLOURS, k=args.pins))
    if(args.target is not None):
        target = args.target

    player_guesses = []
    clues = []

    print_game(target, False, args.turns, args.pins, player_guesses, clues)

    correct = False
    try:
        for _ in range(args.turns):
            player_guess = get_player_input(args.pins)
            clue, correct = compare(player_guess, target)
            player_guesses.append(player_guess)
            clues.append(clue)
            print_game(target, correct, args.turns, args.pins, player_guesses, clues, end_game=False)

            if(correct):
                break

        print_game(target, correct, args.turns, args.pins, player_guesses, clues, end_game=True)

    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    # args = parser.parse_args()
    main()