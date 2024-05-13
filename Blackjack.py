from Containers import Hand, Shoe
from Dealer import Dealer
from Player import Player

GAMES = 500000
SHOE_SIZE = 2
SHOE_PENETRATION = 0.25
BET_SPREAD = 50
DECK_SIZE = 52

class Game:
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.shoe = Shoe(SHOE_SIZE, SHOE_PENETRATION, DECK_SIZE)

        self.money = 0.0
        self.bet = 0.0
        self.stake = 1.0

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
            self.stake = BET_SPREAD
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
    
if __name__ == "__main__":
    money = []
    bets = []
    countings = []
    nb_hands = 0
    
    for g in range(GAMES):
        game = Game()
        while not game.shoe.reshuffle:
            game.play_round()
            nb_hands += 1

        money.append(game.get_money())
        bets.append(game.get_bet())
        countings += game.shoe.count_history

        print("Game %d: %s (%s bet)" % (g + 1, "{0:.2f}".format(game.get_money()), "{0:.2f}".format(game.get_bet())))

    money_won = sum(money)
    bet_volume = sum(bets)
    print("-" * 30)
    print("Money Won: ${:,.2f}".format(money_won))
    print("Bet Volume: ${:,.2f}".format(bet_volume))
    print("Overall winnings: ${} (EDGE = {} %)".format("{0:.2f}".format(money_won), "{0:.3f}".format(100.0 * money_won/bet_volume)))