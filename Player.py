from Strategy import Strategy

strategy_file = Strategy('data.csv')
HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = strategy_file.get_st()

class Player:
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
                    hand.doubled = True
                    self.hit(hand, shoe)
                    break
                else:
                    flag = 'H'

            if flag == 'Sr':
                if hand.length() == 2:
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

    def split(self, hand, shoe):
        self.hands.append(hand.split())
        self.play_hand(hand, shoe)