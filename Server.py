import socket
import threading

from VigenerCipher import VigenersCipher

klucz = "ONLYMESSAGE"
szyfr_vigenera = VigenersCipher(klucz)


host_IP = socket.gethostbyname(socket.gethostname())  # Pobranie ip hosta
port = 12345
MaxClients = 20

# AF_INET - IPv4, SOCK_STREAM - tcp / SOCK_DGRAM - udp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host_IP, port))  # Przypisanie serwerowi IP oraz portu

server.listen(MaxClients)

ClientsList = []
UserNamesList = []


# Wysylanie wiadomosci do wszystkich klientow (broadcast)
def ServerToClients(message):
    CipherText = szyfr_vigenera.szyfruj(message)
    for client in ClientsList:
        client.send(CipherText.encode("utf-8"))


def ClientHandle(client):
    while True:
        try:
            message0 = client.recv(1024)
            message0 = message0.decode("utf-8")
            message1 = message2 = szyfr_vigenera.deszyfruj(message0)

            if message1.startswith("KICK"):
                if UserNamesList[ClientsList.index(client)] == "admin":
                    ToBeKicked = message1[5:]

                    Kick_User(ToBeKicked)
                else:
                    msg = "Nie masz uprawnień!"
                    Cypher = szyfr_vigenera.szyfruj(msg)
                    client.send(Cypher.encode("utf-8"))

            if message1.startswith("BAN"):
                if UserNamesList[ClientsList.index(client)] == "admin":
                    ToBeBanned = message1[4:]
                    Kick_User(ToBeBanned)
                    with open("BAN_LIST.txt", "a") as f:
                        f.write(f"{ToBeBanned}\n")
                    print(f"{ToBeBanned} został zbanowany!")
                else:
                    msg = "Nie masz uprawnień!"
                    Cypher = szyfr_vigenera.szyfruj(msg)
                    client.send(Cypher.encode("utf-8"))
            else:
                ServerToClients(message2)
        except:
            if client in ClientsList:
                index = ClientsList.index(client)
                ClientsList.remove(client)
                client.close()

                UserName = UserNamesList[index]
                ExitMessage = f"{UserName} opuścił chat"
                ServerToClients(ExitMessage)

                UserNamesList.remove(UserName)
                break


def ReceiveMessages():
    while True:
        client, IP_Adress = server.accept()
        ConnectMessage = f"Połączono z {str(IP_Adress)}"
        print(ConnectMessage)

        FlagINIT = "FLAG_INIT"
        CypherFlagInit = szyfr_vigenera.szyfruj(FlagINIT)
        client.send(CypherFlagInit.encode("utf-8"))

        UserNameEncrypted = client.recv(1024).decode("utf-8")
        UserName = szyfr_vigenera.deszyfruj(UserNameEncrypted)
        print(f"------test =[{UserName}]")  ##############################

        with open("BAN_LIST.txt", "r") as f:
            bans = f.readlines()

        if UserName + "\n" in bans:
            FlagBAN = "FLAG_BAN"
            CypherFlagBAN = szyfr_vigenera.szyfruj(FlagBAN)
            client.send(f"{CypherFlagBAN}".encode("utf-8"))

            client.close()
            continue

        if UserName == "admin":
            FlagAdminPass = "FLAG_ADMIN_PASSWORD"
            CypherFlagAdmPass = szyfr_vigenera.szyfruj(FlagAdminPass)
            client.send(f"{CypherFlagAdmPass}".encode("utf-8"))
            print("Próba zalogowania na admina")

            AdminPasswordEncrypt = client.recv(1024).decode("utf-8")
            AdminPassword = szyfr_vigenera.deszyfruj(AdminPasswordEncrypt)
            # tutaj zamienic haslo na hash hasła
            if AdminPassword != "123":
                FlagWrng = "FLAG_Wrong_Password"
                CypherFlagWrng = szyfr_vigenera.szyfruj(FlagWrng)
                client.send(f"{CypherFlagWrng}".encode("utf-8"))
                client.close()
                continue

        UserNamesList.append(UserName)
        ClientsList.append(client)

        print(f"Nowy użytkownik: {UserName}")
        WelcomeMsg = f"{UserName} dołączył do chat'u"
        ServerToClients(WelcomeMsg)

        Wlcome = "Podłaczono do chat'u"
        CypherWlcome = szyfr_vigenera.szyfruj(Wlcome)
        client.send(CypherWlcome.encode("utf-8"))

        thread = threading.Thread(target=ClientHandle, args=(client,))
        thread.start()


def Kick_User(name):
    if name in UserNamesList:
        UserIndex = UserNamesList.index(name)
        kicked_client = ClientsList[UserIndex]
        ClientsList.remove(kicked_client)

        Kickmsg = "ZOSTAŁEŚ WYRZUCONY PRZEZ ADMINA!"
        CypherKickmsg = szyfr_vigenera.szyfruj(Kickmsg)
        kicked_client.send(CypherKickmsg.encode("utf-8"))

        kicked_client.close()
        UserNamesList.remove(name)

        KickmsgALL = f"{name} został wyrzucony przez Admina!"
        ServerToClients(KickmsgALL)


print("Serwer został uruchomiony...")
ReceiveMessages()
