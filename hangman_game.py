# ==========================================
# Project 15 - Terminal Hangman Game
# ==========================================

import json
import os
import random

# Global Database File for High Scores
LEADERBOARD_FILE = "hangman_leaderboard.json"

# Word Categories Data Bank
WORDS_BANK = {
    "MOVIES": ["INCEPTION", "AVENGERS", "INTERSTELLAR", "GLADIATOR", "TITANIC", "PARASITE"],
    "TECH": ["PYTHON", "JAVASCRIPT", "DATABASE", "INTERNET", "ALGORITHM", "COMPILER"],
    "ANIMALS": ["ELEPHANT", "KANGAROO", "PENGUIN", "CHEETAH", "DOLPHIN", "CHIMPANZEE"],
    "COUNTRIES": ["INDIA", "CANADA", "AUSTRALIA", "GERMANY", "JAPAN", "BRAZIL"]
}

# Visual Stages of Hangman (ASCII Art)
HANGMAN_STAGES = [
    """
       +---+
       |   |
           |
           |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
     =========
    """
]


# -------------------------------
# Leaderboard Management (JSON)
# -------------------------------

def load_leaderboard():
    """Loads top scores from the JSON file."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def save_score(player_name, score):
    """Saves the player's winning score and updates the leaderboard."""
    leaderboard = load_leaderboard()
    leaderboard.append({"name": player_name, "score": score})
    
    # Sort leaderboard by highest score first
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
    
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=2)


def view_leaderboard():
    """Displays the top 5 high scores."""
    print("\n🏆 --- HANGMAN LEADERBOARD --- 🏆")
    leaderboard = load_leaderboard()
    
    if not leaderboard:
        print("No scores recorded yet. Be the first to win!")
        return
        
    print(f"{'Rank':<6} | {'Player Name':<20} | {'Score (Remaining Lives)':<10}")
    print("-" * 48)
    for index, record in enumerate(leaderboard, 1):
        print(f"{index:<6} | {record['name']:<20} | {record['score']:<10}")


# -------------------------------
# Core Game Loop Implementation
# -------------------------------

def play_game():
    print("\n--- Start New Game ---")
    player_name = input("Enter your name: ").strip()
    if not player_name:
        player_name = "Anonymous Player"

    # 1. Select Category
    print("\nChoose a Word Category:")
    categories = list(WORDS_BANK.keys())
    for index, cat in enumerate(categories, 1):
        print(f"{index}. {cat}")
        
    choice = input("Select category number (1-4): ").strip()
    if choice not in ["1", "2", "3", "4"]:
        print("❌ Invalid selection! Defaulting to 'TECH'.")
        category_name = "TECH"
    else:
        category_name = categories[int(choice) - 1]

    # Pick a random secret word from the chosen category
    secret_word = random.choice(WORDS_BANK[category_name])
    
    # Setup tracking lists
    guessed_letters = []
    wrong_attempts = 0
    max_lives = 6

    print(f"\n🎮 Category Selected: {category_name}. Game Started!")

    # Game Loop
    while wrong_attempts < max_lives:
        # Print Hangman Visual Stage
        print(HANGMAN_STAGES[wrong_attempts])
        
        # Build masked word structure (e.g., P _ T H _ N)
        display_word = []
        for letter in secret_word:
            if letter in guessed_letters:
                display_word.append(letter)
            else:
                display_word.append("_")
        
        current_progress = " ".join(display_word)
        print(f"Word to guess: {current_progress}")
        print(f"Guessed Letters: {', '.join(guessed_letters) if guessed_letters else 'None'}")
        print(f"Remaining Lives: {max_lives - wrong_attempts}")

        # Win Condition Check
        if "_" not in display_word:
            print(f"\n🎉 CONGRATULATIONS {player_name}! You guessed the word '{secret_word}' correctly!")
            score = max_lives - wrong_attempts
            save_score(player_name, score)
            return

        # Player Input
        guess = input("\nGuess a letter: ").strip().upper()

        # Input Validations
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Invalid Input! Please guess exactly one alphabetic letter.")
            continue
            
        if guess in guessed_letters:
            print(f"⚠️ You already guessed '{guess}'. Try a different letter!")
            continue

        # Process the guess
        guessed_letters.append(guess)

        if guess in secret_word:
            print(f"✅ Good job! '{guess}' is in the word.")
        else:
            print(f"❌ Oops! '{guess}' is not in the word.")
            wrong_attempts += 1

    # Lose Condition
    print(HANGMAN_STAGES[wrong_attempts])
    print(f"💀 GAME OVER, {player_name}! You ran out of lives.")
    print(f"The correct word was: '{secret_word}'")


# -------------------------------
# Main Interface Structure
# -------------------------------

def menu():
    while True:
        print("\n===== 🎯 HANGMAN GAME ENGINE =====")
        print("1. Play Hangman")
        print("2. View Top Leaderboard")
        print("3. Exit Game")
        print("==================================")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            view_leaderboard()
        elif choice == "3":
            print("\n👋 Thank you for playing Hangman! See you next time.")
            break
        else:
            print("❌ Invalid Choice! Please enter a number between 1 and 3.")


if __name__ == "__main__":
    menu()