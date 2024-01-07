import socket
import threading




from Fernet import FernetGenerator

f = FernetGenerator.generate_key()



host_IP = socket.gethostbyname(socket.gethostname()) #Pobranie ip hosta 
port = 12345
MaxClients = 20

# AF_INET - IPv4, SOCK_STREAM - tcp / SOCK_DGRAM - udp 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

server.bind((host_IP, port))  # Przypisanie serwerowi IP oraz portu

server.listen(MaxClients)

ClientsList = []
UserNamesList= []


# Wysylanie wiadomosci do wszystkich klientow (broadcast)
def ServerToClients(message):
    message = f.encrypt(bytes(message,'UTF-8'))
    for client in ClientsList:
        client.send(message)

def ClientHandle(client):
    while True:
        try:
            f = FernetGenerator.generate_key()
            message0 = client.recv(1024)
            message1 = message2 = f.decrypt(message0)
            
            if message1.decode("utf-8").startswith("KICK"):
                if UserNamesList[ClientsList.index(client)] == 'admin':
                    ToBeKicked = message1.decode("utf-8")[5:]
                    
                    Kick_User(ToBeKicked)
                else:
                    msg = f"Nie masz uprawnień!"
                    Cypher = f.encrypt(bytes(msg,'UTF-8'))
                    client.send(f"{Cypher}".encode("utf-8"))

            if message1.decode("utf-8").startswith("BAN"):
                if UserNamesList[ClientsList.index(client)] == 'admin':
                    ToBeBanned = message1.decode("utf-8")[4:]
                    Kick_User(ToBeBanned)
                    with open("BAN_LIST.txt", "a") as f:
                        f.write(f"{ToBeBanned}\n")
                    print(f"{ToBeBanned} został zbanowany!")
                else:
                    msg = f"Nie masz uprawnień!"
                    Cypher = f.encrypt(bytes(msg,'UTF-8'))
                    client.send(f"{Cypher}".encode("utf-8"))
            else:
                CypherToAll = f.encrypt(bytes(message2,'UTF-8'))
                ServerToClients(CypherToAll)
        except:
            if client in ClientsList:
                index = ClientsList.index(client)
                ClientsList.remove(client)
                client.close()
                
                UserName = UserNamesList[index]
                ExitMessage = f"{UserName} opuścił chat"
                CypherExitMessage = f.encrypt(bytes(ExitMessage,'UTF-8'))
                ServerToClients(f"{CypherExitMessage}".encode('utf-8'))

                UserNamesList.remove(UserName)
                break

def ReceiveMessages():
    while True:
        client, IP_Adress = server.accept()
        ConnectMessage = f"Połączono z {str(IP_Adress)}"

        f = FernetGenerator.generate_key()
       
        
        print(ConnectMessage)
        
        FlagINIT = "FLAG_INIT"
        CypherFlagInit = f.encrypt(bytes(FlagINIT,'UTF-8'))
        client.send(f"{CypherFlagInit}".encode("utf-8"))
        UserNameEncrypted = client.recv(1024).decode("utf-8")
        UserName = f.decrypt(UserNameEncrypted)

        
        with open("BAN_LIST.txt", "r") as f:
            bans = f.readlines()

        if UserName + "\n" in bans:
            f = FernetGenerator.generate_key()
            FlagBAN = "FLAG_BAN"
            CypherFlagBAN = f.encrypt(bytes(FlagBAN,'UTF-8'))
            client.send(f"{CypherFlagBAN}".encode("utf-8"))

            client.close()
            continue

        if UserName == "admin":
            f = FernetGenerator.generate_key()
            FlagAdminPass = "FLAG_ADMIN_PASSWORD"
            CypherFlagAdmPass= f.encrypt(bytes(FlagAdminPass,'UTF-8'))
            client.send(f"{CypherFlagAdmPass}".encode("utf-8"))
            print("Próba zalogowania na admina")
            AdminPasswordEncrypt = client.recv(1024).decode("utf-8")
            AdminPassword = f.decrypt(AdminPasswordEncrypt)
            #tutaj zamienic haslo na hash hasła
            if AdminPassword != "123":
                FlagWrng = "FLAG_Wrong_Password"
                CypherFlagWrng = f.encrypt(bytes(FlagWrng,'UTF-8'))
                client.send(f"{CypherFlagWrng}".encode("utf-8"))
                client.close()
                continue
            


        UserNamesList.append(UserName)
        ClientsList.append(client)

        print(f"Nowy użytkownik: {UserName}")
        WelcomeMsg = f"{UserName} dołączył do chat'u"
        CypherWelcomeMsg = f.encrypt(bytes(WelcomeMsg,'UTF-8'))
        ServerToClients(f"{CypherWelcomeMsg}".encode("utf-8"))

        Wlcome = "Podłaczono do chat'u"
        CypherWlcome = f.encrypt(bytes(Wlcome,'UTF-8'))
        client.send(f"{CypherWlcome}".encode("utf-8"))

        thread = threading.Thread(target=ClientHandle, args = (client,))
        thread.start()

def Kick_User(name):
    if name in UserNamesList:
        
        UserIndex = UserNamesList.index(name)
        kicked_client = ClientsList[UserIndex]
        ClientsList.remove(kicked_client)

        Kickmsg = f"ZOSTAŁEŚ WYRZUCONY PRZEZ ADMINA!"
        CypherKickmsg = f.encrypt(bytes(Kickmsg,'UTF-8'))
        kicked_client.send(f"{CypherKickmsg}".encode("utf-8"))
        
        kicked_client.close()
        UserNamesList.remove(name)

        KickmsgALL = f"{name} został wyrzucony przez Admina!"
        CypherKickmsgALL = f.encrypt(bytes(KickmsgALL,'UTF-8'))
        ServerToClients(f"{CypherKickmsgALL}".encode("utf-8"))
        

print("Serwer został uruchomiony...")
ReceiveMessages()