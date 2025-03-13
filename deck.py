import pandas as pd
from itertools import combinations
import random

def select_game(game_select=None):
    card_games = {
        "Poker": 2,  # Adjust the number of cards as needed, easy to add more games
        "Blackjack": 2,
        "Truco": 3,
    }
    while True:
        try:
            game_select = input("Choose one of the games\n"
                                "Poker\n"
                                "Blackjack\n"
                                "Truco\n"
                                ": ").capitalize()
            if game_select in card_games:
                num_cards_per_player = card_games[game_select]
                print(f"You chose {game_select}. Each player will receive {num_cards_per_player} cards.")
                return game_select, num_cards_per_player
            else:
                print(f"{game_select} is not available or is invalid.")
        except Exception as e:
            print(f"Error: {e}")

def select_num_players(num_players=None):
    num_players = 0
    while num_players < 2 or num_players > 16:
        try:
            num_players = int(input("Select the number of players (2-16): "))
            if num_players < 2 or num_players > 16:
                print("Please enter a number between 2 and 16.")
        except ValueError:
            print("Invalid input! Enter an integer number.")
    print(f"Number of players: {num_players}")
    return num_players

def create_deck(suits=None, values=None):
    # Deck data
    if suits is None:
        suits = ["Diamonds ♦", "Spades ♠", "Hearts ♥", "Clubs ♣"]
    if values is None:
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    # Generate full deck
    card = [{"Value": value, "Suit": suit} for suit in suits for value in values]
    deck = pd.DataFrame(card)

    return deck

def deal_cards(deck, num_players, num_cards_per_player):
    # Distribute random cards to players without repetition.
    if num_players * num_cards_per_player > len(deck):
        raise ValueError("Not enough cards in the deck for distribution.")

    # Shuffle the deck (randomly shuffles the indexes)
    shuffled_deck = deck.sample(frac=1, random_state=None).reset_index(drop=True)

    # Distribute cards to players
    players = {}
    for player in range(1, num_players + 1):
        # Select the first available cards
        players[f"Player {player}"] = shuffled_deck.iloc[:num_cards_per_player].to_dict(orient="records")
        # Remove distributed cards from the deck
        shuffled_deck = shuffled_deck.iloc[num_cards_per_player:].reset_index(drop=True)

    # Distribute table cards
    dist_cards = 5
    table_cards = []
    for tb in range(dist_cards):
        table_cards.append(shuffled_deck.iloc[:1].to_dict(orient="records")[0])
        shuffled_deck = shuffled_deck.iloc[1:].reset_index(drop=True)

    return players, shuffled_deck, table_cards

card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
               '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def card_value(card):
    """Returns the numerical values of the cards, considering Ace as 1 or 14"""
    return card_values[card] if card != "A" else [1, 14]

def evaluate_hand(cards):
    # Extract values and suits from cards
    values = sorted([card_values[card["Value"]] for card in cards], reverse=True)
    suits = [card["Suit"] for card in cards]

    # Count occurrences of each value and each suit
    value_count = {value: values.count(value) for value in values}
    suit_count = {suit: suits.count(suit) for suit in suits}

    # Check for a Flush (5 cards of the same suit)
    flush = any(count == 5 for count in suit_count.values())
    # Check for a Straight (5 consecutive values)
    straight = values == list(range(values[0], values[0] - 5, -1))
    # Special case for a Straight with A-2-3-4-5
    if set(values) == {14, 2, 3, 4, 5}:
        straight = True
        values = [5, 4, 3, 2, 1]  # Adjust so Ace counts as 1
    # Check for Royal Flush (A-K-Q-J-10 of the same suit)
    if flush and values == [14, 13, 12, 11, 10]:
        return "Royal Flush"
    # Check for Straight Flush (sequence + flush)
    if flush and straight:
        return "Straight Flush"
    # Check for Four of a Kind
    if 4 in value_count.values():
        return "Four of a Kind"
    # Check for Full House (Three of a Kind + a Pair)
    if 3 in value_count.values() and 2 in value_count.values():
        return "Full House"
    # Check for Flush (all same suit)
    if flush:
        return "Flush"
    # Check for Straight (sequence)
    if straight:
        return "Straight"
    # Check for Three of a Kind
    if 3 in value_count.values():
        return "Three of a Kind"
    # Check for Two Pair
    if list(value_count.values()).count(2) == 2:
        return "Two Pair"
    # Check for One Pair
    if 2 in value_count.values():
        return "One Pair"
    # If nothing is found, return High Card
    return "High Card"
