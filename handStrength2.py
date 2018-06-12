from collections import Counter

# Straight might need some work
#Needs a full_house function

achieved_strength = {'straight_flush':0, 'four_kind':0, 'full_house':0,
                     'flush':0, 'straight':0, 'three_kind':0,
                     'two_pair':0, 'pair':0,'high_card':0}
achieved_strength2 = []
high_hand = []


def flush(hand):
    global achieved_strength, achieved_strength2
    how_many = Counter(suit[1] for suit in hand)
#    print(how_many)
    for suit in ['c', 'h', 'd', 's']:
        
        if how_many[suit] > 4:
            suited_hand = hand[:]
            for card in suited_hand:
                if card[1] != suit:
                    hand.remove(card)
            achieved_strength['flush'] = 1
            achieved_strength2.append('flush')
            high_hand.append(hand)
    else: straight(hand)
            
'''
    elif how_many['h'] > 4:
        suited_hand = hand[:]
        for card in suited_hand:
            if card[1] != 'h':
                hand.remove(card)
        achieved_strength['flush'] = 1
        achieved_strength2.append('flush')
        high_hand.append(hand)
        straight(hand)

    elif how_many['d'] > 4:
        suited_hand = hand[:]
        for card in suited_hand:
            if card[1] != 'd':
                hand.remove(card)
        achieved_strength['flush'] = 1
        achieved_strength2.append('flush')
        high_hand.append(hand)

    elif how_many['s'] > 4:
        suited_hand = hand[:]
        for card in suited_hand:
            if card[1] != 's':
                hand.remove(card)
        achieved_strength['flush'] = 1
        achieved_strength2.append('flush')
        high_hand.append(hand)'''
    



def straight(hand):
    shand = {x[0] for x in hand} 
    shand = list(shand)
    shand = sorted(shand)
 #   print('straight nums: ', shand)

    while len(shand) >= 5:
 #       print('shand in while: ', shand)
        if shand[-1] == shand[-2] + 1 == shand[-3] + 2 == shand[-4] +3 == shand[-5] +4:
            achieved_strength['straight'] = shand[-1]
            achieved_strength2.append('straight')
            high_hand.append(shand[:-6:-1])
            shand = []
        else: shand.pop()
    else:
        if len(high_hand) == 0:
            three_kind(hand)
 #       else: print('What happened???')


def four_kind(hand):
    nhand = [x[0] for x in hand]
    for card in nhand:
        if nhand.count(card) > 3:
            achieved_strength['four_kind'] = card
            achieved_strength2.append('four_kind')
            high_hand.append(card)
    if len(high_hand) == 0: full_house(hand)
            


def three_kind(hand):
    nhand = [x[0] for x in hand]
#    print ('three kind checking: ', nhand)
    for card in nhand:
        if nhand.count(card) > 2:
            nhand_mod = list(filter((card).__ne__, nhand))#get rid of the trips
            if type(pair_check(nhand_mod)) == int: #pair_check isn't needed anymore
                achieved_strength['full_house'] = [card, pair_check(nhand_mod)]
                achieved_strength2.append('full_house')
                high_hand.append(card)
                high_hand.append(card)
                high_hand.append(card)
                break
            else:
                achieved_strength['three_kind'] = card
                achieved_strength2.append('three_kind')
                high_hand.append(card)
                high_hand.append(card)
                high_hand.append(card)
                break
    else: pair(hand)
    

def full_house(hand):
    nhand = [x[0] for x in hand]
#    print ('full_house: ', nhand)
    for card in nhand:
        if nhand.count(card) > 2:
            nhand_mod = list(filter((card).__ne__, nhand))#get rid of the trips
            if type(pair_check(nhand_mod)) == int:
                achieved_strength['full_house'] = [card, pair_check(nhand_mod)]
                achieved_strength2.append('full_house')
                high_hand.append(card)
                high_hand.append(card)
                high_hand.append(card)
                break
    if len(high_hand) < 5:
        flush(hand)

    
def pair_check(hand):
    for card in hand:
        if hand.count(card) > 1:
            high_hand.append(card)
            return card


def pair(hand):
    pair_count = 0
    nhand = [x[0] for x in hand]
    for card in nhand:
        if nhand.count(card) > 1:
            achieved_strength['pair'] = card
            achieved_strength2.append('pair')
            high_hand.append(card)
            pair_count += 1
    if pair_count == 4:
        achieved_strength['two_pair'] = 1
        achieved_strength2.append('two_pair')
    elif pair_count == 2:
        pass
    else: high_card(hand)
    print('Pair count: ', pair_count)

def high_card(hand):
    nhand = [x[0] for x in hand]
    nhand = sorted(nhand, reverse=True)
    nhand = nhand[0:5]
    achieved_strength['high_card'] = [nhand]
    achieved_strength2.append('high_card')
    for card in nhand:
        high_hand.append(card)
    return False

def returning(test):
    four_kind(test)
    print ('achieved_strength: ', achieved_strength)
    print ('achieved_strength2: ', achieved_strength2)
    print ('High hand: ', high_hand)
    return achieved_strength2, high_hand
        

test = [(7, 'd'), (12, 'd'), (9, 's'), (5, 'd'), (5, 'd'), (12, 'd'), (8, 's')]
'''
if __name__ == '__main__': flush(test), straight(test), four_kind(test),
three_kind(test), pair(test), high_card(test)
'''
if __name__ == '__main__': print(returning(test))


'''    
print('achieved_strength: ', achieved_strength)
print('achieved_strength2: ', achieved_strength2)
print('High hand: ', high_hand)
'''


'''    if len(shand) > 5 and shand[1] == shand[2] - 1 == shand[3] - 2 == shand[4] -3 == shand[5] -4:
        achieved_strength['straight'] = shand[5]
        achieved_strength2.append('straight')
        high_hand.append(shand[1:6])
        return True
    elif len(shand) > 6 and shand[1] == shand[2] - 1 == shand[3] - 2 == shand[4] -3 == shand[5] -4:
        achieved_strength['straight'] = shand[5]
        achieved_strength2.append('straight')
        high_hand.append(shand[1:6])
        return True
    elif shand[0] == shand[1] - 1 == shand[2] - 2 == shand[3] -3 == shand[4] -4:
        achieved_strength['straight'] = shand[4]
        achieved_strength2.append('straight')
        high_hand.append(shand[0:5])
        return True'''


        
