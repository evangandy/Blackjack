from Containers import Hand, Shoe
from Dealer import Dealer
from Player import Player

class Game:
    def __init__(self, games, shoe_size, shoe_penetration, bet_spread, deck_size):
        self.player = Player()
        self.dealer = Dealer()
        self.shoe = Shoe(shoe_size, shoe_penetration, deck_size)

        self.money = 0.0
        self.bet = 0.0
        self.stake = 1.0

        self.games = games
        self.shoe_size = shoe_size
        self.shoe_penetration = shoe_penetration
        self.bet_spread = bet_spread
        self.deck_size = deck_size

    def winnings(self, hand):
        win = 0.0
        bet = self.stake
        if not hand.surrender:
            if hand.busted():
                status = "LOST"
            else:
                if hand.blackjack():
                    if self.dealer.hand.blackjack():
                        status = "PUSH"
                    else:
                        status = "WON 3:2"
                elif self.dealer.hand.busted():
                    status = "WON"
                elif self.dealer.hand.value() < hand.value():
                    status = "WON"
                elif self.dealer.hand.value() > hand.value():
                    status = "LOST"
                elif self.dealer.hand.value() == hand.value():
                    if self.dealer.hand.blackjack():
                        status = "LOST"  # player's 21 vs dealers blackjack
                    else:
                        status = "PUSH"
        else:
            status = "SURRENDER"

        if status == "LOST":
            win += -1
        elif status == "WON":
            win += 1
        elif status == "WON 3:2":
            win += 1.5
        elif status == "SURRENDER":
            win += -0.5
        if hand.doubled:
            win *= 2
            bet *= 2

        win *= self.stake

        return win, bet
    
    def play_round(self):
        if self.shoe.truecount() > 6:
            self.stake = self.bet_spread
        else:
            self.stake = 1.0

        player_hand = Hand([self.shoe.deal(), self.shoe.deal()])
        dealer_hand = Hand([self.shoe.deal()])
        
        self.player.set_hands(player_hand, dealer_hand)
        self.dealer.set_hand(dealer_hand)

        self.player.play(self.shoe)
        self.dealer.play(self.shoe)

        for hand in self.player.hands:
            win, bet = self.winnings(hand)
            self.money += win
            self.bet += bet

    def get_money(self):
        return self.money

    def get_bet(self):
        return self.bet