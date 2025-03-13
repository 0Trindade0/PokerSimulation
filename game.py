from Deck import create_deck, deal_cards, select_num_players, select_game
from Project_GOA.Deck import evaluate_hand

game, num_cards = select_game()
if game is None or num_cards is None:
    print("Error selecting game. Exiting program.")
    exit()

num_players = select_num_players()
deck = create_deck()
players, remaining_deck, table_cards = deal_cards(deck, num_players, num_cards)

player1 = players['Player 1']
print("Player 1's Cards:")
for card in player1:
    print(f"{card['Value']} of {card['Suit']}")

print("\nTable Cards:")
for i, card in enumerate(table_cards, start=1):
    print(f"Card {i}: {card['Value']} of {card['Suit']}")

# Evaluate Player 1's hand (considering hand + table)
complete_hand = player1 + table_cards
hand_evaluation = evaluate_hand(complete_hand)
print(f"\nPlayer 1's Hand Evaluation: {hand_evaluation}")

"""for player, cards in players.items():
    print(f"{player}")
    for card in cards:
        print(f" {card['Value']} of {card['Suit']}")
    print()"""

print(f"Remaining cards in the deck: {len(remaining_deck)}")
