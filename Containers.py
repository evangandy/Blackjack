import random

CARDS = {
    "Ace": 11,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

ST = {
    "Ace": 0,
    "Two": 1,
    "Three": 1,
    "Four": 2,
    "Five": 2,
    "Six": 2,
    "Seven": 1,
    "Eight": 0,
    "Nine": -1,
    "Ten": -2,
    "Jack": -2,
    "Queen": -2,
    "King": -2
}

class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.name)

class Hand:
    def __init__(self, cards):
        self.splithand = False
        self.surrender = False
        self.doubled = False
        self.cards = cards

    def __str__(self):
        h = ""
        for c in self.cards:
            h += "%s " % c
        return h

    def value(self):
        self._value = 0
        for c in self.cards:
            self._value += c.value

        if self._value > 21 and self.aces_soft() > 0:
            for ace in self.aces():
                if ace.value == 11:
                    self._value -= 10
                    ace.value = 1
                    if self._value <= 21:
                        break

        return self._value

    def aces(self):
        self._aces = []
        for c in self.cards:
            if c.name == "Ace":
                self._aces.append(c)
        return self._aces

    def aces_soft(self):
        self._aces_soft = 0
        for ace in self.aces():
            if ace.value == 11:
                self._aces_soft += 1
        return self._aces_soft

    def soft(self):
        if self.aces_soft() > 0:
            return True
        else:
            return False

    def splitable(self):
        if self.length() == 2 and self.cards[0].name == self.cards[1].name:
            return True
        else:
            return False

    def blackjack(self):
        if not self.splithand and self.value() == 21:
            if self.length() == 2:
                return True
            else:
                return False
        else:
            return False

    def busted(self):
        if self.value() > 21:
            return True
        else:
            return False

    def add_card(self, card):
        self.cards.append(card)

    def split(self):
        self.splithand = True
        c = self.cards.pop()
        new_hand = Hand([c])
        new_hand.splithand = True
        return new_hand

    def length(self):
        return len(self.cards)

class Shoe:
    reshuffle = False

    def __init__(self, num_decks, sp, deck_size):
        self.num_decks = num_decks
        self.sp = sp
        self.deck_size = deck_size
        
        self.count = 0
        self.count_history = []
        self.ideal_count = {}
        
        self.cards = self.init_cards()
        self.init_count()

    def __str__(self):
        s = ""
        for c in self.cards:
            s += "%s\n" % c
        return s

    def init_cards(self):
        self.count = 0
        self.count_history.append(self.count)

        cards = []
        for d in range(self.num_decks):
            for c in CARDS:
                for i in range(0, 4):
                    cards.append(Card(c, CARDS[c]))
        random.shuffle(cards)
        return cards

    def init_count(self):
        for card in CARDS:
            self.ideal_count[card] = 4 * self.num_decks

    def deal(self):
        if self.shoe_penetration() < self.sp:
            self.reshuffle = True
        card = self.cards.pop()

        self.ideal_count[card.name] -= 1

        self.do_count(card)
        return card

    def do_count(self, card):
        self.count += ST[card.name]
        self.count_history.append(self.truecount())

    def truecount(self):
        return self.count / (self.num_decks * self.shoe_penetration())

    def shoe_penetration(self):
        return len(self.cards) / (self.deck_size * self.num_decks)