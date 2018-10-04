import pycard
import time

def MainGame(deck,dealer,*players,**kwargs):
    dealer_stand_17=0
    if kwargs.get('standsoft17',None) is not None:
        dealer_stand_17=1
    if kwargs.get('hitsoft17',None) is not None:
        dealer_stand_17=0



    while True:
        dealer.discard(all=True)
        for hands in players:
            hands.discard(all=True)
        deck.clear()
        deck.addpack()
        deck.shuffle()
        dealer.deal(2,deck)
        Totals=[]
        for hands in players:
            hands.deal(2,deck)
        print('Dealer\'s cards: {} ##'.format(dealer.__str__(cards=dealer.cards)[0]))
        for n,hands in enumerate(players):
            print('Player {}\'s hand: {} {}'.format(n+1,hands.__str__(cards=hands.cards)[0],hands.__str__(cards=hands.cards)[1]))
        #Enter action phase
        for n,hands in enumerate(players):
            time.sleep(1)
            stringprint = '{} {}'.format(hands.__str__(cards=hands.cards)[0],hands.__str__(cards=hands.cards)[1])
            print('\n\nPlayer {}\'s turn:'.format(n+1))
            print('Hand: {}    Total: {}'.format(stringprint,hands.evaluate_BJ()[0]))
            usr_inp=input('Action (stand/hit): ')
            while usr_inp!='stand':
                hands.deal(1,deck)
                stringprint+=' {}'.format(hands.__str__(cards=hands.cards)[-1])
                print('Hand: {}    Total: {}'.format(stringprint,hands.evaluate_BJ()[0]))
                if hands.evaluate_BJ()[0]>21:
                    time.sleep(1)
                    print('Bust! Your total is: {}'.format(hands.evaluate_BJ()[0]))
                    break
                usr_inp=input('Action (stand/hit)')

            else:
                print('Total: {}\n\n'.format(hands.evaluate_BJ()[0]))
            Totals.append(hands.evaluate_BJ()[0])
        print('Dealer\'s hand: {} {}    Total: {}'.format(dealer.__str__(cards=dealer.cards)[0],dealer.__str__(cards=dealer.cards)[1],dealer.evaluate_BJ()[0]))
        if dealer_stand_17==0:
            stringprint = '{} {}'.format(dealer.__str__(cards=dealer.cards)[0],dealer.__str__(cards=dealer.cards)[1])
            while dealer.evaluate_BJ()[0]<17 or (dealer.evaluate_BJ()[0]==17 and 11 in dealer.evaluate_BJ()[1]):
                time.sleep(2)
                dealer.deal(1,deck)
                stringprint+= ' {}'.format(dealer.__str__(cards=dealer.cards)[-1])
                print('Dealer\'s hand: {}    Total: {}'.format(stringprint,dealer.evaluate_BJ()[0]))
            Totals.append(dealer.evaluate_BJ()[0])
        if dealer_stand_17==1:
            while dealer.evaluate_BJ()[0]<17:
                time.sleep(2)
                dealer.deal(1,deck)
                stringprint+= ' {}'.format(dealer.__str__(cards=dealer.cards)[-1])
                print('Dealer\'s hand: {}    Total: {}'.format(stringprint,dealer.evaluate_BJ()[0]))

        print('\n')
        time.sleep(1)
        for n,i in enumerate(Totals[:-1]):
            if (i>Totals[-1] and i<22) or (Totals[-1]>21 and i<22):
                print('Player {} wins!'.format(n+1))
            elif i==Totals[-1] and i<22:
                print('Player {} draws!'.format(n+1))
            else:
                print('Player {} loses!'.format(n+1))
        input('\n\nPlay again press enter')






deck1=pycard.deck()
hand1=pycard.hand()
hand2=pycard.hand()
dealer1=pycard.hand()
MainGame(deck1,dealer1,hand1,hand2)
