import socket
import threading
from VigenerCipher import VigenersCipher


class ChatServer:
    def __init__(self):
        self.host_IP = socket.gethostbyname(socket.gethostname())
        self.port = 12345
        self.MaxClients = 20
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_IP, self.port))
        self.server.listen(self.MaxClients)
        self.ClientsList = []
        self.UserNamesList = []
        self.klucz = "WHATSAPE"
        self.szyfr_vigenera = VigenersCipher(self.klucz)
        self.AccountsCredentials = self.load_user_credentials()

    def load_user_credentials(self):
        user_credentials = {}
        with open("user_credentials.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                username, password = line.strip().split(":")
                user_credentials[username] = password
        return user_credentials

    def broadcast_message(self, message):
        CipherText = self.szyfr_vigenera.szyfruj(message)
        for client in self.ClientsList:
            client.send(CipherText.encode("utf-8"))

    def handle_client(self, client):
        while True:
            try:
                message0 = client.recv(4096)
                message0 = message0.decode("utf-8")
                message1 = message2 = self.szyfr_vigenera.deszyfruj(message0)

                #KICK/BAN - admin
                if message1.startswith("KICK"):
                    if self.UserNamesList[self.ClientsList.index(client)] == "admin":
                        ToBeKicked = message1[5:]
                        self.kick_user(ToBeKicked)
                    else:
                        msg = "Nie masz uprawnień!"
                        Cypher = self.szyfr_vigenera.szyfruj(msg)
                        client.send(Cypher.encode("utf-8"))

                elif message1.startswith("BAN"):
                    if self.UserNamesList[self.ClientsList.index(client)] == "admin":
                        ToBeBanned = message1[4:]
                        self.kick_user(ToBeBanned)
                        with open("BAN_LIST.txt", "a") as f:
                            f.write(f"{ToBeBanned}\n")
                        print(f"{ToBeBanned} został zbanowany!")
                    else:
                        msg = "Nie masz uprawnień!"
                        Cypher = self.szyfr_vigenera.szyfruj(msg)
                        client.send(Cypher.encode("utf-8"))

                #PUBLIC / PRIVATE 
                elif message2.startswith("1"):
                    self.broadcast_message(message2)
                    

                elif message2.startswith("2"):
                    MsgParts = message2.split("|")
                    Destination = MsgParts[1]
                    Sender = MsgParts[2]
                    MsgContent = MsgParts[3]
                    if Destination in self.UserNamesList:
                        UserIndex = self.UserNamesList.index(Destination)
                        Destinationclient = self.ClientsList[UserIndex]
                        
                        PvMsgDestination=f"{Destination}|{Sender}|{MsgContent}"
                        CipherPvMsgDestination=self.szyfr_vigenera.szyfruj(PvMsgDestination)
                        Destinationclient.send(CipherPvMsgDestination.encode("utf-8"))

                        PvMsgSender=f"{Sender}|{Destination}|{MsgContent}"
                        CipherPvMsgSender = self.szyfr_vigenera.szyfruj(PvMsgSender)
                        client.send(CipherPvMsgSender.encode("utf-8"))
                        





            except:
                if client in self.ClientsList:
                    index = self.ClientsList.index(client)
                    self.ClientsList.remove(client)
                    client.close()

                    UserName = self.UserNamesList[index]
                    ExitMessage = f"{UserName} opuścił chat"
                    print(ExitMessage)
                    self.broadcast_message(ExitMessage)

                    self.UserNamesList.remove(UserName)
                    break

    def receive_users(self):
        while True:
            client, IP_Adress = self.server.accept()
            ConnectMessage = f"Połączono z {str(IP_Adress)}"
            print(ConnectMessage)

            FlagINIT = "FLAG_INIT"
            CypherFlagInit = self.szyfr_vigenera.szyfruj(FlagINIT)
            client.send(CypherFlagInit.encode("utf-8"))

            SuccesfullLoginAttempt = False

            # rejestracja/logowanie
            logtype = client.recv(4096).decode("utf-8")

            #########################################################################################################################
            if logtype == "1":
                while SuccesfullLoginAttempt == False:
                    print("JSDJDJSAJA")
                    UserNameEncrypted = client.recv(4096).decode("utf-8")
                    UserName = self.szyfr_vigenera.deszyfruj(UserNameEncrypted)
                    print(f"------test deszyfracji rejestracja =[{UserName}]")

                    with open("BAN_LIST.txt", "r") as f:
                        bans = f.readlines()

                    if UserName + "\n" in bans:
                        FlagBAN = "FLAG_BAN"
                        CypherFlagBAN = self.szyfr_vigenera.szyfruj(FlagBAN)
                        client.send(f"{CypherFlagBAN}".encode("utf-8"))

                        client.close()
                        continue

                    if UserName in self.AccountsCredentials:
                        taken = "USERNAME_TAKEN"
                        Flagtaken = self.szyfr_vigenera.szyfruj(taken)
                        client.send(Flagtaken.encode("utf-8"))
                        continue  #### Nie wiem czy to tutaj odpowiednie
                    else:
                        Succes = "REGISTER_SUCCESS"
                        Succes = self.szyfr_vigenera.szyfruj(Succes)
                        client.send(Succes.encode("utf-8"))

                        Encryptedpassword = client.recv(4096).decode("utf-8")
                        password = self.szyfr_vigenera.deszyfruj(Encryptedpassword)

                        self.AccountsCredentials[UserName] = password

                        with open("user_credentials.txt", "a") as f:
                            f.write(f"{UserName}:{password}\n")

                        print(self.AccountsCredentials)

                        SuccesfullLoginAttempt = True

            elif logtype == "2":
                print("JSDJDJSAJA")
                while not SuccesfullLoginAttempt:
                    UserNameEncrypted = client.recv(4096).decode("utf-8")
                    UserName = self.szyfr_vigenera.deszyfruj(UserNameEncrypted)
                    print(f"------test deszyfracji login =[{UserName}]")

                    CorrectPassword = False

                    with open("BAN_LIST.txt", "r") as f:
                        bans = f.readlines()

                    if UserName + "\n" in bans:
                        FlagBAN = "FLAG_BAN"
                        CypherFlagBAN = self.szyfr_vigenera.szyfruj(FlagBAN)
                        client.send(f"{CypherFlagBAN}".encode("utf-8"))

                        client.close()
                        continue

                    if UserName in self.AccountsCredentials:
                        taken = "LOGIN_SUCCESS"
                        Flagtaken = self.szyfr_vigenera.szyfruj(taken)
                        client.send(Flagtaken.encode("utf-8"))

                        while CorrectPassword != True:
                            Encryptedpassword = client.recv(4096).decode("utf-8")
                            password = self.szyfr_vigenera.deszyfruj(Encryptedpassword)
                            if password == self.AccountsCredentials[UserName]:
                                FlagGood = "FLAG_Good_Password"
                                CypherFlagGood = self.szyfr_vigenera.szyfruj(FlagGood)
                                client.send(f"{CypherFlagGood}".encode("utf-8"))

                                print(self.AccountsCredentials)
                                SuccesfullLoginAttempt = True
                                CorrectPassword = True
                            else:
                                FlagWrng = "FLAG_Wrong_Password"
                                CypherFlagWrng = self.szyfr_vigenera.szyfruj(FlagWrng)
                                client.send(f"{CypherFlagWrng}".encode("utf-8"))
                                continue
                    else:
                        NoUser = "No_User"  ### JESLI NIE MA KONTA A LOGIN To WYWAL APKE
                        print("no user")
                        NoUser = self.szyfr_vigenera.szyfruj(NoUser)
                        client.send(NoUser.encode("utf-8"))
                        client.close()
                        client = None
                        SuccesfullLoginAttempt = True
                        CorrectPassword = True
                        break

            #########################################################################################################################

            if client != None:
                self.UserNamesList.append(UserName)
                self.ClientsList.append(client)

                print(f"Nowy użytkownik: {UserName}")
                WelcomeMsg = f"{UserName} dołączył do chat'u"
                self.broadcast_message(WelcomeMsg)

                Wlcome = "\nPodłaczono do chat'u"
                CypherWlcome = self.szyfr_vigenera.szyfruj(Wlcome)
                client.send(CypherWlcome.encode("utf-8"))

                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()

    def kick_user(self, name):
        if name in self.UserNamesList:
            UserIndex = self.UserNamesList.index(name)
            kicked_client = self.ClientsList[UserIndex]
            self.ClientsList.remove(kicked_client)

            Kickmsg = "ZOSTAŁEŚ WYRZUCONY PRZEZ ADMINA!"
            CypherKickmsg = self.szyfr_vigenera.szyfruj(Kickmsg)
            kicked_client.send(CypherKickmsg.encode("utf-8"))

            kicked_client.close()
            self.UserNamesList.remove(name)

            KickmsgALL = f"{name} został wyrzucony przez Admina!"
            self.broadcast_message(KickmsgALL)

if __name__ == "__main__":
    chat_server = ChatServer()
    print("Serwer został uruchomiony...")
    chat_server.receive_users()