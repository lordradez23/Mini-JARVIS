import random

def get_joke():
    """Returns a random joke."""
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why was the cell phone wearing glasses? It lost its contacts.",
        "What do you call a computer that sings? A Dell.",
        "Why did the web developer walk out of the restaurant? Because of the table layout."
    ]
    return random.choice(jokes)

def get_fun_fact():
    """Returns a random interesting fact."""
    facts = [
        "The first computer programmer was Ada Lovelace.",
        "Honey never spoils.",
        "A group of flamingos is called a 'flamboyance'.",
        "The shortest war in history lasted only 38 minutes."
    ]
    return random.choice(facts)

def play_mini_game(game_name, user_choice=None):
    """Handles simple logic for mini-games."""
    if game_name == "dice":
        return f"I rolled a {random.randint(1, 6)}."
    elif game_name == "coin":
        return f"It's {'Heads' if random.random() > 0.5 else 'Tails'}."
    elif game_name == "rps":
        options = ["rock", "paper", "scissors"]
        bot_choice = random.choice(options)
        if user_choice == bot_choice:
            return f"I chose {bot_choice}. It's a tie!"
        win_map = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if win_map[user_choice] == bot_choice:
            return f"I chose {bot_choice}. You win!"
        return f"I chose {bot_choice}. I win!"
    return "I'm not sure how to play that."
