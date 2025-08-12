##########################################
# CARD GAME: WAAAAAAAAR
##########################################
# Library imports
import random
from random import shuffle

##########################################
# Card class definition
##########################################
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
        shuffle(self.cards)

    def add_joker(self, add = True):
        
        yes_no_map = {
            'y': True,
            'n': False
                      }
        
        prompt1 = "Do you want to play with jokers included (Yes/No)?"
        prompt2 = "Do you wish to read the functionality of the Joker card in this game (Yes/No)?"

        prompts = [prompt1, prompt2]

        for i in prompts:
            try:
                prompt = str(input(i))
                prompt.lower()
                if prompt[0] != "y" or prompt[0] != 'n':
                    raise ValueError
                
            except ValueError:
                print("Please input only 'Yes' or 'Y', or 'No' or 'N'.")

            x = 0
            prompts[x] = prompt[yes_no_map]
            x += 1
        prompt = 

        if add:
            joker = Card(15, 5)
            self.cards.extend([joker, joker])
            print("Jokers were successfully added!")
        else:
            print("No Jokers wered added!")
            

    def deal(self):
        return self.cards[:26], self.cards[26:]
    
##########################################
# Player class definition
##########################################
class Player():
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hand = []
        self.refill_hand()
        
    def refill_hand(self):
        self.slots = 5 - len(self.hand)
        self.to_hand = min(self.slots, len(self.stack))
        for _ in range(self.to_hand):
            self.hand.append(self.stack.pop(0))
    
    # def collect_spoils(self, spoils):
    #     to_stack = len(spoils) - self.to_hand

    #     self.hand.extend(spoils[:self.to_hand])
    #     self.stack.extend(spoils[self.to_hand:])

    #     spoils.clear()

    #     self.spoils_refill_msg(self.to_hand, to_stack)
    
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

    # num_text_dict = {
    #     0: "Zero", 1: "One", 2: "Two", 3: "Three",
    #     4: "Four", 5: "Five:", 6: "Six", 7: "Seven",
    #     8: "Eight", 9: "Nine", 10: "Ten"
    #     }
    
    # def spoils_refill_msg(self, to_hand, to_stack):
    #     num_to_text = self.num_text_dict[len(to_stack)]
    #     if len(to_stack) == 1:
    #         card_text = "One card was"
    #     elif len(to_stack) in range(11) and not 0 and not 1:
    #         card_text = f"{num_to_text} cards were"
    #     print(f"The following cards were added to your hand: {to_hand}\n{card_text} added to the bottom of your stack!")

##########################################
# Game class definition
##########################################
class Game():
    def __init__(self):
        self.simulate = False

        name1 = input("\033[1;4mPlayer 1\033[0m\033[1m, enter your username:\033[0m")
        name2 = input("\033[1;4mPlayer 2\033[0m\033[1m, enter your username:\033[0m")
        
        self.deck = Deck()
        stack1, stack2 = self.deck.deal()
        
        print(f"\n\033[1mA large-scale war between {name1} and {name2} has begun!\033[0m")

        self.p1 = Player(name1, stack1)
        self.p2 = Player(name2, stack2)

##########################################
# GAME LOOP
##########################################
    def play_game(self):
        while self.p1.stack and self.p2.stack:
            # print(len(self.p1.stack), len(self.p2.stack))

            if not self.simulate:
                response = input("\n\033[3mPress\033[0m \033[1;3mq\033[0m \033[3mto quit,\033[0m \033[1;3ms\033[0m \033[3mto simulate, or press\033[0m \033[1;3many other key\033[0m \033[3mto play:\033[0m")
            if response == "s":
                self.simulate = True
            if response == "q":
                print("Quitters will amount to nothing in life! Bye bye :)")
                return
            
            print("--------------------\nA new battle commences, draw your weapons!\n")
            
            self.one_round()

##########################################
# Round definition
##########################################
    def one_round(self):
        p1n = self.p1.name
        p2n = self.p2.name

        # DEBUGGINGG GNGNAGEIEAOHFJAJSPDASDLA J
        print(f"{p1n}:", len(self.p1.hand), len(self.p1.stack))
        print(f"{p2n}:", len(self.p2.hand), len(self.p2.stack))

        p1c, p2c = self.card_choice(p1n, p2n)
        
        if p1c > p2c:
            self.p1.stack.extend([p1c, p2c])
            self.win_msg(p1n)
        elif p2c > p1c:
            self.p2.stack.extend([p1c, p2c])
            self.win_msg(p2n)
        elif p1c == p2c:
            self.war_resolve(p1n, p1c, p2n, p2c)

        self.p1.refill_hand()
        self.p2.refill_hand()

        win, winner = self.determine_winner()
        if win == None:
            print("A terrible mistake took place as no winner can be determined, rendering this war pointless... Sorry, not sorry :)")
            return
        elif win == False:
            return
        elif win == True:
            print(f"All battles have been fought, the war is over.\n\n\033[1;4m{winner.upper()}\033[0m WINS and takes ALL spoils home!\n====================")
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

    def tie_draw_msg(self, p1n, p1comp, p2n, p2comp):
        tie_draw_msg = f"\n\033[3m{p1n} drew {p1comp} as their war card, \n{p2n} drew {p2comp} as theirs.\033[0m\n"
        print(tie_draw_msg)
    
    def tie_win_msg(self, winner_name):
        print(f"\033[1m{winner_name}\033[0m has won the war and takes all the spoils back to their camp!\n====================\n--------------------\n")
    
    def tie_tie_msg(self, p1n, p2n, comp_card):
        comp_name = Card.values[comp_card]
        article = "an" if comp_name[0].lower() in ("a", "8") else "a"
        print(f"====================\nBoth {p1n} and {p2n} played {article} {comp_name}, so the war continues...")

##########################################
# War scenario methods
##########################################
    def war_resolve(self, p1n, p1c, p2n, p2c):
        print(f"Both players had a {p1c.value}, it's a tie...\n\033[1mWar has broken out!\033[0m\n----------------")
        spoils = [p1c, p2c]

        # DEBUGGINGG GNGNAGEIEAOHFJAJSPDASDLA J
        print(len(self.p1.hand), len(self.p1.stack))
        print(len(self.p2.hand), len(self.p2.stack))

        tie_repeat = True
        
        while tie_repeat:
            game_end, burn_flags = self.war_cards_check(self.p1.stack, self.p2.stack)

            if game_end:
                return
            
            burn_flag_p1 = burn_flags[self.p1]
            burn_flag_p2 = burn_flags[self.p2]

            burn_cards, war_cards = self.war_card_choice(burn_flag_p1, burn_flag_p2)
            
            spoils.extend(burn_cards)

            comp_card1, comp_card2 = war_cards
            
            self.tie_draw_msg(p1n, comp_card1, p2n, comp_card2)
            
            # DEBUGGINGG GNGNAGEIEAOHFJAJSPDASDLA J
            print("burn:", burn_cards, "war:", war_cards)
            print(f"{self.p1.name}'s stack: {len(self.p1.stack)}")
            print(f"{self.p2.name}'s stack: {len(self.p2.stack)}")
            print(f"{self.p1.name}'s hand: {len(self.p1.hand)}")
            print(f"{self.p2.name}'s hand: {len(self.p2.hand)}")
            
            #### JOKER LOGIC
            if self.joker in (comp_card1, comp_card2):
                pass

            if comp_card1 > comp_card2:
                self.p1.stack.extend(spoils + war_cards)
                print(spoils + war_cards)
                self.tie_win_msg(p1n) 
                tie_repeat = False
            elif comp_card2 > comp_card1:
                self.p2.stack.extend(spoils + war_cards)
                print(spoils + war_cards)
                self.tie_win_msg(p2n)
                tie_repeat = False
            elif comp_card1 == comp_card2:
                spoils.extend([comp_card1, comp_card2])
                self.tie_tie_msg(p1n, p2n, comp_card1.value)
                tie_repeat = True   

            # DEBUGGINGG GNGNAGEIEAOHFJAJSPDASDLA J
            print("burn:", burn_cards, "war:", war_cards)
            print(f"{self.p1.name}'s stack: {len(self.p1.stack)}")
            print(f"{self.p2.name}'s stack: {len(self.p2.stack)}")
            print(f"{self.p1.name}'s hand: {len(self.p1.hand)}")
            print(f"{self.p2.name}'s hand: {len(self.p2.hand)}")

        # STILL EDBUGIGENINGEINGEIN
        print("spoils:", spoils)      


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
                        except ValueError:
                            print("Please enter a number.")
                            continue
                        except IndexError:
                            print(f"Choose a number between 1 and {len(p.hand)}.")
                            continue
                        break

                    elif self.simulate:
                        idx = random.choice(range(1, len(p.hand) + 1))
                        break

                    burn_card = p.hand.pop(idx - 1)
                    burn_cards.append(burn_card)

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
    
    def war_cards_check(self, stack_p1, stack_p2):
        players = [(self.p1, len(stack_p1)), (self.p2, len(stack_p2))]

        burn_flags = {}
        game_end = False

        for p, count in players:
            if count >= 2:
                burn_flags[p] = True

            elif count == 1:
                print(f"\033[1m{p.name}\033[0m is on their last card. They will play this round without a burner card. Better make it count!")
                burn_flags[p] = False
            elif count == 0:
                print(f"\033[1m{p.name}\033[0m has run out of cards to use in the war...\n--------------------")
                burn_flags[p] = True
                game_end = True
            else:
                raise ValueError(f"Invalid card count ({count}) for player \033[1m{p.name}\033[0m. Expected >= 0.")

        return game_end, burn_flags

##########################################
# Special mechanics
##########################################
    def hand_redeal(self):
    # Allow the player to exchange all 5 cards in their hand for 5 cards in their stack (or 3 if only 3 cards left in stack, etc.)
    # Allow only 3 times per entire game per player
    # Automatically makes the player lose the round in which they apply this mechanic by taking 1 card randomly from the new hand,
    # and losing that card to the other player regardless of strength of the card.
    
        for p in (self.p1, self.p2):
            p.hand_red = 0
            if p.hand_red < 3:
            # code
                hand_redeal += 1
            elif p.hand_red == 3:
                print("You've run out of redeals, stay on top of your game...")
        pass
    
    # JOKER CARD
    # Joker allows to see the other player's hand 
    # Allows to exchange one of own cards with a chosen card from the other player's hand
    # Can be used whenever

##########################################
# Winner determination
##########################################
    def determine_winner(self):
        if not self.p1.stack and not self.p2.stack:
            print("Game-end-tie")
            return None, None # Return different something in order to make a 
                        # tie breaker to resultingly determine the actual winner
        if not self.p2.stack:
            return True, self.p1.name
        if not self.p1.stack:
            return True, self.p2.name
        else:
            return False, None

##########################################
# Running the game:
##########################################
game = Game()
game.play_game()

