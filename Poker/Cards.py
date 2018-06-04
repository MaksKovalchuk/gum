import random


class Cards(object):

    name = ""              # имя карты
    strenght = 2           # сила карты
    suit = ""              # масть карты
    numberInHand = 0       # номер карты в руке
    configurations = ["Покер", "Роял флэш", "Стрит флэш", "Каре", "Фулл хаус", "Флэш",\
                      "Стрит", "Трипл", "Две пары", "Одна пара"]

    # обновить колоду
    @staticmethod
    def RefreshDeck(cards):
        while len(cards) > 0:
            cards.pop()

        diamonds = []    # бубновая масть
        spades = []      # пиковая масть
        clubs = []       # трефовая масть
        hearts = []      # червонная масть

        joker = Cards()  # джокер
        joker.strenght = 15
        joker.name = "Joker"
        joker.suit = "?"

        cardStrenght = 2

        for i in range(13):
            diamonds.append(Cards())
            diamonds[i].suit = "<>"
            if i < 9:
                diamonds[i].strenght = cardStrenght
                diamonds[i].name = cardStrenght
                cardStrenght += 1
            elif i == 9:
                diamonds[i].strenght = 11
                diamonds[i].name = "J"
            elif i == 10:
                diamonds[i].strenght = 12
                diamonds[i].name = "Q"
            elif i == 11:
                diamonds[i].strenght = 13
                diamonds[i].name = "K"
            else:
                diamonds[i].strenght = 14
                diamonds[i].name = "A"
                cardStrenght = 2
                break

        for i in range(13):
            spades.append(Cards())
            spades[i].suit = "<^>"
            if i < 9:
                spades[i].strenght = cardStrenght
                spades[i].name = cardStrenght
                cardStrenght += 1
            elif i == 9:
                spades[i].strenght = 11
                spades[i].name = "J"
            elif i == 10:
                spades[i].strenght = 12
                spades[i].name = "Q"
            elif i == 11:
                spades[i].strenght = 13
                spades[i].name = "K"
            else:
                spades[i].strenght = 14
                spades[i].name = "A"
                cardStrenght = 2
                break

        for i in range(13):
            clubs.append(Cards())
            clubs[i].suit = "x"
            if i < 9:
                clubs[i].strenght = cardStrenght
                clubs[i].name = cardStrenght
                cardStrenght += 1
            elif i == 9:
                clubs[i].strenght = 11
                clubs[i].name = "J"
            elif i == 10:
                clubs[i].strenght = 12
                clubs[i].name = "Q"
            elif i == 11:
                clubs[i].strenght = 13
                clubs[i].name = "K"
            else:
                clubs[i].strenght = 14
                clubs[i].name = "A"
                cardStrenght = 2
                break

        for i in range(13):
            hearts.append(Cards())
            hearts[i].suit = "<3"
            if i < 9:
                hearts[i].strenght = cardStrenght
                hearts[i].name = cardStrenght
                cardStrenght += 1
            elif i == 9:
                hearts[i].strenght = 11
                hearts[i].name = "J"
            elif i == 10:
                hearts[i].strenght = 12
                hearts[i].name = "Q"
            elif i == 11:
                hearts[i].strenght = 13
                hearts[i].name = "K"
            else:
                hearts[i].strenght = 14
                hearts[i].name = "A"
                break

        cards.extend(diamonds)
        cards.extend(spades)
        cards.extend(clubs)
        cards.extend(hearts)
        # cards.append(joker)

    # проверка на наличие джокера
    @staticmethod
    def CheckForJoker(hand):
        contains = False

        for card in hand:
            if card.name == "Joker":
                contains = True
                break
            else:
                pass

        return contains

    # попытка составления комбинации с джокером
    @staticmethod
    def UseJoker(hand):
        return

    # перетасовать колоду
    @staticmethod
    def ShuffleDeck(cards):
        random.shuffle(cards)

    # раздать карты
    @staticmethod
    def GetHand(cards, hand):
        for i in range(5):
            hand.append(cards.pop(0))
            hand[i].numberInHand = i + 1

    # убрать карту
    @staticmethod
    def DeleteCards(hand, cardToSwap):
        for card in hand:
            if card.numberInHand == cardToSwap:
                deletedCard = card
                hand.remove(card)
                return str(deletedCard.name) + str(deletedCard.suit)
            else:
                pass

    # сортировка карт в руке по убыванию силы
    @staticmethod
    def SortHand(hand):
        for i in range(len(hand)):
            for j in range(len(hand)):
                if hand[j].strenght < hand[i].strenght:
                    hand[j], hand[i] = hand[i], hand[j]

    # пересчет номера в руке
    @staticmethod
    def RecalculateNumbers(hand):
        Cards.SortHand(hand)
        num = 1

        for card in hand:
            card.numberInHand = num
            num += 1

    # вывод руки в консоль:
    @staticmethod
    def PrintHand(hand):
        for card in hand:
            print(str.format("{}|{}{}", card.numberInHand, card.name, card.suit))

    # дополнить руку
    @staticmethod
    def ExpandHand(deck, hand):
        for i in range(5 - len(hand)):
            hand.append(deck.pop(0))
        Cards.SortHand(hand)
        Cards.RecalculateNumbers(hand)

    # смена карт
    @staticmethod
    def SwapCards(swapList, hand):
        amountToSwap = int(swapList[1])
        swapList.pop(0)
        swapList.pop(0)
        returnList = []
        for i in range(amountToSwap):
            for card in hand:
                if card.numberInHand == int(swapList[0]):
                    returnList.append(str(card.name) + str(card.suit))
                    swapList.pop(0)
                    hand.remove(card)
                    break
                else:
                    pass

        return returnList

    # проверка на одинаковость масти
    @staticmethod
    def SameFlush(hand):
        Cards.SortHand(hand)

        sameSuit = True
        for i in range(len(hand) - 1):
            if hand[i].suit == hand[i + 1].suit:
                pass
            else:
                sameSuit = False
                break

        return sameSuit

    # проверка на комбинации
    @staticmethod
    def HandConfiguration(hand):

        if Cards.FiveOfAkind(hand):
            return [10, "Покер"]
        elif Cards.RoyalFlush(hand):
            return [9, "Роял-флэш"]
        elif Cards.StraightFlush(hand):
            return [8, "Стрит-флэш"]
        elif Cards.Quads(hand):
            return [7, "Каре"]
        elif Cards.FullHouse(hand):
            return [6, "Фулл хаус"]
        elif Cards.Flash(hand):
            return [5, "Флэш"]
        elif Cards.Straight(hand):
            return [4, "Стрит"]
        elif Cards.ThreeOfAkind(hand):
            return [3, "Трипл"]
        elif Cards.TwoPairs(hand):
            return [2, "Две пары"]
        elif Cards.OnePair(hand):
            return [1, "Одна пара"]
        else:
            return [0, "Старшая карта"]

    # нахождение победителя
    @staticmethod
    def chooseWinner(strongHandWins, handOne, handTwo):
        firstHand = Cards.HandConfiguration(handOne)
        secondHand = Cards.HandConfiguration(handTwo)

        if int(firstHand[0]) > int(secondHand[0]) and strongHandWins:
            return 0
        elif int(firstHand[0]) > int(secondHand[0]) and not strongHandWins:
            return 1
        elif int(firstHand[0]) < int(secondHand[0]) and strongHandWins:
            return 1
        elif int(firstHand[0]) < int(secondHand[0]) and not strongHandWins:
            return 0

    # вывод руки и её кофигурации
    @staticmethod
    def printHandConfig(hand):
        for card in hand:
            print(str.format("{}|{}{}", card.numberInHand, card.name, card.suit))
        conf = Cards.HandConfiguration(hand)
        print("Результат " + str(conf[1]))

    # проверка на покер(4 туза + джокер)
    @staticmethod
    def FiveOfAkind(hand):
        if hand[0].strenght == 15 and hand[1].strenght == 14 and\
           hand[2].strenght == 14 and hand[3].strenght == 14 and hand[4].strenght == 14:
            return True
        else:
            return False

    # проверка на роял-флэш
    @staticmethod
    def RoyalFlush(hand):
        Cards.SortHand(hand)

        if Cards.StraightFlush(hand) and hand[0].name == "A":
            return True
        else:
            return False

    # проверка на стрит-флэш (5 карт одной масти по порядку)
    @staticmethod
    def StraightFlush(hand):
        Cards.SortHand(hand)
        if hand[0].strenght - hand[1].strenght == 1 and hand[1].strenght - hand[2].strenght == 1 and \
         hand[2].strenght - hand[3].strenght == 1 and hand[3].strenght - hand[4].strenght == 1 and Cards.SameFlush(hand):
            return True
        else:
            return False

    # проверка на каре(четвёрка) (4 карты одного достоинства)
    @staticmethod
    def Quads(hand):
        Cards.SortHand(hand)

        if hand[0].name == hand[1].name and hand[1].name == hand[2].name and \
           hand[2].name == hand[3].name:
            return True
        elif hand[4].name == hand[3].name and hand[1].name == hand[2].name and \
           hand[2].name == hand[3].name:
            return True
        else:
            return False

    # проверка на фулл хаус (тройка и пара)
    @staticmethod
    def FullHouse(hand):
        Cards.SortHand(hand)

        if hand[0].strenght == hand[1].strenght and hand[1].strenght == hand[2].strenght and \
            hand[2].strenght != hand[3].strenght and hand[3].strenght == hand[4].strenght:
            return True

        elif hand[0].strenght == hand[1].strenght and hand[1].strenght != hand[2].strenght and \
            hand[2].strenght == hand[3].strenght and hand[3].strenght == hand[4].strenght:
            return True

        else:
            return False

    # проверка на флэш (пять карт одной масти)
    @staticmethod
    def Flash(hand):
        Cards.SortHand(hand)
        if hand[0].suit == hand[1].suit and hand[1].suit == hand[2].suit and hand[2].suit == hand[3].suit\
                   and hand[3].suit == hand[4].suit:
            return True
        else:
            return False

    # проверка на стрит (пять карт по порядку любых мастей)
    @staticmethod
    def Straight(hand):
        Cards.SortHand(hand)
        if hand[0].strenght == 14 and hand[1].strenght == 5 and hand[2].strenght == 4 \
           and hand[3] == 3 and hand[4] == 2:
            hand[0].strenght = 1
            Cards.SortHand(hand)
            return True
        elif hand[0].strenght - hand[1].strenght == 1 and hand[1].strenght - hand[2].strenght == 1 and \
             hand[2].strenght - hand[3].strenght == 1 and hand[3].strenght - hand[4].strenght == 1 :
            return True
        else:
            return False

    # проверка на трипл (три карты одной силы)
    @staticmethod
    def ThreeOfAkind(hand):
        Cards.SortHand(hand)

        if(hand[0].strenght == hand[1].strenght and hand[1].strenght \
                == hand[2].strenght):
            return True
        else:
            return False

    # проверка на две пары (две пары карт одной силы)
    @staticmethod
    def TwoPairs(hand):
        Cards.SortHand(hand)
        if (hand[0].strenght == hand[1].strenght and hand[2].strenght == hand[3].strenght) or\
                (hand[4].strenght == hand[3].strenght and hand[2].strenght == hand[1].strenght):
            return True
        else:
            return False

    # проверка на одну пару (пара карт одной силы)
    @staticmethod
    def OnePair(hand):
        Cards.SortHand(hand)

        if hand[0].strenght == hand[1].strenght or hand[1].strenght == hand[2].strenght\
                or hand[2].strenght == hand[3].strenght or hand[3].strenght == hand[4].strenght:
            return True
        else:
            return False

    # нахождение старшей карты, если нет ни одной комбинации
    @staticmethod
    def HighCard(hand):
        Cards.SortHand(hand)
        return hand[0].strenght


# deck = []
# hand = []
# Cards.RefreshDeck(deck)
# Cards.ShuffleDeck(deck)
# Cards.GetHand(deck, hand)
# Cards.SortHand(hand)
# Cards.RecalculateNumbers(hand)
# for card in hand:
#    print(str.format("{}|{}{}", card.numberInHand, card.name, card.suit))
# Cards.printHandConfig(hand)
