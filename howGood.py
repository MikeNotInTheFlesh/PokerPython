import handStrength3 as hs


def how_strong(hand):
    achieved = hs.returning(hand)[0]
    achieved2 = hs.returning(hand)[1]
    hand_power = 0
    
    if achieved['flush'] > 0 and achieved['straight'] > 0:
        hand_power += 1000
        hand_power += achieved['straight']
    elif achieved['four_kind'] > 0:
        hand_power += 900
        hand_power += achieved['four_kind']
    elif achieved['full_house'] != 0:
        hand_power += 700
        hand_power += achieved['full_house'][0]+ 0.1 * achieved['full_house'][1]
    elif achieved['flush'] > 0:
        if achieved['flush'] > 13:
            hand_power += 699
        elif achieved['flush'] > 12:
            hand_power = +670
        elif achieved['flush'] > 10:
            hand_power = +640
            hand_power += achieved['flush']
        else: hand_power = 600
    elif achieved['straight'] > 0:
        if achieved['straight'] > 13:
            hand_power += 599
        elif achieved['straight'] > 12:
            hand_power += 570
            hand_power += achieved['straight']
        else:
            hand_power += 500
            hand_power += achieved['straight']
    elif achieved['three_kind'] > 0:
        hand_power += 400
        hand_power += achieved['three_kind']
    elif achieved['two_pair'] > 0:
        pairs = sorted(hs.returning(hand)[2], reverse=True)
        hand_power += 300
        hand_power += pairs[2] + .01 * pairs[0]
    elif achieved['pair'] > 0:
        hand_power += 100
        pairs = sorted(hs.returning(hand)[2])
        hand_power += achieved['pair']     
    else: hand_power += 0

    return hand_power

def preflop(hand):
    achieved = hs.returning(hand)[0]
    power = 0

    if hand[0][1] == hand[1][1]:
        power += 350
        print('Suited power up')
    if not achieved['pair'] > 0 and achieved['high_card'][0][0] - achieved['high_card'][0][1] == (1 or -1):
        power += 350
        print('Sequential power up')
    if achieved['pair'] > 13:
        power += 1000
    elif achieved['pair'] > 12:
        power += 900
    elif achieved['pair'] > 11:
        power += 800
    elif achieved['pair'] > 11:
        power += 700
    elif achieved['pair'] > 11:
        power += 600
    elif achieved['pair'] > 7:
        power += 400
    elif achieved['pair'] > 1:
        power += 300
    elif achieved['high_card'][0][0] + achieved['high_card'][0][1] > 26:
        power += 780
    elif achieved['high_card'][0][0] + achieved['high_card'][0][1] > 25:
        power += 580
    elif achieved['high_card'][0][0] + achieved['high_card'][0][1] > 20:
        power += 450
    elif achieved['high_card'][0][0] + achieved['high_card'][0][1] > 15:
        power += 80
    elif achieved['high_card'][0][0] + achieved['high_card'][0][1] > 10:
        power += 50
    else: power += 0
    return power
    

def strength_resolver_2pair(hand1, hand2):
#hand1 if for the player hand, hand2 for npc's
    for card in hand1:
        hand1 = [x[0] for x in hand1]
        hand2 = [x[0] for x in hand2]
        hand1, hand2 = sorted(hand1), sorted(hand2)
        for card in hand1:
            if hand1.count(card) > 1:
                hand1.remove(card)
                hand1.remove(card)
        hand1 = hand1[-1]
        for card in hand2:
            if hand2.count(card) > 1:
                hand2.remove(card)
                hand2.remove(card)
        hand2 = hand2[-1]
        if hand1 > hand2:
            return ('player')
        elif hand2 > hand1:
            return ('npc')
        elif hand1 == hand2:
            return ('split')
        else: print('Somthing went wrong in strength_resolve_2pair...')


def strength_resolver_3kind(hand1, hand2):
#hand1 if for the player hand, hand2 for npcs
    for card in hand1:
        hand1 = [x[0] for x in hand1]
        hand2 = [x[0] for x in hand2]
        hand1, hand2 = sorted(hand1, reverse = True), sorted(hand2, reverse = True)
        for card in hand1:
            if hand1.count(card) > 1:
                hand1.remove(card)
                hand1.remove(card)
                hand1.remove(card)
        for card in hand2:
            if hand2.count(card) > 1:
                hand2.remove(card)
                hand2.remove(card)
                hand2.remove(card)
        for y in range(2):
            if hand1[y] > hand2[y]:
                return ('player')
            elif hand1[y] < hand2[y]:
                return('npc')
        else: return ('split')


def strength_resolver_pair(hand1, hand2):
# hand1 if for the player hand, hand2 for npc's
    for card in hand1:
        hand1 = [x[0] for x in hand1]
        hand2 = [x[0] for x in hand2]
        hand1, hand2 = sorted(hand1, reverse = True), sorted(hand2, reverse = True)
        for card in hand1:
            if hand1.count(card) > 1:
                hand1.remove(card)
                hand1.remove(card)
        for card in hand2:
            if hand2.count(card) > 1:
                hand2.remove(card)
                hand2.remove(card)
        for y in range(3):
            if hand1[y] > hand2[y]:
                return ('player')
            elif hand1[y] < hand2[y]:
                return('npc')
        else: return ('split')

def resolve_high_card(hand1, hand2):
# hand1 if for the player hand, hand2 for npc's
    for card in hand1:
        hand1 = [x[0] for x in hand1]
        hand2 = [x[0] for x in hand2]
        hand1, hand2 = sorted(hand1, reverse = True), sorted(hand2, reverse = True)
        for y in range(5):
            if hand1[y] > hand2[y]:
                return ('player')
            elif hand1[y] < hand2[y]:
                return('npc')
        else: return ('split')


c = [(8, 'h'), (8, 's')]
a = [(2, 'd'), (3, 'd'), (2, 'd'), (13, 'c'), (11, 'd'), (2, 'h'), (8, 'd')]
b = [(2, 'd'), (7, 'd'), (6, 'd'), (2, 'c'), (8, 'd'), (2, 'h'), (11, 'd')]
#if __name__ == '__main__': print('BBv Preflop: ',preflop(c))
#if __name__ == '__main__': print('How Strong: ',how_strong(
#    [(4, 'd'), (5, 'd'), (6, 'd'), (2, 'c'), (7, 'd'), (4, 'h'), (8, 'd')]))
#if __name__ == '__main__': print('resolve pair: ',strength_resolver_pair(a, b))
#if __name__ == '__main__': print('resolve high_card: ',resolve_high_card(a, b))
if __name__ == '__main__': print('resolve 3kind: ',strength_resolver_3kind(a, b))
