##########################################
# CARD GAME: WAAAAAAAAR
##########################################
# Library imports
import random
from random import shuffle

##########################################
# Card class definition
##########################################
class Functions:
    def __init__ (self):
        pass

    def ask_yes_no(question, default = True):
        while True:
            resp = input(question + " [Y/N]: ").strip().lower()
            if not resp:
                print("No option was chosen: sticking to default settings.")
                return default
            if resp[0] in ("y", "n"):
                return resp[0] == "y"
            print("Please input Yes (Y), or No (N) only.")

    def list_msg(cards):
        list = [f"[{i}]: {card}"
                for i, card in enumerate(cards, start = 1)]
        list_str = ",\n".join(list)
        return list_str

class Card:
    suits = {1: "Spades",
             2: "Hearts",
             3: "Diamonds",
             4: "Clubs",
             5: "Joker"
             }

    values = {2: "2", 3: "3", 4: "4", 5: "5", 
              6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 
              11: "Jack", 12: "Queen", 13: "King", 14: "Ace",
              15: "Joker"
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
        if self.value == 15:
            card_name = "Joker"
        else:
            card_name = self.values[self.value] + " of " \
            + self.suits[self.suit]
        return card_name

##########################################
# Deck class definition
##########################################
class Deck():
    def __init__(self):
        self.cards = []

        for i in range(2, 15):
            for j in range(1, 5):
                self.cards.append(Card(i, j))

        self.use_jokers = self.joker_flags()

        if self.use_jokers:
            self.cards.extend([Card(15, 5), Card(15, 5)])
            print("Jokers were successfully added!")
        else:
            print("No Jokers were added!")

        shuffle(self.cards)

    def joker_flags(self):
        print("Do you want to play with jokers?\n"
              "\033[3m(Default selection is:\033[0m \033[1;3mno rules\033[0m \033[3mshown, and \033[1;3mjokers excluded\033[0m\033[3m)\033[0m")
        show_rules = Functions.ask_yes_no("Do you want to see the rules of the jokers?", default=False)
        if show_rules:
            print("JOKER EXPLANATION PLACEHOLDER")
        use_jokers = Functions.ask_yes_no("Do you want to play with jokers included?", default=False)
        return use_jokers
            
    def deal(self):
        if self.use_jokers:
            return self.cards[:27], self.cards[27:]
        else:
            return self.cards[:26], self.cards[26:]
    
##########################################
# Player class definition
##########################################
class Player():
    def __init__(self, name, stack, hand, refill = True):
        self.name = name
        self.stack = stack
        self.hand = hand
        if refill == True:
            self.refill_hand()

    def refill_hand(self):
        self.slots = 5 - len(self.hand)
        self.to_hand = min(self.slots, len(self.stack))
        for _ in range(self.to_hand):
            self.hand.append(self.stack.pop(0))
    
    # Player message print statements
    def hand_msg(self, first = False, war = False, burn = True):
        numbered_hand = [f"[{i}]: {card}"
                       for i, card in enumerate(self.hand, start = 1)]
        hand_str = ",\n".join(numbered_hand)

        if first == True:
            print(f"\n\033[1m{self.name}\033[0m, you start with the following hand:\n{hand_str}")
        elif first == False and war == False:
            print(f"\n\033[1m{self.name}\033[0m, your hand for this round is:\n{hand_str}")
        elif first == False and war == True and burn == True:
            print(f"\n\033[1m{self.name}\033[0m, your hand to select a burn card from is:\n{hand_str}")
        elif first == False and war == True and burn == False:
            print(f"\n\033[1m{self.name}\033[0m, your hand to select a playing card from is:\n{hand_str}")

##########################################
# Game class definition
##########################################
class Game():
    def __init__(self):
        self.simulate = False

        self.name1 = input("\033[1;4mPlayer 1\033[0m\033[1m, enter your username:\033[0m")
        self.name2 = input("\033[1;4mPlayer 2\033[0m\033[1m, enter your username:\033[0m")

        self.deck = Deck()

        self.stack1, self.stack2 = self.deck.deal()

        print(f"\n\033[1mA large-scale war between {self.name1} and {self.name2} has begun!\033[0m")

        self.play_game(self.name1, self.stack1, self.name2, self.stack2)

##########################################
# GAME LOOP
##########################################
    def play_game(self, name1, stack1, name2, stack2, hand1 = [], hand2 = [], test_game = False):

        if test_game:
            self.p1 = Player(name1, stack1, hand1)
            self.p2 = Player(name2, stack2, hand2)
        elif not test_game:
            self.p1 = Player(self.name1, self.stack1, [])
            self.p2 = Player(self.name2, self.stack2, [])
        else:
            print("error")
            return

        self.win = False

        round = 1

        while not self.win:

            if not self.simulate:
                response = input("\n\033[3mPress\033[0m \033[1;3mq\033[0m \033[3mto quit,\033[0m \033[1;3ms\033[0m \033[3mto simulate, or press\033[0m \033[1;3many other key\033[0m \033[3mto play:\033[0m")
            if response == "s":
                self.simulate = True
            if response == "q":
                print("Quitters will amount to nothing in life! Bye bye :)")
                return
            
            print(f"--------------------\nBattle {round} commences, draw your weapons!\n")
            round += 1

            self.one_round()

            for p in (self.p1, self.p2):
                self.hand_redeal(p)


##########################################
# Round definition
##########################################
    def one_round(self):
        p1n, p2n = self.p1.name, self.p2.name

        p1c, p2c = self.card_choice(p1n, p2n)
        
        for p in (self.p1, self.p2):
            if p1c > p2c:
                self.p1.stack.extend([p1c, p2c])
                self.win_msg(p1n)
                p.refill_hand()
            elif p2c > p1c:
                self.p2.stack.extend([p1c, p2c])
                self.win_msg(p2n)
                p.refill_hand()
            elif p1c == p2c:
                self.war_resolve(p1n, p1c, p2n, p2c)
                p.refill_hand()

        self.win, winner = self.determine_winner()

        if self.win == None:
            print("The messenger was killed: no winner can be determined, rendering this war pointless... Sorry, not sorry :)")
            return
        elif self.win == False:
            return
        elif self.win == True:
            print(f"All battles have been fought, the war is over.\n\n\033[1;4m{winner.upper()}\033[0m WINS everything, and takes ALL spoils home!\n====================")
        return

    def card_choice(self, p1n, p2n):
        chosen = []
        for p in (self.p1, self.p2):
            while True:
                if not self.simulate:
                    p.hand_msg()
                    print(self.p1.hand, self.p2.hand)
                    prompt = f"\033[1m{p.name}\033[0m, choose a card (1-{len(p.hand)}): "

                    try:
                        idx = int(input(prompt)) 
                        if idx not in range(1, len(p.hand) + 1):
                            raise IndexError
                    except ValueError:
                        print("Please enter a number.")
                        continue
                    except IndexError:
                        print(f"Choose a number between 1 and {len(p.hand)}")
                        continue
                    break
                elif self.simulate:
                    idx = random.choice(range(1, len(p.hand) + 1))
                    break
            chosen.append(p.hand.pop(idx - 1))
        p1c, p2c = chosen

        print(f"\n--------------------\n{p1n} chose: {p1c}")
        print(f"{p2n} chose: {p2c}\n")

        return p1c, p2c

##########################################
# Message print statements
##########################################

    def win_msg(self, winner):
        win_msg = f"\033[1;4m{winner}\033[0m \033[1mwins\033[0m this battle!\n--------------------\n"
        print(win_msg)

    def draw_msg(self, p1n, p1c, p2n, p2c):
        draw_msg = f"\033[3m{p1n} drew {p1c},\n{p2n} drew {p2c}.\033[0m\n"
        print(draw_msg)

    def war_draw_msg(self, p1n, p1comp, p2n, p2comp):
        war_draw_msg = f"\n\033[3m{p1n} chose {p1comp} as their war card, \n{p2n} chose {p2comp} as theirs.\033[0m\n"
        print(war_draw_msg)
    
    def war_win_msg(self, winner_name):
        print(f"\033[1m{winner_name}\033[0m has won the war and takes all the spoils back to their camp!\n====================\n--------------------\n")

    def war_refill_msg(self, name, to_hand, to_stack, winner, to_spoils=None):
        print("war refill message entered...")
        if winner:
            if not to_spoils:
                hand_str = Functions.list_msg(to_hand)
                stack_str = Functions.list_msg(to_stack)

                if len(to_hand) == 1:
                    hand_text = f"\033[1m{name}\033[0m, the following, single, card was added to your hand: \033[1m{hand_str}\033[0m.\n"
                    stack_text = f"No cards were added to your stack..."
                    print(hand_text, stack_text)
                elif len(to_hand) > 1:
                    hand_text = f"\033[1m{name}\033[0m, the following, \033[1m{len(to_hand)}\033[0m, cards were added to your hand: \n\033[1m{hand_str}\033[0m.\n"
                    stack_text = f"The following \033[1m{len(to_stack)}\033[0m cards were added to the bottom of your stack:\n\033[1m{stack_str}\033[0m"
                    print(hand_text, stack_text)
            
            elif to_spoils:
                try: 
                    if not to_spoils:
                        raise ValueError
                except ValueError:
                    print("This option shouldn't exist")
                    print(name, to_hand, to_stack, winner, to_spoils)
                    return
                
        elif not winner:
            if not to_spoils:
                print(f"\033[1m{name}\033[0m, you lost, so, unfortunately, you do not receive any cards from this war...")

            elif to_spoils:
                spoils_str = Functions.list_msg(to_spoils)
                print(f"All cards played in this war, so far, have been added to spoils:\n{spoils_str}")
        
    def war_tie_msg(self, p1n, p2n, comp_card):
        comp_name = Card.values[comp_card]
        article = "an" if comp_name[0].lower() in ("a", "8") else "a"
        print(f"====================\nBoth {p1n} and {p2n} played {article} {comp_name}, so the war continues...")

##########################################
# War scenario methods
##########################################
    def war_resolve(self, p1n, p1c, p2n, p2c):
        print(f"Both players had a {p1c.value}, it's a tie...\n\n\033[1mWar has broken out!\033[0m\n----------------")
        spoils = [p1c, p2c]

        war_repeat = True
        
        while war_repeat:
            game_end, burn_flags = self.war_cards_check(self.p1.stack, self.p1.hand, self.p2.stack, self.p2.hand)

            if game_end:
                return

            burn_flag_p1 = burn_flags[self.p1]
            burn_flag_p2 = burn_flags[self.p2]

            burn_cards, war_cards = self.war_card_choice(burn_flag_p1, burn_flag_p2)
            
            spoils.extend(burn_cards)

            comp_card1, comp_card2 = war_cards
            
            self.war_draw_msg(p1n, comp_card1, p2n, comp_card2)
            
            #### JOKER LOGIC
            for card in (comp_card1, comp_card2):
                if card.value == 15:
                    pass

            extend = (spoils + war_cards)
            
            if comp_card1 > comp_card2:
                self.p1.stack.extend(extend)
                print("extend:", extend)

                num_won = len(extend) - len(self.p1.hand) - 1
                to_stack = extend[num_won:]
                to_hand = extend[:num_won]

                # ADD CHOICE FOR WHICH CARDS TO ADD TO HAND, REST GOES TO STACK

                self.war_win_msg(self.p1.name)

                self.war_refill_msg(p1n, to_hand, to_stack, winner=True)
                self.war_refill_msg(p2n, to_hand, to_stack, winner=False) 

                war_repeat = False

            elif comp_card2 > comp_card1:
                self.p2.stack.extend(extend)
                print("extend:", extend)

                num_won = len(extend) - len(self.p2.hand) - 1
                to_stack = extend[num_won:]
                to_hand = extend[:num_won]
                
                # ADD CHOICE FOR WHICH CARDS TO ADD TO HAND, REST GOES TO STACK

                self.war_win_msg(self.p2.name)

                self.war_refill_msg(p2n, to_hand, to_stack, winner=True) 
                self.war_refill_msg(p1n, to_hand, to_stack, winner=False)

                war_repeat = False

            elif comp_card1 == comp_card2:
                to_spoils = [comp_card1, comp_card2]

                print("war_resolve further tie:", to_spoils, "(to_spoils)", extend, "extend")

                spoils.extend(to_spoils)
                self.war_tie_msg(p1n, p2n, comp_card1.value)
                self.war_refill_msg("war_tie", extend, to_stack = None, winner=False, to_spoils=to_spoils)

                war_repeat = True

            for p in (self.p1, self.p2):
                p.refill_hand()   

            for p in (self.p1, self.p2):
                print(f"""{p.name}'stack: {len(p.stack)}: {p.stack},
                      {p.name}'s hand: {len(p.hand)}: {p.hand}\n""")

    def war_card_choice(self, burn1 = True, burn2 = True):
        burn_cards = []
        war_cards = []

        for p, should_burn in zip((self.p1, self.p2), (burn1, burn2)):
                if not should_burn:
                    continue
                
                while True:
                    if not self.simulate:
                        p.hand_msg(first = False, war = True, burn = True)
                        prompt = f"Choose your card (1-{len(p.hand)}): "
                        try:
                            idx = int(input(prompt))
                            if idx not in range(1, len(p.hand) + 1):
                                raise IndexError
                            burn_card = p.hand.pop(idx-1)
                            print(f"burn card ({p.name}):", burn_card)
                            burn_cards.append(burn_card)
                            print("burn cards:", burn_cards)
                            
                        except ValueError:
                            print("Please enter a number.")
                            continue
                        except IndexError:
                            print(f"Choose a number between 1 and {len(p.hand)}.")
                            continue
                        break

                    elif self.simulate:
                        idx = random.choice(range(1, len(p.hand)))
                        break
                    
                # burn_cards.append(p.hand.pop(idx-1))
                # print("ADDED TO BURN CARDS", p.hand.pop(idx-1))

        for p in (self.p1, self.p2):
            while True:
                if not self.simulate:
                    p.hand_msg(first = False, war = True, burn = False)
                    prompt = f"Choose your card (1-{len(p.hand)}): "
                    try:
                        idx = int(input(prompt))
                        if idx not in range(1, len(p.hand) + 1):
                            raise IndexError
                    except ValueError:
                        print("Please enter a number.")
                        continue
                    except IndexError:
                        print(f"Choose a number between 1 and {len(p.hand)}")
                        continue
                    break
                elif self.simulate:
                    idx = random.choice(range(1, len(p.hand) + 1))
                    break

            choice = p.hand.pop(idx - 1)
            war_cards.append(choice)

        return burn_cards, war_cards
    
    def war_cards_check(self, stack1, hand1, stack2, hand2):
        players = [(self.p1, len(hand1), len(stack1)), (self.p2, len(hand2), len(stack2))]

        burn_flags = {}
        game_end = False

        for p, count_hand, count_stack in players:
            if count_hand + count_stack == 0:
                print(f"\033[1m{p.name}\033[0m has run out of cards to use in the war...\n--------------------")
                burn_flags[p] = True
                game_end = True

            elif count_hand + count_stack == 1:
                print(f"\033[1m{p.name}\033[0m is on their last card. They will play this round without a burner card. Better make it count!")
                burn_flags[p] = False

            elif count_hand + count_stack >= 2:
                burn_flags[p] = True

            else:
                raise ValueError(f"Invalid card count ({count_hand + count_stack}) for player \033[1m{p.name}\033[0m. Expected >= 0.")

        return game_end, burn_flags

##########################################
# Special mechanics
##########################################
    def hand_redeal(self, player):
    # Allow the player to exchange all 5 cards in their hand for 5 cards in their stack (or 3 if only 3 cards left in stack, etc.)
    # Allow only 3 times per entire game per player
    # Automatically makes the player lose the round in which they apply this mechanic by taking 1 card randomly from the new hand,
    # and losing that card to the other player regardless of strength of the card.
        if player == self.p1:
            p = self.p1
        elif player == self.p2:
            p = self.p2
        else:
            print("EROROOREOROEO")

        p.hand_red = 0

        if p.hand_red >= 3:
            print(f"{p.name}, you've run out of redeals, stay on top of your game...")
            return
        
        elif p.hand_red < 3:
            prompt = (f"{p.name}, do you want to redeal? You have \033[1m{3 - p.hand_red}/3 times left\033[0m!")
            redeal = Functions.ask_yes_no(prompt, False)
        
        if not redeal:
                print(f"No redeal for {p.name}\n")
                return

        elif redeal < 3:
            print(f"{p.name}'s stack: {p.stack}")
            stack_str = Functions.list_msg(p.stack)
            print(f"Your current stack is: {stack_str}")

            print(f"{p.name}'s hand before redeal:{p.hand}")

            to_stack_len = min(len(p.hand), 5)
            for _ in range((to_stack_len), 5):
                to_stack = p.hand.pop()
                p.stack.append(to_stack[0])

            print(f"{p.name}'s hand afterredeal:{p.hand}")

            prompt = (f"Input the \033[1m{to_stack_len}\033[0m digits of the cards you want to take from your stack:")

            try:
                idx = list(input(prompt))
                if idx != list():
                    raise ValueError
                if idx > to_stack_len:
                    print(f"Please enter, at most, {to_stack_len} numbers.")
                    raise ValueError
                for id in idx:
                    if id not in range(0, to_stack_len):
                        raise ValueError
            except ValueError:
                print("Please enter a list.")

            hand_redeal += 1
        
    # JOKER CARD
    # Joker allows to see the other player's hand 
    # Allows to exchange one of own cards with a chosen card from the other player's hand
    # Can be used whenever

##########################################
# Winner determination
##########################################
    def determine_winner(self):
        if not self.p1.hand and not self.p2.hand:
            print("Game-end-tie")
            return None, None # Return different something in order to make a 
                        # tie breaker to resultingly determine the actual winner
        if not self.p2.hand:
            return True, self.p1.name
        if not self.p1.hand:
            return True, self.p2.name
        else:
            return False, None

class Test_Game(Game):
    def __init__(self):
        self.test_game = True

        self.simulate = False
        
        self.deck = Test_Deck()

        self.hand1, self.stack1, self.hand2, self.stack2 = self.deck.test_deal()
        
        self.play_game("p1", self.stack1, "p2", self.stack2, self.hand1, self.hand2, True)

class Test_Deck():
    def __init__ (self):
        self.cards = []
        
        for j in range(1,5):
            for i in range(2,15):
                self.cards.append(Card(i, j))

    def test_deal(self):
        hand1 = []
        hand2 = []

        for _ in range(13,18):
            hand2.append(self.cards.pop(13))

        for _ in range(0,5):
            hand1.append(self.cards.pop(0))

        stack1 = []
        stack2 = []

        shuffle(self.cards)
        
        stack1 = self.cards[:21]
        stack2 = self.cards[21:]

        return hand1, stack1, hand2, stack2

##########################################
# Running the game:
##########################################
game = input("Test?")
if game == "t":
    game = Test_Game()
else:
    game = Game()

