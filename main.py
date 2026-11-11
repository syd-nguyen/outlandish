import random
import numpy as np

class Card:

    '''
    leanings is a list
    [pathos, ethos, logos, motm]
    dice is a list
    [[dice to roll], threshold, success multiplier, fail multiplier]
    
    '''
    def __init__(self, name: str, leanings: list[int], moveName: str, dice: list, damage: int):
        self.name = name
        self.leanings = leanings
        self.moveName = moveName
        self.dice = dice
        self.damage = damage

    def generateLeaning(self):
        optList = (['p'] * self.leanings[0]) + (['e'] * self.leanings[1]) + (['l'] * self.leanings[2]) + (['m'] * self.leanings[3]) 
        return random.choice(optList)  

    def getDmg(self):
        # roll dice to calculate base damage
        if self.dice is None:
            return self.damage
        else:
            rolls = [random.randrange(1, 1+die) for die in self.dice[0]]
            totalRoll = np.sum(rolls)
            if totalRoll >= self.dice[1]:
                return self.damage * self.dice[2]
            else:
                return self.damage * self.dice[3]



class PlayerOrOpponent():
    def __init__(self, name: str, leanings: list[int], sk: int, pt: int, handSize: int, deck: list[Card]):
        self.name = name
        self.leanings = leanings
        self.sk = sk
        self.pt = pt
        self.handSize = handSize
        self.hand = []
        self.draw = deck
        self.discard = []

    def generateLeaning(self):
            optList = (['p'] * self.leanings[0]) + (['e'] * self.leanings[1]) + (['l'] * self.leanings[2]) + (['m'] * self.leanings[3]) 
            return random.choice(optList)  

    def shuffle(self, pile):
        self.pile = random.shuffle(pile)

    def drawCards(self):
        if len(self.draw) == 0:
            random.shuffle(self.discard)
            self.draw = list.copy(self.discard)
            self.discard = []
        while len(self.hand) < self.handSize:
            self.hand.append(self.draw.pop(0)) 

    def playCard(self):
        self.shuffle(self.hand)
        toPlay = self.hand.pop(0)
        self.discard.append(toPlay)
        return toPlay

def playCards(plrCard, oppCard, opp):

    # calculate leaningMultiplier
    plrLeaning = plrCard.generateLeaning()
    oppLeaning = opp.generateLeaning()
    leaningMultiplier = 0.0
    if (plrLeaning == oppLeaning):
        leaningMultiplier = 1.5
    else:
        leaningMultiplier = 0.5

    # get base damages
    plrDmg = plrCard.getDmg()
    oppDmg = oppCard.getDmg()

    change = ( plrDmg - oppDmg ) * leaningMultiplier
    opp.sk -= change

    print('player plays', plrCard.name, 'for', plrDmg)
    print('opponent plays', oppCard.name, 'for', oppDmg)
    print('leanings are', plrLeaning, 'and', oppLeaning, 'for', leaningMultiplier, 'multiplier')
    print('skepticism changes by', change, 'and is now', opp.sk)
    print('---------------------------------------------')
    
    return

def simulateRound(plr: PlayerOrOpponent, opp: PlayerOrOpponent):

    print('ℹ️  plr draw is ' + str([card.name for card in plr.draw]))
    print('ℹ️  plr hand is ' + str([card.name for card in plr.hand]))
    print('ℹ️  plr discard is ' + str([card.name for card in plr.discard]))
    print('ℹ️  opp draw is ' + str([card.name for card in opp.draw]))
    print('ℹ️  opp hand is ' + str([card.name for card in opp.hand]))
    print('ℹ️  opp discard is ' + str([card.name for card in opp.discard]))

    # player draws up to hand size
    plr.drawCards()

    # opponent draws up to hand size
    opp.drawCards()

    # player and opponent play random cards
    plrCard = plr.playCard()
    oppCard = opp.playCard()    
    playCards(plrCard, oppCard, opp)


def simulateDispute(plr: PlayerOrOpponent, opp: PlayerOrOpponent):

    # shuffle draw piles
    random.shuffle(plr.draw)
    random.shuffle(opp.draw)

    # simulate a bunch of rounds
    turnsTaken = 0
    patienceRanOut = True
    for _ in range(opp.pt):
        simulateRound(plr, opp)
        turnsTaken += 1
        if markus.sk <= 0:
            break
    if markus.sk <= 0:
        patienceRanOut = False

    if patienceRanOut:
        print('🟥 patience ran out in', turnsTaken, 'turns')
    else:
        print('🟢 dispute won in', turnsTaken, 'turns')

'''
MAIN STUFF THAT RUNS
'''
# tbd: make this not gross to look at

CARDS = {
    'hug': Card('hug', [1,0,0,0], 'friendship & love', None, 5),
    'hug2': Card('hug2', [1,0,0,0], 'friendship & love', None, 5),
    'hug3': Card('hug3', [1,0,0,0], 'friendship & love', None, 5),
    'strokeOfDoubt': Card('stroke of doubt', [0,0,0,1], 'pang of questioning', None, 2),
    'strokeOfDoubt2': Card('stroke of doubt2', [0,0,0,1], 'pang of questioning', None, 2),
    'strokeOfDoubt3': Card('stroke of doubt3', [0,0,0,1], 'pang of questioning', None, 2)
}

markus = PlayerOrOpponent('markus', [75, 15, 9, 1], 10, 3, 1, [CARDS['strokeOfDoubt'], CARDS['strokeOfDoubt2'], CARDS['strokeOfDoubt3']])
player = PlayerOrOpponent('player', None, None, None, 1, [CARDS['hug'], CARDS['hug2'], CARDS['hug3']])

simulateDispute(player, markus)