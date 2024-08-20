# Hi-Lo
BlackJack Card Counting and Optimal Bet Sizing with Kelly Criterion


Simulates any number of blackjack games where the Hero uses basic (optimal strategy) and a high-low card counting technique. Bet size is determined by Kelly Criterion wherein the Hero gains an (approximate) edge of 0.5% for every TrueCount increase above 1. The "Illustrious 18" play deviances (capturing ~85% of the value from all possible deviances) are also included. The relative aggression of a Kelly Bet strongly influences the bankroll variance over time, with plus-EV results favoring a semi-aggressive Kelly Bet (around 40-50% of a standard Kelly Bet, with minimum bet requirements hindering the applicability of Kelly Criterion). 

See Kelly_100k.png for a comparison of bet aggression levels.
  0.4x standard Kelly Bet seems to introduce enough aggression to capitalize on positive true counts but not too much as to destroy the bankroll early before any accumulation.


See NumDecks.png for a comparison of performance with different numbers of decks being played. 
  High-Low is massively profitable when the minimum number of decks (2) is being played. 
