from Cards import Cards
import threading
import socket
import pickle
import time
import sys

class Server(object):
    def __init__(self, host="localhost", port=5555):

        self.fp = ""
        self.sp = ""
        self.deck = []
        self.FPhand = []
        self.SPHand = []
        self.clients = []
        self.bets = ["", ""]
        self.FPDoneBet = False
        self.SPDoneBet = False
        self.FPShowdown = False
        self.SPShowdown = False
        self.gameStarted = False
        self.FPhandStrenght = 0
        self.SPhandStrenght = 0
        self.StrongHandWins = None
        self.restartVote = 0

        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(2)
        self.sock.setblocking(0)

        acceptor = threading.Thread(target=self.acceptorCon)
        processor = threading.Thread(target=self.processorCon)

        acceptor.daemon = True
        processor.daemon = True
        acceptor.start()
        processor.start()

        Cards.RefreshDeck(self.deck)
        Cards.ShuffleDeck(self.deck)

        while True:
            message = input("=>")
            if message == "exit":
                self.sock.close()
                sys.exit()
            else:
                pass

    def stopGame(self):
        self.sock.close()
        time.sleep(3)
        sys.exit()

    def restart(self):
        self.deck = []
        self.FPhand = []
        self.SPHand = []
        self.clients = []
        self.bets = ["", ""]
        self.FPDoneBet = False
        self.SPDoneBet = False
        self.FPShowdown = False
        self.SPShowdown = False
        self.FPhandStrenght = 0
        self.SPhandStrenght = 0
        self.StrongHandWins = None
        self.restartVote = 0

        Cards.RefreshDeck(self.deck)
        Cards.ShuffleDeck(self.deck)
        self.msgToPlayers("restart")
        self.msgToPlayers("Колода обновлена, наберите start для начала следующего раунда")

    def msgToAll(self, message, client):
        for c in self.clients:
            try:
                if c != client:
                    c.send(message)
            except:
                self.clients.remove(c)

    def msgToPlayers(self, message):
        for c in self.clients:
            try:
                c.send(pickle.dumps(message))
            except:
                self.clients.remove(c)

    def acceptorCon(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                if not self.fp:
                    self.fp = conn
                elif not self.sp:
                    self.sp = conn
                conn.setblocking(0)
                self.clients.append(conn)
            except:
                pass

    def processorCon(self):
        while True:
                if len(self.clients) == 2:
                    self.msgToPlayers("canStart")
                for c in self.clients:
                    try:
                        data = c.recv(2048)
                        dataPrint = pickle.loads(data)
                        print(dataPrint)
                        if dataPrint == "start":
                            if c is self.fp:
                                c.send(pickle.dumps("hand"))
                                Cards.GetHand(self.deck, self.FPhand)
                                Cards.SortHand(self.FPhand)
                                Cards.RecalculateNumbers(self.FPhand)
                                sendHand = self.FPhand
                                c.sendto(pickle.dumps(sendHand), c.getpeername())
                            elif c is self.sp:
                                c.send(pickle.dumps("hand"))
                                Cards.GetHand(self.deck, self.SPHand)
                                Cards.SortHand(self.SPHand)
                                Cards.RecalculateNumbers(self.SPHand)
                                c.sendto(pickle.dumps(self.SPHand), c.getpeername())
                        elif dataPrint == "strong":
                            self.msgToAll(pickle.dumps("Противник сделал выбор в пользу сильной руки"), c)
                            self.StrongHandWins = True
                        elif dataPrint == "weak":
                            self.msgToAll(pickle.dumps("Противник сделал выбор в пользу слабой руки"), c)
                            self.StrongHandWins = False
                        elif type(dataPrint) is list and dataPrint[0] == "swap":
                            if c is self.fp:
                                swapList = dataPrint
                                swappedCards = Cards.SwapCards(swapList, self.FPhand)
                                sendCardsSwapped = ["swappedCards"]
                                sendCardsSwapped.extend(swappedCards)
                                self.msgToAll(pickle.dumps(sendCardsSwapped), c)
                                Cards.ExpandHand(self.deck, self.FPhand)
                                Cards.SortHand(self.FPhand)
                                Cards.RecalculateNumbers(self.FPhand)
                                c.sendto(pickle.dumps("hand"), c.getpeername())
                                c.sendto(pickle.dumps(self.FPhand), c.getpeername())
                            elif c is self.sp:
                                swapList = dataPrint
                                swappedCards = Cards.SwapCards(swapList, self.SPHand)
                                sendCardsSwapped = ["swappedCards"]
                                sendCardsSwapped.extend(swappedCards)
                                self.msgToAll(pickle.dumps(sendCardsSwapped), c)
                                Cards.ExpandHand(self.deck, self.SPHand)
                                Cards.SortHand(self.SPHand)
                                Cards.RecalculateNumbers(self.SPHand)
                                c.sendto(pickle.dumps("hand"), c.getpeername())
                                c.sendto(pickle.dumps(self.SPHand), c.getpeername())
                        elif type(dataPrint) is list and dataPrint[0] == "bet":
                            if c is self.fp:
                                self.msgToAll(pickle.dumps("Первый игрок повысил ставку до " + str(dataPrint[1])), c)
                            elif c is self.sp:
                                self.msgToAll(pickle.dumps("Второй игрок повысил ставку до " + str(dataPrint[1])), c)
                        elif type(dataPrint) is list and dataPrint[0] == "stbet":
                            if c is self.fp:
                                self.FPDoneBet = True
                                self.bets[0] = dataPrint[1]
                                self.msgToAll(pickle.dumps("Окончательная ставка первого игрока : " + str(dataPrint[1])), c)
                                if self.SPDoneBet and int(self.bets[0]) > int(self.bets[1]):
                                    c.sendto(pickle.dumps("chooseRight"), c.getpeername())
                                elif self.SPDoneBet and int(self.bets[0]) < int(self.bets[1]):
                                    self.msgToAll(pickle.dumps("chooseRight"), c)
                            elif c is self.sp:
                                self.SPDoneBet = True
                                self.bets[1] = dataPrint[1]
                                self.msgToAll(pickle.dumps("Окончательная ставка второго игрока :" + str(dataPrint[1])), c)
                                if self.FPDoneBet and int(self.bets[0]) > int(self.bets[1]):
                                    self.msgToAll(pickle.dumps("chooseRight"), c)
                                elif self.FPDoneBet and int(self.bets[0]) < int(self.bets[1]):
                                    c.sendto(pickle.dumps("chooseRight"), c.getpeername())
                        elif type(dataPrint) is list and dataPrint[0] == "sd":
                            if c is self.fp:
                                self.FPShowdown = True
                                self.FPhand = dataPrint[1]
                                if self.SPShowdown:
                                    winCondition = Cards.chooseWinner(self.StrongHandWins, self.FPhand, self.SPHand)
                                    if winCondition == 0:
                                        self.msgToPlayers(["FP", self.FPhand, self.SPHand, self.bets[0], self.bets[1]])
                                    elif winCondition == 1:
                                        self.msgToPlayers(["SP", self.FPhand, self.SPHand, self.bets[1], self.bets[0]])
                            elif c is self.sp:
                                self.SPHand = dataPrint[1]
                                self.SPShowdown = True
                                if self.FPShowdown:
                                    winCondition = Cards.chooseWinner(self.StrongHandWins, self.FPhand, self.SPHand)
                                    if winCondition == 0:
                                        self.msgToPlayers(["FP", self.FPhand, self.SPHand, self.bets[0], self.bets[1]])
                                    elif winCondition == 1:
                                        self.msgToPlayers(["SP", self.FPhand, self.SPHand, self.bets[1], self.bets[0]])
                        elif dataPrint == "OutOfMoney":
                            if c is self.fp:
                                self.msgToPlayers("У первого игрока закончились фишки")
                                time.sleep(3)
                                self.sock.close()
                                sys.exit()
                            elif c is self.sp:
                                self.msgToPlayers("У второго игрока закончились фишки")
                                self.stopGame()

                        elif dataPrint == "stop":
                            if c is self.fp:
                                self.msgToPlayers("Первый игрок решил закончить игру")
                                self.stopGame()
                            elif c is self.sp:
                                self.msgToPlayers("Второй игрок решил закончить игру")
                                self.stopGame()

                        elif dataPrint == "restart":
                            self.restartVote += 1
                            if self.restartVote == 2:
                                self.restart()
                    except:
                        pass

s = Server()
