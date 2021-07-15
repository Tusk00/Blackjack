import random, os, sys, re

class Card:
    def __init__(self, suit, rank):
        self.__rank = rank
        self.__suit = suit

    @property
    def suit(self): #Suit getter
        return self.__suit

    @suit.setter
    def suit(self, suit): #Suit setter
        if suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            self.__suit = suit
        else:
            print("INVALID SUIT")

    @property
    def rank(self): #Rank getter
        return self.__rank
    
    @rank.setter
    def rank(self, rank):#Rank setter
        if rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]:
            self.__rank = rank
        else:
            print("INVALID RANK")

    def __str__(self):
        output = self.rank + " Of " + self.suit + "\n"
        return output
#############
# myCard = Card("Jack", "Diamond")
# myCard.suit = "Porsche"
# myCard.rank = "90"
# print(myCard)
##########################################################
class Deck(Card):
    def __init__(self):
        self.__card = []
        self.createDeck()
    
    def createDeck(self): #Fills the card list with 52 cards
        suit = ["Hearts", "Diamonds", "Spades", "Clubs"]
        rank = [str(r) for r in range(2,11)] + ["Jack", "Queen", "King", "Ace"]
        self.__card = [Card(s, r) for s in suit for r in rank]

    def Shuffle(self): 
        random.shuffle(self.__card)

    def deal(self):
        return self.__card.pop()

    def returnCard(self, card): #Checks if the same card is already in deck
        if card in self.__card:
            print("THIS CARD IS ALREADY IN THE DECK.")
        self.__card.append(card)

    def count(self): #Counts # of cards in deck
        count = 0
        for i in self.__card:
            count += 1
        return count
#############
# TEST CODE
# d = Deck()
# print(str(d.count()))
# d.createDeck()
# print(str(d.count()))
##########################################################
class Game(Deck):
    deck = Deck()
    deck.Shuffle()
    playerHand = []
    dealerHand = []
    __won = 0
    __lost = 0

    def deal(self):
        hand1 = []
        hand2 = []
        for i in range(2):
            self.deck.Shuffle()
            hand1.append(self.deck.deal())
            hand2.append(self.deck.deal())
            hands = [hand1, hand2]
            return hands

    def hit(self):
        return self.deck.deal()

    def total(self, hand): #Makes face cards worth 10 and Ace worth 11 or 1 and adds them to the total
        count = 0
        for card in hand:
            if card.rank == "Jack" or card.rank == "Queen" or card.rank == "King":
                count += 10
            elif card.rank == "Ace":
                if count >= 11:
                    count += 1
                else:
                    count += 11
            else:
                count += int(card.rank)
        return count
        
    def printScore(self, dealerHand, playerHand):
        dealerStr = ""
        playerStr = ""
            
        print("Dealer Total: " + str(self.total(self.dealerHand)))
        print("---")
        print("Player Total: " + str(self.total(self.playerHand)) + "\n")

    def playAgain(self):
        again = input("Would you like to play again? (y/n): ").lower()
        if again == "y":
            for i in self.dealerHand:
                self.deck.returnCard(i)
            for j in self.playerHand:
                self.deck.returnCard(j)
            playerHand = []
            dealerHand = []
            if self.deck.count() != 52:
                print("ERROR. DECK DOES NOT HAVE 52 CARDS")
                exit()
            self.game()
        else:
            print("Come back soon!")
            exit()

    def winner(self, dealerHand, playerHand): #Determines the winner of the game
        if self.total(playerHand) == 21:
            self.printScore(dealerHand, playerHand)
            print("YOU WIN!")
            self.__won += 1
            self.playAgain()
        elif self.total(dealerHand) == 21:
            self.printScore(dealerHand, playerHand)
            print("YOU LOSE!")
            self.__lost += 1
            self.playAgain()

    def score(self, totalDealer, totalPlayer): #Determines who wins the game
        if totalPlayer <= 21:
            if totalDealer <= 21:
                if totalDealer < totalPlayer:
                    self.__won += 1
                    self.printScore(self.dealerHand, self.playerHand)
                    print("You win!")
                    self.playAgain()
                elif totalDealer > totalPlayer:
                    self.__lost += 1
                    self.printScore(self.dealerHand, self.playerHand)
                    print("Good luck next time. You lose!")
                    self.playAgain()
                else:
                    self.printScore(self.dealerHand, self.playerHand)
                    print("Its a draw.")
                    self.playAgain()
            else:
                self.__won += 1
                self.printScore(self.dealerHand, self.playerHand)
                print("The dealer busted. You win!")
                self.playAgain()
        else:
            self.__lost += 1
            self.printScore(self.dealerHand, self.playerHand)
            print("You Busted. You lose!")
            self.playAgain()

    def game(self): #Blackjack mechanics
        choice = 0

        print("---------------------------------------------")
        print("\t\t BLACKJACK")
        print("---------------------------------------------")
        print("Games won: %s\t Games lost: %s" %(self.__won, self.__lost))

        blackjack = Game()
        hands = blackjack.deal()
        self.playerHand = hands.pop()   #Deals two cards to each player
        self.dealerHand = hands.pop()
        print("\nDealers card is: " + self.dealerHand[0].__str__())

        handStr = ""
        for i in self.playerHand:
            handStr += i.__str__()
            handStr += " "
        print("Your card is: " + handStr)
        print("Total of: " + str(self.total(self.playerHand))) #Gets the total of your first card
        self.winner(self.dealerHand, self.playerHand)

        while choice != "q":
            choice = input("Would you like to Hit(H), Stay(S), or Quit(Q): ").lower()
            print("--------\n")
            if choice == "q":
                print("Come back soon!")
                exit()
            elif choice == "h":
                card = self.hit()
                self.playerHand.append(card)

                totalPlayer = self.total(self.playerHand)
                print(card.__str__())
                print("The new total is: " + str(totalPlayer) + "\n\n--------")
                if totalPlayer > 21:
                    self.score(self.total(self.dealerHand), totalPlayer)
            elif choice == "s":
                while self.total(self.dealerHand) < 17:
                    self.dealerHand.append(self.hit())
                self.score(self.total(self.dealerHand), self.total(self.playerHand))
            else:
                print("Try again, that wasn't an option")

if __name__ == "__main__":
    game = Game()
    game.game()