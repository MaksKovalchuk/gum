def CheckCommand(command):
    if command == "help":
        return "rules - правила игры\nstart - начать игру\nswap - смена карт\nbalance - текущий баланс" \
               "\nsd - шоудаун(показать карты)\nraise - повысить ставку" \
               "\nstrong - выбрать победу сильной руки\nweak - выбрать победу слабой руки\n"
    elif command == "rules":
        return "Колода на 52 карты\n" \
               "Карты :\nA - туз\nK - король\nQ - дама\nJ - валет, далее все карты обозначены цифрами\n" \
               "Масти :\n<3 - червовая\nx - трефовая\n<> - бубновая\n<^> - пиковая\n" \
               "Основные комбинации(в порядке убывания силы) :\n" \
               "Роял флэш - 5 старших карт одинаковой масти\nСтрит флэш - 5 карт" \
               "одной масти стоящие по порядку (например 9x 8x 7x 6x 5x)\nКаре - 4 карты одной силы\n" \
               "Фулл Хаус - одна тройка и одна пара\nФлэш - пять карт одной масти\nСтрит - пять карт любых мастей" \
               "по порядку, стоит отметить, что туз может как начинать порядок, так и заканчивать его\n" \
               "Сет(тройка) - три карты одной силы\nДве пары - две пары карт одной силы\nОдна пара -" \
               " пара карт одной силы"\
               "Правила игры : каждый игрок в начале игры получает 100 денежных единиц," \
               " при начале каждой партии все получают по 5 карт,а также ставят по 1 фишке" \
               " (1 - фишка = 1000 денежных единиц), после этого существует возможность заменить" \
               " карты, карты которые вы меняете видны всем игрокам после того как все сменили" \
               " карты начинается фаза ставок, каждый игрок может поставить дополнительные фишки," \
               "в отличии от обычного покера, тут нельзя уравнивать ставку, её можно только повышать" \
               ", после окончания ставок игрок с наивысшей ставкой получает право выбора : сильнее или " \
               "слабее. При выборе 'сильнее', то как и в обычном покере побеждает игрок с более сильной" \
               " рукой, при выборе 'слабее' всё наоборот - выигравает человек, чья рука слабее, если" \
               "ни у одного из игроков нет комбинации(у обоих старшая карта), то вне зависимости от вы" \
               "бора выигрывает игрок с сильнейшей старшей картой, если у обоих игроков самая старшая карта" \
               "имеет одинаковую силу, то смотрится по второй по силе карте и т.д.\n"
    elif command == "start":
        return "Starting the game\n"
    elif command == "swap":
        return "Swapping the cards"
    elif command == "sd":
        return "SHOWDOWN!!!!!!!!"
    elif command == "raise":
        return "increasing bet"
    elif command == "strong":
        return "strong hand was chosen"
    elif command == "weak":
        return "weak hand was chosen"
    else:
        return "UC"


def GetHandToSend(hand):
    handToSend = []
    for card in hand:
        handToSend.append(str.format("{}|{}{}", card.numberInHand, card.name, card.suit))

    return handToSend


def FindPlayerWithBiggestBet(bets):
    biggest = max(bets.values())
    for player, bet in bets.items():
        if bet == biggest:
            return player
        else:
            pass


def FindBiggestBet(bets):
    biggest = max(bets.values())
    return biggest


def WaitForAnswer():
    i = 0
    while i < 1000000:
        i += 1