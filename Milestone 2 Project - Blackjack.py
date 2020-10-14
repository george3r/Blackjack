import random
from IPython.display import clear_output

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

game_on = True
playing = True

class Card:
    
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit # + " with a value of " + str(self.value)


class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(rank,suit)           
                self.deck.append(created_card)
    
    def __str__(self):
        return str(len(self.deck))

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.total_value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,new_card):
        self.cards.append(new_card)
        self.total_value += new_card.value
        if new_card.rank == "Ace":
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.total_value > 21 and self.aces > 0:
            self.total_value -=  10
            self.aces -= 1
            
    def __str__(self):
        return str(len(self.cards))   


class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


def take_bet():
    
    user_input = "wrong"
    
    while type(user_input) != int:
        user_input = input('How many chips would you like to bet? ')
        try:
            bet = int(user_input)
        except ValueError:
            user_input
            
        if int(user_input) > players_chips.total:
            print(f'You only have {players_chips.total} chips left to bet! ')
            user_input
    
        elif int(user_input) < players_chips.total + 1:
            players_chips.bet = int(user_input)
            break


def hit_or_stand(deck,hand):
    
    global playing  # to control an upcoming while loop
    playing = True
    
    hit = "wrong"
    
    while hit not in ["H","S"]:
        hit = input('Would you like to Hit "(H)" or Stand "(S)"?  ').upper()
        
        if hit == "H":
            players_hand.add_card(deck.deal())
            players_hand.adjust_for_ace()
            
        elif hit =="S":
            playing = False
        
    hit = "wrong"


# Display cards
def show_some(player,dealer):
    clear_output()
    print(f'\nYou are betting {players_chips.bet} out of {players_chips.total} chips. \n')
    
    print("Dealer's Hand: ") 
    print("*hidden card*")
    print(dealers_hand.cards[0])
        
    print("\nYour Hand: total value: " + str(players_hand.total_value))    
    print(*players_hand.cards, sep='\n')
    
def show_all(player,dealer):
    clear_output()
    print(f'You are betting {players_chips.bet} out of {players_chips.total} chips. \n')
    
    print("Dealer's Hand: total value: " + str(dealers_hand.total_value))
    print(*dealers_hand.cards, sep='\n')
        
    print("\nYour Hand: total value: " + str(players_hand.total_value))    
    print(*players_hand.cards, sep='\n')


# End of Game Scenarios
def player_busts():
    players_chips.lose_bet()
    players_chips.bet = 0
    print("\nYou LOST the hand!")
    print("_"*100 + "\n")
    playing = False

def player_wins():
    players_chips.win_bet()
    players_chips.bet = 0
    print("\nYou WON the hand!")
    print("_"*100 + "\n")
    playing = False
    
def dealer_busts():
    players_chips.win_bet()
    players_chips.bet = 0
    print("\nYou WON the hand!")
    print("_"*100 + "\n")
    
def dealer_wins():
    players_chips.lose_bet()
    players_chips.bet = 0
    print("\nYou LOST the hand!")
    print("_"*100 + "\n")  
    
def push():
    players_chips.bet = 0
    print("\nThe had was TIED!")
    print("_"*100 + "\n")





# Game Play
game_on = True
players_chips = Chips()
    
# opening statement
print("Welcome to Blackjack! \n")
print("You start with 100 chips!")

while game_on == True:
   
    # Create & shuffle the deck, deal two cards to each player

    deck = Deck()
    deck.shuffle()
    
    dealers_hand = Hand()
    dealers_hand.add_card(deck.deal())
    dealers_hand.add_card(deck.deal())
    
    players_hand = Hand()
    players_hand.add_card(deck.deal())
    players_hand.add_card(deck.deal())
        
    
    # Prompt the Player for their bet
    take_bet()
    
    # Show cards (but keep one dealer card hidden)
    show_some(players_hand,dealers_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,players_hand)
        
        
        # Show cards (but keep one dealer card hidden)
        show_some(players_hand,dealers_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if players_hand.total_value > 21:
            player_busts()
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    
    while players_hand.total_value <= 21 and dealers_hand.total_value < 17:
        dealers_hand.add_card(deck.deal())
        dealers_hand.adjust_for_ace()
        if dealers_hand.total_value > 21:
            dealer_busts()
            break
         
    
        # Show all cards
        
    show_all(dealers_hand,players_hand)
    
        # Run different winning scenarios
    
    if players_hand.total_value <= 21 and players_hand.total_value > dealers_hand.total_value:
        player_wins()
    elif dealers_hand.total_value <= 21 and dealers_hand.total_value > players_hand.total_value:
        dealer_wins()
    elif players_hand.total_value == dealers_hand.total_value:
        push()
    elif players_hand.total_value > 21:
        player_busts()
    elif dealers_hand.total_value > 21:
        dealer_busts()
    
    
    # Inform Player of their chips total 
    
    print(f'\nYou have {players_chips.total} chips left! ')
    if players_chips.total <= 0:
        print("You have run out of chips! \nThanks for playing!")
        game_on = False
        break
        
    # Ask to play again
    
    play_again = "wrong"
    while play_again not in ["Y","N"]:
        play_again = input('Would you like to play again "(Y/N)"? ').upper()
        
        if play_again == "Y":
            playing = True
        elif play_again == "N":
            game_on = False
            playing = False
    
