import random
from itertools import chain
from itertools import combinations

class deck:

    def __init__(self,**kwargs):
        '''
        deck() has 2 kwargs:
        cards: this is a list of any numbers up to 52, 1-13 are Ace to King of Clubs, 14-26 are Diamonds, 27-39 are Hearts, 40-52 are Spades
        multi: this is an int which creates a pack of cards with multiple packs of 52, i.e multi=3 will produce a list from 1-52 three times, non-nested.
        '''
        self.card1 = random.randint(1,53)
        self.pack = list(range(1,53))
        if kwargs.setdefault('multi',None) is not None:
            temp=[]
            for i in range(kwargs['multi']):
                temp.append(list(range(1,53)))
            temp = list(chain(*temp))
            self.pack = temp
        if kwargs.setdefault('cards',None) is not None:
            self.pack = kwargs['cards']

    def __str__(self):
        packprint=[]
        pack = self.pack
        for i in pack:
            if i>52:
                raise ValueError('Int greater than 52 found, unable to process')
        temppack=pack[:]
        for j in range(len(temppack)):
            if int(temppack[j])%13==11:
                temppack[j]='J'
            elif int(temppack[j])%13==12:
                temppack[j]='Q'
            elif int(temppack[j])%13==0:
                temppack[j]='K'
            elif int(temppack[j])%13==1:
                temppack[j]='A'
            else:
                temppack[j]=temppack[j]%13

        for i in range(len(pack)):
            if pack[i]<14:
                packprint.append(str(temppack[i])+'C')
            elif pack[i]<27:
                packprint.append(str(temppack[i])+'D')
            elif pack[i]<40:
                packprint.append(str(temppack[i])+'H')
            else:
                packprint.append(str(temppack[i])+'S')
        return str(packprint)

    def __add__(self,other):
        tot = self.pack + other.pack
        return deck(cards=tot)

    def shuffle(self,**kwargs):
        if kwargs.setdefault('cards',None) is not None:
            return random.shuffle(cards)
        return random.shuffle(self.pack)

    def riffle_shuffle(self,**kwargs):
        for n in range(kwargs.setdefault('times',1)):
            half = int(len(self.pack)/2)
            temp=[]
            for i in range(half):

                temp.append(self.pack.pop(0))
                temp.append(self.pack.pop(int(len(self.pack)/2)))
            self.pack = temp
            if len(self.pack)%2:
                g=self.pack.pop(0)
                self.pack.append(g)
        return self.pack

    def __len__(self):
        return len(self.pack)

    def deal(self,cards=1):
        temp=[]
        for i in range(cards):
            temp.append(self.pack.pop(0))
        return temp

    def add(self,cards,**kwargs):
        if type(cards)==int:
            cards=[cards]
        if kwargs.setdefault('top',None) is not None:
            for i in reversed(cards):
                self.pack.insert(0,i)
        else:
            for i in cards:
                self.pack.append(i)
        return self.pack

    def clear(self):
        for i in range(len(self.pack)):
            self.pack.pop(0)
        return self.pack

    def addpack(self,times=1):
        for n in range(times):
            for i in range(1,53):
                self.pack.append(i)
        return self.pack

class hand:

    def __init__(self,**kwargs):
        self.cards=[]
        if kwargs.setdefault('cards',None) is not None:
            self.cards=kwargs['cards']

    def __str__(self,cards=None):
        if cards!=None:
            pack=cards
        else:
            pack = self.cards
        packprint=[]
        # pack = self.cards
        for i in pack:
            if i>52:
                raise ValueError('Int greater than 52 found, unable to process')
        temppack=pack[:]
        for j in range(len(temppack)):
            if int(temppack[j])%13==11:
                temppack[j]='J'
            elif int(temppack[j])%13==12:
                temppack[j]='Q'
            elif int(temppack[j])%13==0:
                temppack[j]='K'
            elif int(temppack[j])%13==1:
                temppack[j]='A'
            else:
                temppack[j]=temppack[j]%13

        for i in range(len(pack)):
            if pack[i]<14:
                packprint.append(str(temppack[i])+'C')
            elif pack[i]<27:
                packprint.append(str(temppack[i])+'D')
            elif pack[i]<40:
                packprint.append(str(temppack[i])+'H')
            else:
                packprint.append(str(temppack[i])+'S')

        if cards!=None:
            return packprint
        return str(packprint)

    def __add__(self,other):
        tot = self.cards + other.cards
        return hand(cards=tot)

    def __len__(self):
        return len(self.cards)

    def add(self,card_add):
        if type(card_add)==int:
            card_add=[card_add]
        for i in card_add:
            self.cards.append(i)
        return self.cards

    def deal(self, card_num, deck):
        for i in range(card_num):
            self.cards.append(deck.deal()[0])
        return self.cards

    def shuffle(self,**kwargs):
        if kwargs.setdefault('cards',None) is not None:
            return random.shuffle(cards)
        return random.shuffle(self.pack)

    def pophand(self,number):
        return self.cards.pop(number-1)

    def evaluate(self,list=None):
        dict = {}
        if list!=None:
            cardset=list
        else:
            cardset=self.cards
        for j in cardset:
            if j<14:
                dict.setdefault('C',[])
                dict['C'].append(j)
                dict['C']=sorted(dict['C'])
            elif j<27:
                dict.setdefault('D',[])
                dict['D'].append(j-13)
                dict['D']=sorted(dict['D'])
            elif j<40:
                dict.setdefault('H',[])
                dict['H'].append(j-26)
                dict['H']=sorted(dict['H'])
            elif j<53:
                dict.setdefault('S',[])
                dict['S'].append(j-39)
                dict['S']=sorted(dict['S'])
        return dict

    def evaluate_BJ(self):
        summer=[]
        for j in self.cards:
            if j%13 >1 and j%13<11:
                summer.append(j%13)
            elif j%13==1:
                summer.append(11)
            elif j%13==0 or j%13==11 or j%13==12:
                summer.append(10)
        while sum(summer)>21:
            if 11 in summer:
                summer[summer.index(11)]=1
            else:
                break
        return sum(summer),summer

    def evaluate_TH(self,*args):
        score = 0
        highest_hand=[]
        ecards=[]
        for i in args:
            if type(i)==list:
                ecards=i
            else:
                ecards=i.cards
        community=self.cards
        if len(ecards)!=2:
            raise ValueError('Hand must have exactly 2 cards in to evaluate using Texas Holdem rules')
        comm_combs = combinations(community,3)
        for i in comm_combs:
            fullhouse,fourkind,threekind,twokind,twopair=0,0,0,0,0
            numbs=[]
            all_cards = list(i)+ecards
            eval = self.evaluate(all_cards)
            for i in eval:
                for j in eval[i]:
                    numbs.append(j)
            first = sorted(numbs)[0]
            for i in range(len(numbs)):
                if numbs[i]==1:
                    numbs[i]=14
            for i in numbs:
                if numbs.count(i)==4:
                    fourkind=i
                if numbs.count(i)==3:
                    for j in numbs:
                        if numbs.count(j)==2 and j!=i:
                            fullhouse=i+j
                    threekind=i
                if numbs.count(i)==2:
                    for j in numbs:
                        if numbs.count(j)==2 and j!=i:
                            twopair=i+j
                    twokind=i
            if len(eval.keys())==1 and sorted(numbs)==[10,11,12,13,14]:
                return 1e10+20, eval

            elif len(eval.keys())==1 and (list(range(first,first+5))==sorted(numbs) or sorted(numbs)==[2,3,4,5,14]):
                if 1e9+max(numbs)>score:
                    score=1e9+max(numbs)
                    highest_hand=eval

            elif fourkind>0:
                if 1e8+fourkind>score:
                    score=1e8+fourkind
                    highest_hand=eval
            elif fullhouse>0:
                if 1e7+fullhouse>score:
                    score=1e7+fullhouse
                    highest_hand=eval
            elif len(eval.keys())==1:
                if 1e6+sum(numbs)>score:
                    score=1e6+sum(numbs)
                    highest_hand=eval
            elif list(range(first,first+5))==sorted(numbs) or sorted(numbs)==[2,3,4,5,14]:
                if 1e5+max(numbs)>score:
                    score=1e5+max(numbs)
                    highest_hand=eval
            elif threekind>0:
                if 1e4+sum(numbs)>score:
                    score=1e4+sum(numbs)
                    highest_hand=eval
            elif twopair>0:
                if 1e3+sum(numbs)>score:
                    score = 1e3+sum(numbs)
                    highest_hand=eval
            elif twokind>0:
                if 1e2+sum(numbs)>score:
                    score=1e2+sum(numbs)
                    highest_hand=eval
            else:
                if sum(numbs)>score:
                    score=sum(numbs)
                    highest_hand=eval
        return score,highest_hand

    def evaluate_multi_TH(self,*args):
        '''
        Used for comparing hands in texas holdem for a winner. All of the cards should be passed as args, using the community to call the function

        '''
        scores=[]
        for i in args:
            if type(i)==list:
                if len(i)!=2:
                    raise ValueError('Must have exactly 2 cards in each hand')
                scores.append(self.evaluate_TH(i)[0])
            else:
                if len(i.cards)!=2:
                    raise ValueError('Must have exactly 2 cards in each hand')
                scores.append(self.evaluate_TH(i)[0])

        if type(args[0])==list:
            return scores.index(max(scores))+1, self.__str__(args[scores.index(max(scores))]),scores
        return scores.index(max(scores))+1, self.__str__(args[scores.index(max(scores))].cards),scores








if __name__ == '__main__':

