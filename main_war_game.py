# "War" Card Game

# Library imports
from random import shuffle

# Define the cards in the game using class
class Card:
    suits = {1: "Spades",
             2: "Hearts",
             3: "Diamonds",
             4: "Clubs"
             }

    values = {2: "2",
               3: "3",
               4: "4",
               5: "5",
               6: "6",
               7: "7",
               8: "8",
               9: "9",
               10: "10",
               11: "Jack",
               12: "Queen",
               13: "King",
               14: "Ace"
               }
    
    def __init__(self, v, s):
        # Suits and Values are ints
        self.value = v
        self.suit = s
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value

    def __gt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value > other.value

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value < other.value
    
    def __repr__(self):
        card_name = self.values[self.value] + " of " \
        + self.suits[self.suit]
        return card_name

# Define a randomly shuffled deck using class
class Deck():
    def __init__(self):
        self.cards = []

        for i in range(2, 15):
            for j in range(1, 5):
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def deal(self):
        return self.cards[:26], self.cards[26:]
    
# Define everything that needs to be logged per player using class
class Player():
    def __init__(self, name, hand=None):
        self.name = name
        self.wins = 0
        self.stack = hand or []

# Define the game itself using class
class Game():
    def __init__(self):
        name1 = input("Player 1's name:")
        name2 = input("Player 2's name:")
        
        self.deck = Deck()
        hand1, hand2 = self.deck.deal()
        
        self.p1 = Player(name1, hand1)
        self.p2 = Player(name2, hand2)

    def wins(self, winner):
        win_msg = f"\033[1;4m{winner}\033[0m \033[1mwins\033[0m this battle!\n--------------------\n"
        print(win_msg)

    def draw_msg(self, p1n, p1c, p2n, p2c):
        draw_msg = f"\033[3m{p1n} drew {p1c},\n{p2n} drew {p2c}.\033[0m\n"
        print(draw_msg)

    def tie_draw_msg(self, p1n, p1comp, p2n, p2comp):
        tie_draw_msg = f"\033[3m{p1n} drew {p1comp} as their war card, \n{p2n} drew {p2comp} as their card.\033[0m\n"
        print(tie_draw_msg)
    
    def tie_win_msg(self, winner_name):
        print(f"{winner_name} has won the war and takes all the spoils back to their camp!\n====================\n--------------------\n")
    
    def tie_tie_msg(self, p1n, p2n, comp):
        article = "an" if comp[0].lower() in "aeio8" else "a"
        print(f"====================\nBoth {p1n} and {p2n} played {article} {comp}, so the war continues...")

    def one_round(self):
        p1c = self.p1.stack.pop(0)
        p2c = self.p2.stack.pop(0)
        p1n = self.p1.name
        p2n = self.p2.name
        self.draw_msg(p1n, p1c, p2n, p2c)

        if p1c > p2c:
            self.p1.stack.extend([p1c, p2c])
            self.p1.wins += 1
            self.wins(p1n)
        elif p2c > p1c:
            self.p2.stack.extend([p1c, p2c])
            self.p2.wins += 1
            self.wins(p2n)
        elif p1c == p2c:
            self.tie_resolve(p1n, p1c, p2n, p2c)
        
    def tie_stack(self, no_burn = False):
        if no_burn:
            comp_card1 = self.p1.stack.pop(0)
            comp_card2 = self.p2.stack.pop(0)
            return comp_card1, comp_card2
        else:
            burn_card1 = self.p1.stack.pop(0)
            comp_card1 = self.p1.stack.pop(0)
            burn_card2 = self.p2.stack.pop(0)
            comp_card2 = self.p2.stack.pop(0)
            return burn_card1, comp_card1, burn_card2, comp_card2
    
    def check_war_cards(self, stack_p1, stack_p2):
        players = [(self.p1.name, len(stack_p1)), (self.p2.name, len(stack_p2))]

        game_end = False
        no_burn = False

        for name, count in players:
            if count >= 2:
                continue
            
            if count == 1:
                print(f"{name} is on their last card. This round of war will be played without a burner card. Better make it count!")
                no_burn = True
            elif count == 0:
                print(f"{name} has run out of cards to use in the war...\n--------------------")
                game_end = True
            else:
                raise ValueError(f"Invalid card count ({count}) for player '{name}'. Expected >= 0.")

        return game_end, no_burn

    def tie_resolve(self, p1n, p1c, p2n, p2c):
        print(f"Both players had a {p1c.value}, it's a tie...\nWar has broken out!\n----------------\n")
        spoils = [p1c, p2c]

        tie_repeat = True

        while tie_repeat:
            print(f"Tied stack p1: {len(self.p1.stack)}")
            print(f"Tied stack p2: {len(self.p2.stack)}")
            game_end, no_burn = self.check_war_cards(self.p1.stack, self.p2.stack)

            if game_end:
                return
            if no_burn:
                comp_card1, comp_card2 = self.tie_stack(no_burn)
                spoils.extend([comp_card1, comp_card2])
            elif not no_burn:
                burn_card1, comp_card1, burn_card2, comp_card2 = self.tie_stack(no_burn)
                spoils.extend([burn_card1, comp_card1, burn_card2, comp_card2])
            
            self.tie_draw_msg(p1n, comp_card1, p2n, comp_card2)

            if comp_card1 > comp_card2:
                self.p1.stack.extend(spoils)
                self.tie_win_msg(p1n) 
                tie_repeat = False
            elif comp_card2 > comp_card1:
                self.p2.stack.extend(spoils)
                self.tie_win_msg(p2n)
                tie_repeat = False
            elif comp_card1 == comp_card2:
                self.tie_tie_msg(p1n, p2n, "comp_card1.value")
                tie_repeat = True

    def play_game(self):
        print(f"\033[1mA large-scale war between {self.p1.name} and {self.p2.name} has begun!\033[0m")

        simulate = False
        
        while self.p1.stack and self.p2.stack:
            print(len(self.p1.stack), len(self.p2.stack))

            if not simulate:
                response = input("Press q to quit, s to simulate, or press any other key to play:")
            if response == "s":
                simulate = True
            if response == "q":
                print("Quitters will amount to nothing in life! Bye bye :)")
                return
            
            print("--------------------\nA new battle commences, draw your weapons!\n")
            
            self.one_round()
        
        win = self.determine_winner()
        if win == None:
            print("A terrible mistake took place as no winner can be determined, rendering this war pointless... Sorry, not sorry :)")
            return
        print(f"All battles have been fought, the war is over.\n\n\033[1;4m{win.upper()}\033[0m WINS and takes ALL spoils home!\n====================")
        return
    
    def determine_winner(self):
        if not self.p1.stack and not self.p2.stack:
            return None # Return different something in order to make a 
                        # tie breaker to resultingly determine the actual winner
        if not self.p2.stack:
            return self.p1.name
        if not self.p1.stack:
            return self.p2.name
        else:
            return None

# Run the "war" game:
game = Game()
game.play_game()

