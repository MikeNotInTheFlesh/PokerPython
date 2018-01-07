import random as rd
import howGood
import handStrength3 as hs
import sys
import time

delay = 0.5 # variable for slowing game 
available_cards = []
npc_hand = []
player_hand = []
board = []
hand_names = {'straight_flush':'a Straight Flush', 'four_kind':'Four of a Kind',
                          'full_house':'a Full House', 'flush':'a Flush', 'straight':'a Straight',
                          'three_kind': 'Three of a Kind', 'two_pair': 'Two Pair',
                          'pair': 'a Pair','high_card':'High Card'}

def full_deck():
        global available_cards
        available_cards = [(x, y) for x in range(2, 15)
                                                   for y in ['c', 'd', 'h', 's']]       
        

def get_card():
                return available_cards.pop(rd.randrange(len(available_cards)))


def hole_cards():
        npc_hand.append(get_card())
        npc_hand.append(get_card())
        player_hand.append(get_card())
        player_hand.append(get_card())

def flop_cards():
        board.append(get_card())
        board.append(get_card())
        board.append(get_card())

def deal_one():
        board.append(get_card())


player_money = 1000
npc_money = 1000
button = rd.choice(('You have', 'Computer has'))
bb, sb = 10, 5 # blinds
pot = 0

def money_stuff(who = None, how_much = 0, winner = None):
        global pot, player_money, npc_money
        pot += how_much
        if who == 'player' and winner == None:
                player_money -= how_much
        elif who == 'npc' and winner == None:
                npc_money -= how_much
        elif winner == 'player':
                print('Paying you a pot of', pot)
                player_money += pot
                pot = 0
        elif winner == 'npc':
                print('Paying Computer a pot of', pot)
                npc_money += pot
                pot = 0
        elif winner == 'split':
                print('Splitting pot. Each player gets', pot/2)
                player_money += pot / 2
                npc_money += pot / 2
                pot = 0
        else: print('Did something go wrong in "money_stuff"? who, how_much, winner: ',
                                who, how_much, winner)


def someone_folds(who_folded):
        if who_folded == 'npc':
                print('The computer folded. You win', pot, '.')
                money_stuff(winner = 'player')
                time.sleep(delay)
                print('Your new balance is', player_money)
        else:
                print('You folded. The computer won', pot)
                money_stuff(winner = 'npc')
                print('Your new balance is', player_money)
                print('Computer has', npc_money)
        print ('Play again? (y or n)')
        again = input('> ').lower()
        print()
        if len(again) == 0:
                print('\n###########################################################\n')
                print('Final values: Player Money: {}.\t Computer Money: {}\n'.format(player_money, npc_money))
                print("Goodbye")
                sys.exit()
        elif again[0] == 'y':
                print('\n###########################################################\n')
                start_game()
        else:
                print('\n###########################################################\n')
                print('Final values: Player Money: {}.\t Computer Money: {}\n'.format(player_money, npc_money))
                print("Goodbye")
                sys.exit()


def does_npc_bet(street, rays = 0, vs_check = False):
 #       hs.returning(npc_hand)
        time.sleep(delay)
        if street == 'pre':
                power = howGood.preflop(npc_hand)
                print('Power: ', power)
                if power > 349 + 100 * rays:
                        rays += 1
                        money_stuff('npc', 2 * bb)
                        print('Computer raises' , bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif vs_check == True:
                        print("Computer checks")
                        flop()
                elif power > 60:
                        money_stuff('npc', bb)
                        print('Computer calls' , bb, 'Pot is now ', pot, '\n')
                        flop()
                else: someone_folds('npc')
        elif street == 'flop':
  #              print('nnnnnnnnnn' , npc_hand + board)
                power = howGood.how_strong(npc_hand + board)
                if power > 299 and vs_check == True:
                        money_stuff('npc', bb)
                        rays += 1
                        print('Computer bets' , bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif power > 299:
                        money_stuff('npc', 2 * bb)
                        print('Computer raises' , bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif vs_check == True:
                        print('Computer checks')
                        turn()
                elif power < 100: someone_folds('npc')
                else:
                        money_stuff('npc', bb)
                        print('Computer calls' , bb, 'Pot is now ', pot, '\n')
                        turn()
        elif street == 'turn':
#                print('mjjjjj' , npc_hand + board)
                power = howGood.how_strong(npc_hand + board)
                if power > 330 and vs_check == True:
                        money_stuff('npc', bb)
                        rays += 1
                        print('Computer bets' , 2 * bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif power > 399:
                        money_stuff('npc', 4 * bb)
                        print('Computer raises' ,2 * bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif vs_check == True:
                        print('Computer checks behind')
                        river()
                elif power < 100: someone_folds('npc')
                else:
                        money_stuff('npc', bb)
                        print('Computer calls' , bb, 'Pot is now ', pot, '\n')
                        river()
        elif street == 'river':
 #               print('riversssss' , npc_hand + board)
                power = howGood.how_strong(npc_hand + board)
                if power > 380 and vs_check == True:
                        money_stuff('npc', bb)
                        rays += 1
                        print('Computer bets' , 2 * bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif power > 499:
                        money_stuff('npc', 4 * bb)
                        print('Computer raises' ,2 * bb, 'Pot is now ', pot, '\n')
                        player_vs_raise(street, rays)
                elif vs_check == True:
                        print('Computer checks behind')
                        showdown()
                elif power < 299: someone_folds('npc')
                else:
                        money_stuff('npc', 2 * bb)
                        print('Computer calls' , 2 * bb, 'Pot is now ', pot, '\n')
                        showdown()


def player_vs_raise(street, rays = 0):
        time.sleep(delay)
        print("\nThe pot is now: ", pot, 'With {} to call.\n'.format(bb))
        time.sleep(delay)
        print("Do you raise, call, or fold? ('r', 'c', or 'f')")
        p_move = (input('> ')).lower()
        print()
        if p_move[0] == 'f': someone_folds('player')
        elif p_move[0] == 'c':
                if street == 'pre':
                        money_stuff('player', bb)
                        print('Player calls {}. Pot is now {}.'.format(bb, pot), '\n')
                        flop()
                elif street == 'flop':
                        money_stuff('player', bb)
                        print('Player calls {}. Pot is now {}.'.format(bb, pot), '\n')
                        turn()
                elif street == 'turn':
                        money_stuff('player', 4 * bb)
                        print('Player calls {}. Pot is now {}.'.format(bb, pot), '\n')
                        river()
                else:
                        money_stuff('player', 4 * bb)
                        print('Player calls {}. Pot is now {}.'.format(bb, pot), '\n')
                        showdown()
        elif p_move[0] == 'r':
                if street == 'pre':
                        money_stuff('player', 2 * bb)
                        print('Player raises {}. Pot is now {}.'.format(bb, pot), '\n')
                        does_npc_bet('pre', rays)
                elif street == 'flop':
                        money_stuff('player', 2 * bb)
                        print('Player raises {}. Pot is now {}.'.format(bb, pot), '\n')
                        does_npc_bet('flop', rays)
                elif street == 'turn':
                        money_stuff('player', 4 * bb)
                        print('Player raises {}. Pot is now {}.'.format(2*bb, pot), '\n')
                        does_npc_bet('turn', rays)
                else:
                        money_stuff('player', 4 * bb)
                        print('Player raises {}. Pot is now {}.'.format(2*bb, pot), '\n')
                        does_npc_bet('river', rays)
        else:
                print("That's not a valid move.")
                player_vs_raise(street, rays)

def player_vs_check(street):
        time.sleep(delay)
        print('Computer checks. Do you want to (check or bet)?')
        action = (input('>      ')).lower()
        if len(action) == 0: player_vs_check(street)
        if action[0] == 'c':
                if street == 'flop':
                        print('You Check. On to the turn.\n')
                        turn()
                elif street == 'turn':
                        print('You Check. Lets see the river.\n')
                        river()
                elif street == 'river':
                        print('You Check. Showdown!!!\n')
                        showdown()
                else: print('Something went wrong in player_vs_check/check')
        elif action[0] == 'b':
                if street == 'flop':
                        print('You bet', bb,'Pot is now', pot,'\n')
                        does_npc_bet('flop', 1)
                elif street == 'turn':
                        print('You bet', 2*bb,'Pot is now', pot,'\n')
                        does_npc_bet('turn', 1)
                elif street == 'river':
                        print('You bet', 2*bb,'Pot is now', pot,'\n')
                        does_npc_bet('river', 1)
                else: print('Something went wrong in player_vs_check/bet')
        else:
                print('Lets give you another chance to type it in right...')
                player_vs_check(street)
                
                        

def preflop_vs_call(street = 'pre'): # is the arg necessary?
        time.sleep(delay)
        print('Your turn. Raise or Check? (r, c)')
        this = (input('> ')).lower()
        if len(this) == 0: preflop_vs_call()
        print()
        if this[0] == 'c':
                flop()
        elif this[0] == 'r':
                money_stuff('player', bb)
                print('Player raises {}. Pot is now {}.'.format(bb, pot), '\n')
                does_npc_bet('pre', rays = 1)
        else:
                print('What\'s that again?')
                preflop_vs_call()


def first_to_act(who, street):
        time.sleep(delay)
        if who == 'npc' and street == 'pre':
  #              hs.returning(npc_hand)
                power = howGood.preflop(npc_hand)
                if power > 349:
                        rays = 0
                        rays += 1
                        money_stuff('npc', sb + bb)
                        print('Computer raises' , bb, 'Pot is now ', pot, '\n')
                        player_vs_raise('pre', rays)
                elif power < 40:
                        someone_folds('npc')
                else:
                        money_stuff('npc', sb)
                        print('Computer calls', sb, '. Pot is now', pot, '\n')
                        preflop_vs_call('pre')
        elif who == 'npc' and street == 'flop':
 #               hs.returning(npc_hand)
                power2 = howGood.how_strong(npc_hand + board)
                if power2 > 108:
                        money_stuff('npc', bb)
                        print('Computer bets', bb, 'Pot is now', pot, '\n')
                        player_vs_raise('flop', rays = 1)
                else:
                        print('Computer checks\n')
                        player_vs_check('flop')
        elif who == 'npc' and street == 'turn':
                power = howGood.how_strong(npc_hand + board)
                if power > 199:
                        money_stuff('npc', 2 * bb)
                        print('Computer bets' ,2 * bb, 'Pot is now', pot, '\n')
                        player_vs_raise('turn', rays = 1)
                else:
                        print('Computer checks\n')
                        player_vs_check('turn')
        elif who == 'npc' and street == 'river':
                power = howGood.how_strong(npc_hand + board)
                if power > 299:
                        money_stuff('npc', 2 * bb)
                        print('Computer bets' ,2 * bb, 'Pot is now', pot, '\n')
                        player_vs_raise('river', rays = 1)
                else:
                        print('Computer checks\n')
                        player_vs_check('river')
        elif who == 'player' and street == 'pre':
                print("Do you raise or call, or fold? ('r', 'c', 'f')")
                p_move = (input('> ')).lower()
                if len(p_move) == 0: first_to_act('player', 'pre')
                print()
                if p_move[0] == 'c':
                        money_stuff('player', sb)
                        print('You call. Pot is now {}.\n'.format(pot))
                        does_npc_bet('pre', rays = 0, vs_check = True)
                elif p_move == 'r':
                        money_stuff('player', sb + bb)
                        print('Player raises {}. Pot is now {}.\n'.format(bb, pot))
                        does_npc_bet('pre', rays = .8)
                elif p_move == 'f':
                        someone_folds('player')
                else:
                        print('You typed the wrong thing in.')
                        first_to_act('player', 'pre')
        elif who == 'player' and street == 'flop':
                print('Your turn. Bet or Check? (b, c)')
                t_bet = (input('> ')).lower()
                if len(t_bet) == 0: first_to_act('player', 'flop')
                print()
                if t_bet[0] == 'c':
                        print('You check.\n')
                        does_npc_bet('flop', rays = 0, vs_check = True)
                elif t_bet[0] == 'b':
                        money_stuff('player', bb)
                        print('Player bets {}. Pot is now {}.\n'.format(bb, pot))
                        does_npc_bet('flop', rays = 1)
                else:
                        print('You typed the wrong thing in.\n')
                        first_to_act('player', 'flop')
        elif who == 'player' and street == 'turn':
                print('Your turn. Bet or Check? (b, c)')
                t_bet = (input('> ')).lower()
                if len(t_bet) == 0: first_to_act('player', 'turn')
                print()
                if t_bet[0] == 'c':
                        print('You check.\n')
                        does_npc_bet('turn', rays = 0, vs_check = True)
                elif t_bet[0] == 'b':
                        money_stuff('player', 2 * bb)
                        print('Player bets {}. Pot is now {}.\n'.format(2 * bb, pot))
                        does_npc_bet('turn', rays = 1)
                else:
                        print('You typed the wrong thing in.\n')
                        first_to_act('player', 'turn')
        elif who == 'player' and street == 'river':
                print('Your turn. Bet or Check? (b, c)')
                t_bet = (input('> ')).lower()
                if len(t_bet) == 0: first_to_act('player', 'river')
                print()
                if t_bet[0] == 'c':
                        print('You check.\n')
                        does_npc_bet('river', rays = 0, vs_check = True)
                elif t_bet[0] == 'b':
                        money_stuff('player', 2 * bb)
                        print('Player bets {}. Pot is now {}.\n'.format(2 * bb, pot))
                        does_npc_bet('river', rays = 1)
                else:
                        print('You typed the wrong thing in.\n')
                        first_to_act('player', 'river')
        else: print('Something went wrong in \'First to Act\'.')
        

def flop():
        time.sleep(delay)
        deal_one()
        deal_one()
        deal_one()
# For testing custom flops
# board.append((2, 'h'))
# board.append((2, 'd'))
# board.append((2, 'c'))
#        flop_cards()
        print('###########################################################')
        print('\nHere comes the flop...\n')
        print('The flop is: ', board)
        print('Your cards are: ', player_hand[0], player_hand[1])
        print('Computer has: ', npc_hand[0], npc_hand[1])
        print('')
        if button == 'You have':
                first_to_act('npc', 'flop')
        else: first_to_act('player', 'flop')

def turn():
        print('###########################################################')
        time.sleep(delay)
        deal_one()
        print('\nHere comes the turn...\n')
        print('The turn card is', board[-1])
        print('The turn makes the board: ', board)
        print('Your cards are: ', player_hand[0], player_hand[1])
        print('Computer has: ', npc_hand[0], npc_hand[1])
        print()
        if button == 'You have':
                first_to_act('npc', 'turn')
        else: first_to_act('player', 'turn')

def river():
        print('###########################################################')
        time.sleep(delay)
        deal_one()
        print('\nHere comes the river...\n')
        print('The river card is', board[-1])
        print('The board is: ', board)
        print('Your cards are: ', player_hand[0], player_hand[1])
        print('Computer has: ', npc_hand[0], npc_hand[1])
        print()
        if button == 'You have':
                first_to_act('npc', 'river')
        else: first_to_act('player', 'river')

##def showdown(): #did this yesterday
##        time.sleep(delay)
##        cpu = howGood.how_strong(npc_hand + board)
##        print(cpu)
##        play = howGood.how_strong(player_hand + board)
##        print(play)
##        if cpu > play:
##                print('Computer wins')
##                money_stuff(winner = 'npc')
##        elif play > cpu:
##                money_stuff(winner ='player')
##                print('Player wins')
##        elif cpu == play:
##                print('Split pot')
##                money_stuff(winner = 'split')
##        else: print("I'm confuzzled...")
##        again = input('Play again? (y or n)\n').lower()
##        if again[0] == 'y':
##                print('\n\n')
##                start_game()
##        else:
##                print('Final values: Player Money: {}.\t Computer Money: {}'.format(player_money, npc_money))
##                print("Goodbye")
##                sys.exit()

def showdown():
        print('Lets see who won...\n')
        time.sleep(delay)
        player = hs.returning(player_hand + board)
        print('You have {} with {}.\n'.format(hand_names[player[1][-1]], player[2]))
 #       print('You Test ', player)
        npc = hs.returning(npc_hand + board)
        print('Computer has {} with {}.\n'.format(hand_names[npc[1][-1]], npc[2]))
#        print('Computer TEST ', npc)
        p_power = howGood.how_strong(player_hand + board)
        print('player_power: ', p_power)
 #       print('player_hand + board ', player_hand + board)
        print('npc hole cards: ', npc_hand)
        npc_power = howGood.how_strong(npc_hand + board)
        print('npc_power: ', npc_power)
        if p_power > npc_power:
                money_stuff(winner = 'player')
                print('You win!')
        elif p_power < npc_power:
                money_stuff(winner = 'npc')
                print('Computer wins')
        elif p_power == npc_power:
                if player[1][0] == 'three_kind':
 #                       print('Trying to resolve three_kind')
                        who = howGood.strength_resolver_3kind(player_hand + board, npc_hand + board)
                elif player[1][-1] == 'two_pair':
 #                       print('Trying to resolve two pair')
                        who = howGood.strength_resolver_2pair(player_hand + board, npc_hand + board)
                elif player[1][0] == 'pair':
 #                       print('Trying to resolve pair')
                        who = howGood.strength_resolver_pair(player_hand + board, npc_hand + board)
                elif player[1][0] == 'high_card':
                        who = howGood.resolve_high_card(player_hand + board, npc_hand + board)
#                        print('Trying to resolve HC')
                else:
                        print('Split pot')
                        who = 'split'
                print('Who won???', who)
                money_stuff(winner = who)
        else:
                print('Whaaat???', howGood.how_strong(player_hand + board) , howGood.how_strong(npc_hand + board))
        print('Your new balance is', player_money)
        print('Computer has', npc_money)
        
        print('Play again? (y or n)')
        again = input('> ').lower()
        
        if len(again) == 0:
                print('\n###########################################################\n')
                print('Final values: Player Money: {}.\t Computer Money: {}\n'.format(player_money, npc_money))
                print("Goodbye")
                sys.exit()
        elif again[0] != 'y':
                print('\n###########################################################\n')
                print('Final values: Player Money: {}.\t Computer Money: {}\n'.format(player_money, npc_money))
                print("Goodbye")
                sys.exit()   
        else:
                print('###########################################################')
                print('\n')
                start_game()


def start_game():
        global player_money, npc_money, button, available_cards, npc_hand, player_hand, board
        available_cards = []
        npc_hand = []
        player_hand = []
        board = []
        if button == 'You have':
                button = 'Computer has'
        else: button = 'You have'
        print('Welcome to Holdem Poker.\n')
        time.sleep(delay/2)
        print('You have {} dollars.'.format(player_money))
        time.sleep(delay/2)
        print('The computer has {} dollars.\n'.format(npc_money))
        time.sleep(delay/2)
        print(button, 'the button.\n')
        print('Blinds in. Shuffle and deal.\n')
        time.sleep(delay/2)
        if button == 'You have':
                money_stuff('player', sb)
                money_stuff('npc', bb)
        else:
                money_stuff('npc', sb)
                money_stuff('player', bb)
        full_deck()
        hole_cards()
        print('Your cards are: ', player_hand[0], player_hand[1])
        print('Computer has: ', npc_hand[0], npc_hand[1], '\t\t ### debugging ###')
        print('')
        if button == 'Computer has':
                first_to_act('npc', 'pre')
        else:
                first_to_act('player', 'pre')
        
                  


if __name__ =='__main__': start_game()



#print('npc hand: ', npc_hand)
#print('player hand: ', player_hand)
#print('board: ', board)






'''
elif who == 'player' and street == 'flop':
                p_move = (input("Do you bet or check? ('bet', 'check')\n")).lower()
                print(p_move)
                if p_move[0] == 'c':
                        print('You check. Pot is still {}.\n'.format(pot))
                        does_npc_bet('flop')
                elif p_move == 'b':
                        money_stuff('player', sb + bb)
                        print('Player bets {}. Pot is now {}.\n'.format(bb, pot))
                        does_npc_bet('pre', .8)
                else:
                        print('You typed the wrong thing in.\n')
                        first_to_act('player', 'flop')
'''
