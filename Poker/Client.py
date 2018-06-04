from Cards import Cards
import ServerCommands
import threading
import socket
import pickle
import time
import sys


class Client(object):
    def __init__(self, host="localhost", port=5555):

        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.hand = []
        self.fullBet = 0
        self.balance = 100
        self.canStart = False
        self.canChoose = False
        self.gameEnded = False

        self.gameStarted = False
        self.swaped = False
        self.madeBet = False
        self.canBet = True

        msg_recv = threading.Thread(target=self.msg_recv)
        msg_recv.daemon = True
        msg_recv.start()

        while True:
            message = input()
            if message == "help":
                print(ServerCommands.CheckCommand(message))
            elif message == "rules":
                print(ServerCommands.CheckCommand(message))
            elif message and not self.canStart:
                print("Ожидание второго игрока")
            elif message == "start" and not self.gameStarted and self.canStart:
                self.gameStarted = True
                self.send_msg(message)
                self.balance -= 1
                self.fullBet += 1
            elif message == "start" and self.gameStarted:
                print("Вы уже начали игру")
            elif message == "swap" and not self.swaped and self.gameStarted and not self.madeBet:
                self.swaped = True
                swapList = []
                amountToSwap = int(input("Сколько карт вы хотите поменять?"))
                if int(amountToSwap) == 5:
                    swapList.append("1")
                    swapList.append("2")
                    swapList.append("3")
                    swapList.append("4")
                    swapList.append("5")
                    swapList.insert(0, str(amountToSwap))
                    swapList.insert(0, "swap")
                    self.send_msg(swapList)
                elif 0 < amountToSwap < 5:
                    while len(swapList) < int(amountToSwap):
                        cardToSwap = int(input("Введите номер карты, которую хотите заменить:"))
                        if str(cardToSwap) not in swapList and 0 < int(cardToSwap) < 6:
                            swapList.append(str(cardToSwap))
                        else:
                            print("Неверный номер карты, либо вы уже и так запросили обмен данной карты")
                        if len(swapList) == int(amountToSwap):
                            break
                    swapList.insert(0, str(amountToSwap))
                    swapList.insert(0, "swap")
                    self.send_msg(swapList)
                elif amountToSwap == 0:
                    pass
                else:
                    print("Некорректное число карт")
            elif message == "swap" and self.swaped:
                print("Обмен карт возможен только 1 раз")
            elif message == "swap" and not self.gameStarted:
                print("Данная команда недоступна на этом этапе")
            elif message == "swap" and self.madeBet:
                print("После совершения ставки обмен карт уже невозможен")
            elif message == "balance":
                print("Ваш текущий баланс", self.balance)
            elif message == "raise" and not self.gameStarted:
                print("Данная команда недоступна на этом этапе")
            elif message == "raise" and self.balance == 0 and self.gameStarted:
                print("У вас больше нет средств, чтобы повысить ставку")
            elif message == "raise" and not self.canBet:
                print("Вы уже завершили ставку")
            elif message == "raise" and self.balance > 0 and self.gameStarted and self.canBet:
                bet = int(input("На сколько вы хотите поднять ставку? :"))
                if bet > self.balance:
                    print("Ставка превышает ваш баланс")
                else:
                    self.madeBet = True
                    self.fullBet += bet
                    self.balance -= bet
                    print("Ставка повышена до", str(self.fullBet))
                    self.send_msg(["bet", str(self.fullBet)])
            elif message == "bet" and not self.gameStarted:
                print("Данная команда недоступна на этом этапе")
            elif message == "bet" and self.gameStarted:
                print("Ваша ставка :", self.fullBet)
            elif message == "stbet" and not self.gameStarted:
                print("Данная команда недоступна на этом этапе")
            elif message == "stbet" and not self.madeBet and self.gameStarted:
                print("Сначала необходимо сделать ставку")
            elif message == "stbet" and self.gameStarted and self.madeBet:
                self.canBet = False
                print("Ваша окончательная ставка :", self.fullBet)
                self.send_msg(["stbet", self.fullBet])
            elif (message == "strong" or message == "weak") and not self.gameStarted:
                print("Данная команда недоступна на этом этапе")
            elif (message == "strong" or message == "weak") and not self.canChoose:
                print("У вас нет права выбора победной руки")
            elif message == "strong" and self.canChoose:
                self.send_msg("strong")
                print("Выбор сильной руки подтверждён")
            elif message == "weak" and self.canChoose:
                self.send_msg("weak")
                print("Выбор слабой руки подтверждён")
            elif message == "sd" and not self.gameStarted:
                print("Данная команда недоступна на этом этапе")
            elif message == "sd" and not self.madeBet:
                print("Сначала сделайте ставку")
            elif message == "sd" and self.gameStarted and self.madeBet:
                sendList = ["sd", self.hand]
                self.send_msg(sendList)

            elif message == "exit":
                self.sock.close()
                sys.exit()
            else:
                self.send_msg(message)

    def restart(self):
        self.hand = []
        self.fullBet = 0
        self.canChoose = False
        self.gameEnded = False

        self.gameStarted = False
        self.swaped = False
        self.madeBet = False
        self.canBet = True
    
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(2048)
                dataReceived = pickle.loads(data)
                if dataReceived == "canStart" and not self.canStart:
                    self.canStart = True
                    print("Оба игрока подключены. Теперь можно начать игру")
                elif dataReceived == "canStart" and self.canStart:
                    pass
                elif type(dataReceived) is list and str(dataReceived[0]) == "swappedCards":
                    dataReceived.pop(0)
                    for row in dataReceived:
                        print("Противник поменял карту : " + str(row))
                elif dataReceived == "hand":
                    self.hand = pickle.loads(self.sock.recv(2048))
                    for card in self.hand:
                        print(str.format("{}|{}{}", card.numberInHand, card.name, card.suit))
                elif dataReceived == "chooseRight":
                    self.canChoose = True
                    print("Теперь вы можете сделать выбор между победой сильной и слабой руки")
                elif type(dataReceived) is list and (str(dataReceived[0]) == "FP" or str(dataReceived[0]) == "SP"):
                    if str(dataReceived[0]) == "FP":
                        print("Победа первого игрока")
                        print("Рука первого игрока")
                        Cards.printHandConfig(dataReceived[1])
                        print("##############")
                        print("Рука второго игрока")
                        Cards.printHandConfig(dataReceived[2])
                        if int(dataReceived[3]) == int(self.fullBet):
                            self.balance += int(dataReceived[3]) + int(dataReceived[4])
                        else:
                            pass
                    elif str(dataReceived[0]) == "SP":
                        print("Победа второго игрока")
                        print("Рука первого игрока")
                        Cards.printHandConfig(dataReceived[1])
                        print("##############")
                        print("Рука второго игрока")
                        Cards.printHandConfig(dataReceived[2])
                        if int(dataReceived[3]) == int(self.fullBet):
                            self.balance += int(dataReceived[3]) + int(dataReceived[4])
                        else:
                            pass
                        if self.balance < 1:
                            self.send_msg("OutOfMoney")
                        else:
                            answer = input("Хотите сыграть ещё раунд (y/n)?")
                            while answer != "y" or answer != "n":
                                answer = input("Хотите сыграть ещё раунд (y/n)?")
                            if answer == "n":
                                self.send_msg("stop")
                            else:
                                self.send_msg("restart")
                    elif dataReceived == "restart":
                        self.restart()
                else:
                    print(dataReceived)
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))


c = Client()
