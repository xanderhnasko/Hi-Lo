# Hi-Lo
BlackJack Card Counting and Optimal Bet Sizing with Kelly Criterion


Simulates any number of blackjack games where the Hero uses basic (optimal strategy) and a high-low card counting technique. Bet size is determined by Kelly Criterion wherein the Hero gains an (approximate) edge of 0.5% for every TrueCount increase above 1. The "Illustrious 18" play deviances (capturing ~85% of the value from all possible deviances) are also included. The relative aggression of a Kelly Bet strongly influences the bankroll variance over time, with plus-EV results favoring a semi-aggressive Kelly Bet (around 40-50% of a standard Kelly Bet, with minimum bet requirements hindering the applicability of Kelly Criterion). 
