from Containers import Hand, Shoe
from Strategy import Strategy

GAMES = 20000
SHOE_SIZE = 6
SHOE_PENETRATION = 0.25
BET_SPREAD = 20
DECK_SIZE = 52

strategy_file = Strategy('data.csv')
HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = strategy_file.get_st()

class Dealer:
    def __init__(self, hand=None):
        self.hand = hand

    def set_hand(self, new_hand):
        self.hand = new_hand

    def play(self, shoe):
        while self.hand.value() < 17:
            self.hit(shoe)

    def hit(self, shoe):
        c = shoe.deal()
        self.hand.add_card(c)

class Player(object):
    def __init__(self, hand=None, dealer_hand=None):
        self.hands = [hand]
        self.dealer_hand = dealer_hand

    def set_hands(self, new_hand, new_dealer_hand):
        self.hands = [new_hand]
        self.dealer_hand = new_dealer_hand

    def play(self, shoe):
        for hand in self.hands:
            self.play_hand(hand, shoe)

    def play_hand(self, hand, shoe):
        if hand.length() < 2:
            if hand.cards[0].name == "Ace":
                hand.cards[0].value = 11
            self.hit(hand, shoe)

        while not hand.busted() and not hand.blackjack():
            if hand.soft():
                flag = SOFT_STRATEGY[hand.value()][self.dealer_hand.cards[0].name]
            elif hand.splitable():
                flag = PAIR_STRATEGY[hand.value()][self.dealer_hand.cards[0].name]
            else:
                flag = HARD_STRATEGY[hand.value()][self.dealer_hand.cards[0].name]

            if flag == 'D':
                if hand.length() == 2:
                    # print "Double Down"
                    hand.doubled = True
                    self.hit(hand, shoe)
                    break
                else:
                    flag = 'H'

            if flag == 'Sr':
                if hand.length() == 2:
                    # print "Surrender"
                    hand.surrender = True
                    break
                else:
                    flag = 'H'

            if flag == 'H':
                self.hit(hand, shoe)

            if flag == 'P':
                self.split(hand, shoe)

            if flag == 'S':
                break

    def hit(self, hand, shoe):
        c = shoe.deal()
        hand.add_card(c)
        # print "Hitted: %s" % c

    def split(self, hand, shoe):
        self.hands.append(hand.split())
        self.play_hand(hand, shoe)

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
    game = Game()
    game.play_round()