# Splittin-eights

Splittin-Eights is a text-based Python blackjack game that allows players to enjoy the classic card game of blackjack. The game is implemented using Python and leverages a simple command-line interface to simulate a casino-style blackjack experience. Players can create and manage their profiles, place bets, draw cards, and challenge the dealer to win chips.



Features:

Player Profiles: Create and manage player profiles with customizable names and starting chips.

Blackjack Gameplay: Experience classic blackjack gameplay, including card drawing, player decisions, and dealer play.

Betting System: Place bets with your chips and compete for rewards.

Database Integration: Store game results and player profiles in a SQLite database.

Results Tracking: View game results by player or for all games played.




How to Play:

In the terminal run pipenv run python lib/App.py to enter the game's Main Menu.

Main Menu: When you launch the game, you'll be presented with the main menu. Here, you can choose to create a new player profile, load an existing profile, view game results, or exit the game.

Player Profiles: You can create a new player profile by entering your name and specifying the number of chips you want to start with. If you have an existing profile, you can load it using your name.

Gameplay: Once you have a player profile, you can start a new game. Place your bet and draw cards by selecting options. You can choose to "Hit" to draw a card, "Stay" to keep your current hand, or "Quit" to return to the main menu.

Dealer's Turn: After you've made your choices, the dealer will play their hand based on standard blackjack rules.

Game Results: The game will determine the winner, update chip counts, and store the game result in the database. You can view results by player or see all game results in the "Results Menu."



Game Rules:

The objective is to have a hand value as close to 21 as possible without exceeding it.
Cards have the following values: 2-10 are face value, face cards (J, Q, K) are worth 10, and Aces are worth 11 or 1, whichever is more favorable.
A "blackjack" is an Ace and a 10-value card, and it beats all other hands.
The dealer must "hit" until their hand value is 17 or higher.



Database Integration:

Splittin-Eights uses an SQLite database to store player profiles and game results. The database includes two tables:

players: Stores player information, including names and chip counts.
games: Records game results, including bets, results, and player IDs.

The database is automatically created and managed by the game. You can view your results and track your progress over time.