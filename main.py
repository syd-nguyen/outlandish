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

class Opponent():
    def __init__(self, name: str, leanings: list[int], sk: int, pt: int):
        self.name = name
        self.leanings = leanings
        self.sk = sk
        self.pt = pt

    def generateLeaning(self):
            optList = (['p'] * self.leanings[0]) + (['e'] * self.leanings[1]) + (['l'] * self.leanings[2]) + (['m'] * self.leanings[3]) 
            return random.choice(optList)  

    def changeSk(self, change):
        self.sk -= change


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
    opp.changeSk(change)

    print('player plays', plrCard.name, 'for', plrDmg)
    print('opponent plays', oppCard.name, 'for', oppDmg)
    print('leanings are', plrLeaning, 'and', oppLeaning, 'for', leaningMultiplier, 'multiplier')
    print('skepticism changes by', change, 'and is now', opp.sk)
    print('---------------------------------------------')
    
    return

def simulate(opp: Opponent, plrDeck: list[Card], oppDeck: list[Card]):
    # tba: drawing and discarding and shuffling
    playCards(plrDeck[0], oppDeck[0], opp)


'''
MAIN STUFF THAT RUNS
'''
# tbd: make this not gross to look at

CARDS = {
    'hug': Card('hug', [1,0,0,0], 'friendship & love', None, 5),
    'strokeOfDoubt': Card('stroke of doubt', [0,0,0,1], 'pang of questioning', None, 2)
}

markus = Opponent('markus', [75, 15, 9, 1], 10, 3)
currentOpp = markus

print()
turnsTaken = 0
patienceRanOut = True
for _ in range(currentOpp.pt):
    simulate(markus, [CARDS['hug']], [CARDS['strokeOfDoubt']])
    turnsTaken += 1
    if markus.sk <= 0:
        break
if markus.sk <= 0:
    patienceRanOut = False


if patienceRanOut:
    print('🟥 patience ran out in', turnsTaken, 'turns')
else:
    print('🟢 dispute won in', turnsTaken, 'turns')

print()
