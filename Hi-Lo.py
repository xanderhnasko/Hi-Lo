import random
import matplotlib.pyplot as plt
Soft17 = True
NumGames = 100000
InitBankRoll = 10000
BetSize = 1
NumDecks = 2
Penetration = 0.75
AgressionFactor = 0.4
KellyBet = True



class Deck:
    def __init__(self, num_decks=NumDecks):
        self.num_decks = num_decks
        self.cards = self.create_deck()
        
    def create_deck(self):
        values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        return [value for value in values] * 4 * self.num_decks
        

    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self, bet = 1):
        self.cards = []
        self.bet = bet
        self.is_doubled_down = False
    
    def add_card(self, card):
        self.cards.append(card)
    
    def value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card in ['J','Q','K']:
                value += 10
            elif card == 'A':
                value += 11
                num_aces += 1
            else:
                value += int(card)
      
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value
    def blackjack(self):
        return self.value() == 21 and len(self.cards) == 2
    def bust(self):
        return self.value() > 21
    def can_split(self):
        return len(self.cards) == 2 and self.cards[0] == self.cards[1]
    def double_down(self):
        if not self.is_doubled_down:
            self.is_doubled_down = True
            self.bet*=2

class Game:
    def __init__(self, deck, running_count = 0, num_players = 1, num_decks = 1, init_bankroll = InitBankRoll, bet = 1, player_wins = 0, dealer_wins = 0, ties = 0):
        self.deck = deck
        self.player_hands = [Hand(bet)]
        self.other_players = [Hand() for _ in range(num_players - 1)]   
        self.rc = running_count
        self.dealer = Hand()
        self.dealer_upcard = None
        self.bankroll = init_bankroll
        self.player_wins = player_wins
        self.dealer_wins = dealer_wins
        self.ties = ties
        self.num_players = num_players
        self.betsize = self.kelly_citerion()
        self.bets = []
        self.outcomes = []
        

    def count_card(self, card):
        if card in ['2','3','4','5','6']:
            self.rc += 1
        elif card in ['10','J','Q','K','A']:
            self.rc -= 1    
    
    def kelly_citerion(self):
        if KellyBet:
            tc = self.rc/(len(self.deck.cards) / 52) if len(self.deck.cards) > 0 else 0
            # each TC above 1 gives player approx. 0.5% edge
            bet = BetSize
            edge = (tc - 1) * 0.005
            if edge > 0: 
                kelly_bet = self.bankroll * edge * AgressionFactor

                bet = max(BetSize, min(kelly_bet, self.bankroll))
            
            # minbet otherwise
            return bet
        else: return BetSize
        

    def deal(self):
        if len(self.deck.cards) <= (1- Penetration) * 52 * NumDecks:
            self.deck = Deck(num_decks= NumDecks)   
            self.deck.shuffle()
            self.rc = 0

        for hand in self.player_hands:
            card = self.deck.deal_card()
            hand.add_card(card)
            

        ## TBU
        #for hand in self.other_players:
            #hand.add_card(self.deck.deal_card())    

        self.dealer.add_card(self.deck.deal_card())
        self.dealer_upcard = self.dealer.cards[0]
        

        for hand in self.player_hands:
            card = self.deck.deal_card()
            hand.add_card(card)
            

        ## TBU
        #for hand in self.other_players:
            #hand.add_card(self.deck.deal_card())

        self.dealer.add_card(self.deck.deal_card())

    def hit(self, hand):
        card = self.deck.deal_card()    
        hand.add_card(card)
        
    
    def split(self, hand):

        new_hand = Hand(bet = hand.bet)
        new_hand.add_card(hand.cards.pop())
        new_1 = self.deck.deal_card()
        new_2 = self.deck.deal_card()   
        hand.add_card(new_1)
        new_hand.add_card(new_2)
        self.player_hands.append(new_hand) 

        

    def optimal_strategy(self, hand):
        tc = self.rc/(len(self.deck.cards) / 52) if len(self.deck.cards) > 0 else 0
        value = hand.value()
        du = self.dealer_upcard
        # Soft Hand Values

        if "A" in hand.cards:
            if value >= 19:
                return "S"
            if value == 18:
                if du in ['2','7','8']:
                    return "S"
                elif du in ['3','4','5','6']:
                    return "D"
                else:
                    return "H"
            if value == 17:
                if du == '2':
                    return "S"
                elif du in ['3','4','5','6']:
                    return "D"
                else:
                    return "H"
            if value >= 15:

                # deviation at 16-10 and 16-9
                if value == 16:
                    if (du == '10' and tc >= 1) or (du == '9' and tc >= 5):
                        return "S"
                #deviation at 15-10
                elif value == 15:
                    if du == '10' and tc >= 4:
                        return "S"
                    

                elif du in ['4','5','6']:
                    return "D"
                else:
                    return "H"
            if value >= 13:
                if du in ['5','6']:
                    return "D"
                else:
                    return "H"
                
        # Pair Values
        if hand.can_split():
            if hand.cards[0] == "A" or hand.cards[0] == "8":
                return "SP"
            if hand.cards[0] == "10":
    
                # deviation at 10-10-5 and 10-10-6
                if (du == '5' and tc >= 5) or (du == '6' and tc >= 4):
                    return "SP"
                else:
                    return "S"
                
            if hand.cards[0] == "9":
                if du in ['7','10','A']:
                    return "S"
                else:
                    return "SP"
            if hand.cards[0] == "7":
                if du in ['8','9','10','A']:
                    return "H"
                else:
                    return "SP"
            if hand.cards[0] == "6":
                if du in ['7','8','9','10','A']:
                    return "H"
                else:
                    return "SP"
            if hand.cards[0] == "5":
                if du in ['10','A']:
                    return "H"
                else:
                    return "D"
            if hand.cards[0] == "4":
                if du in ['5','6']:
                    return "SP"
                else:
                    return "H"
            if hand.cards[0] == "3" or hand.cards[0] == "2":
                if du in ['8','9','10','A']:
                    return "H"
                else:
                    return "SP"

        # Hard Hand Values 
        if value >= 17:
            return "S"
        if value >= 13:

            # deviation at 13-2 and 13-3
            if value == '13' and du == '2' and tc <= -1:
                return "H"
            elif value == '13' and du == '3' and tc <= -2:
                return "H"

            elif du in ['2','3','4','5','6']:
                return "S"
            else:
                return "H"
        if value == 12:

            # Deviation at 12-2 and 12-3
            if (du =='2' and tc >= 3) or (du == '3' and tc >= 2):
                return "S"

            # Deviation at 12-4, 12-5, and 12-6
            elif (du == '4' and tc <= 0) or (du == '5' and tc <= -2) or (du == '6' and tc <= -1):
                return "H"

            elif du in ['4','5','6']:
                return "S"
            else:
                return "H"
        if value == 11:
            if du == 'A':
                # Deviation at 11-A
                if tc >= 1:
                    return "D"
                else:
                    return "H"
            else:
                return "D"
        if value == 10:

            # deviation at 10-10 and 10-A
            if du in ['10', 'A'] and tc >= 4:
                return "D"
            
            elif du in ['10','J','Q','K','A']:
                return "H"
            else:
                return "D"
        if value == 9:
            if du in ['3','4','5','6']:
                return "D"

            # deviation at 9-2 and 9-7
            elif du == '2' and tc >= 1:
                return "D"
            elif du == '7' and tc >= 3:
                return "D"
            
            else:
                return "H"
        if value >= 5:
            return "H"
        
    


    def player_play(self):
        index = 0
        while index < len(self.player_hands):
            hand = self.player_hands[index]
            
            while True:
                if len(self.player_hands) > 1:
                    print(f"P{index + 1}: ", hand.cards)
                else:
                    print("P: ", hand.cards)    
                #hand.bet = self.kelly_citerion(hand)
                action = self.optimal_strategy(hand) 

                if hand.blackjack():
                    break
                elif hand.bust():
                    break
                elif action == "H":
                    print("Hit")
                    self.hit(hand)
                    if hand.bust():
                        break
                    
                elif action == "S":
                    print("Stand")
                    break
                elif action == "D":
                    print("Double Down")
                    hand.double_down()
                    self.hit(hand)

                    if hand.bust():
                        break
                elif action == "SP":
                    print("Split")
                    if hand.can_split():
                        self.split(hand)
                        index = -1
                    else:
                        print("Cannot split")
            index += 1           
            

    def dealer_hits(self):
        value = self.dealer.value()
        if self.dealer.blackjack():
            return False

        if value < 17 or (value == 17 and Soft17 and any(card == 'A' for card in self.dealer.cards)):
            return True
        else:
            return False
            

    def dealer_play(self):
        while self.dealer_hits():
            print("DH")
            self.hit(self.dealer)
            print("D: ", self.dealer.cards)
        
    
    def winner(self, hand):
        print("______________________")

        if self.dealer.blackjack() and not hand.blackjack():
            print("DBJ")
            self.outcomes.append(-1)
            self.dealer_wins += 1
            self.bankroll -= hand.bet
        elif hand.blackjack() and not self.dealer.blackjack():
            print("PBJ")
            self.outcomes.append(1.5)
            self.player_wins += 1
            self.bankroll += hand.bet * 1.5 
        # blackjack push
        elif hand.blackjack() and self.dealer.blackjack():
            print("BJPush")
            self.outcomes.append(0)
            self.ties += 1
        elif hand.bust():
            print("PBust")
            self.outcomes.append(-1)
            self.dealer_wins += 1
            self.bankroll -= hand.bet   
        elif self.dealer.bust():
            print("DBust")
            self.outcomes.append(1)
            self.player_wins += 1
            self.bankroll += hand.bet   
        elif hand.value() > self.dealer.value():
            print("PWin")
            self.outcomes.append(1)    
            self.player_wins += 1
            self.bankroll += hand.bet   
        elif hand.value() < self.dealer.value():
            print("DWin")    
            self.outcomes.append(-1)
            self.dealer_wins += 1
            self.bankroll -= hand.bet   
        # natural push
        else:
            print("NPush")
            self.ties += 1
            self.outcomes.append(0)
            
    def play_game(self):
        bet = self.kelly_citerion()    
        self.deal()  
        print("\n\nDUp: ", self.dealer_upcard) 
        self.player_play()
        if not any(hand.bust() for hand in self.player_hands):
            self.dealer_play()

        for card in self.dealer.cards:
            self.count_card(card)
    
        for hand in self.player_hands:
            hand.bet = bet   
            self.bets.append(hand.bet)  
            for card in hand.cards:
                self.count_card(card)
            
            self.winner(hand)
            print("bet size: ", round(hand.bet))
            print("cards left in deck: ", len(self.deck.cards))
            print("running count: ", self.rc, "true count: ", (round(self.rc/(len(self.deck.cards) / 52), 2) if len(self.deck.cards) > 0 else 0)) 
            
        

   
def simulate(ngames):
    player_wins = 0
    dealer_wins = 0
    ties = 0
    bankroll = InitBankRoll
    deck = Deck(num_decks= NumDecks)
    deck.shuffle()
    run_count = 0
    bets = []
    outcomes = []
    bankrolls = []   

    for _ in range(ngames):
        
        game = Game(running_count=run_count, deck = deck, num_decks= NumDecks, bet=BetSize, player_wins=0, dealer_wins=0, ties=0, init_bankroll=bankroll)
        game.play_game()
        
        player_wins += game.player_wins
        dealer_wins += game.dealer_wins
        ties += game.ties
        bankroll = game.bankroll
        bankrolls.append(bankroll)
        deck = game.deck
        run_count = game.rc
        bets += game.bets
        outcomes += game.outcomes   
        
        
        print("new bankroll: ", round(bankroll, 2))
        print("______________________")

    EVs = [bet * outcome for bet, outcome in zip(bets, outcomes)]
    
    pwin = round(player_wins / (player_wins + dealer_wins + ties) * 100, 3)
    dwin = round(dealer_wins / (player_wins + dealer_wins + ties) * 100, 3) 
    avgEV = 1 + round(sum(EVs)/len(EVs),2) 
    print(f"\nAfter {ngames} Games ... \nTotal Player Wins: ", player_wins, "\nTotal Dealer Wins: ", dealer_wins, "\nTotal Ties: ", ties, "\nFinal Bankroll: ", round(bankroll))  
    print("player win percentage: ", pwin, "%")
    print("dealer win percentage: ", dwin, "%")
    print("avg. EV per $1 bet: $", avgEV)
    return bankrolls, pwin, avgEV

if __name__ == "__main__":
   
    plt.figure(1)
    for i in range(1,10):
         AgressionFactor = i/10
         results = simulate(NumGames)
         bankrolls = results[0]
         pwin = results[1]
         ev = results[2]    
         plt.plot(bankrolls, label= f"Kelly Agr.: {AgressionFactor}, PWin %: {pwin}, EV on $1: {round(ev, 1)}")   
    plt.legend()
    plt.xlabel("Number of Games")
    plt.ylabel("Bankroll")
     
    plt.figure(2)
    AgressionFactor = 0.4
    for i in range(2,10):
         NumDecks = i
         results = simulate(NumGames)
         bankrolls = results[0]
         pwin = results[1]
         ev = results[2]    
         plt.plot(bankrolls, label= f"NumDecks: {NumDecks}, PWin %: {pwin}, EV on $1: {round(ev, 1)}")   
    plt.legend()
    plt.xlabel("Number of Games")
    plt.ylabel("Bankroll")
    plt.show()  

