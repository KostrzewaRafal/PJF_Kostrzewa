import socket
import threading

from VigenerCipher import PseudoRandomBytesGenerator
from Cryptodome.Cipher import AES

seed = 42 
prbg = PseudoRandomBytesGenerator(seed)

key = prbg.generate_bytes(16)

cipher = AES.new(key, AES.MODE_EAX)
d_cipher = AES.new(key, AES.MODE_EAX, cipher.nonce)






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
    for client in ClientsList:
        client.send(f"{message}".encode())

def ClientHandle(client):
    while True:
        try:
           
            message0 = client.recv(1024)
            message1 = message2 = d_cipher.decrypt(message0)
            
            if message1.decode("utf-8").startswith("KICK"):
                if UserNamesList[ClientsList.index(client)] == 'admin':
                    ToBeKicked = message1.decode("utf-8")[5:]
                    
                    Kick_User(ToBeKicked)
                else:
                    msg = f"Nie masz uprawnień!"
                    Cypher = cipher.encrypt(bytes(msg,'UTF-8'))
                    client.send(f"{Cypher}".encode())

            if message1.decode("utf-8").startswith("BAN"):
                if UserNamesList[ClientsList.index(client)] == 'admin':
                    ToBeBanned = message1.decode("utf-8")[4:]
                    Kick_User(ToBeBanned)
                    with open("BAN_LIST.txt", "a") as f:
                        f.write(f"{ToBeBanned}\n")
                    print(f"{ToBeBanned} został zbanowany!")
                else:
                    msg = f"Nie masz uprawnień!"
                    Cypher = cipher.encrypt(bytes(msg,'UTF-8'))
                    client.send(f"{Cypher}".encode())
            else:
                message2 = message2.decode("utf-8")
                CypherToAll = cipher.encrypt(bytes(message2,'UTF-8'))
                ServerToClients(CypherToAll)
        except:
            if client in ClientsList:
                index = ClientsList.index(client)
                ClientsList.remove(client)
                client.close()
                
                UserName = UserNamesList[index]
                ExitMessage = f"{UserName} opuścił chat"
                CypherExitMessage = cipher.encrypt(bytes(ExitMessage,'UTF-8'))
                ServerToClients(CypherExitMessage)

                UserNamesList.remove(UserName)
                break

def ReceiveMessages():
    while True:
        client, IP_Adress = server.accept()
        ConnectMessage = f"Połączono z {str(IP_Adress)}"
        print(ConnectMessage)
        
        FlagINIT = "FLAG_INIT"
        CypherFlagInit = cipher.encrypt(bytes(FlagINIT,'UTF-8'))
        client.send(f"{CypherFlagInit}".encode())
        UserNameEncrypted = client.recv(1024)
        UserName = d_cipher.decrypt(UserNameEncrypted).decode("utf-8")
        print(f"------test =[{UserName}]") ##############################3
        
        with open("BAN_LIST.txt", "r") as f:
            bans = f.readlines()

        if UserName + "\n" in bans:
            
            FlagBAN = "FLAG_BAN"
            CypherFlagBAN = cipher.encrypt(bytes(FlagBAN,'UTF-8'))
            client.send(f"{CypherFlagBAN}".encode())

            client.close()
            continue

        if UserName == "admin":
            FlagAdminPass = "FLAG_ADMIN_PASSWORD"
            CypherFlagAdmPass = cipher.encrypt(bytes(FlagAdminPass,'UTF-8'))
            client.send(f"{CypherFlagAdmPass}".encode())
            print("Próba zalogowania na admina")
            AdminPasswordEncrypt = client.recv(1024)
            AdminPassword = d_cipher.decrypt(AdminPasswordEncrypt).decode("utf-8")
            #tutaj zamienic haslo na hash hasła
            if AdminPassword != "123":
                FlagWrng = "FLAG_Wrong_Password"
                CypherFlagWrng = cipher.encrypt(bytes(FlagWrng,'UTF-8'))
                client.send(f"{CypherFlagWrng}".encode())
                client.close()
                continue
            


        UserNamesList.append(UserName)
        ClientsList.append(client)

        print(f"Nowy użytkownik: {UserName}")
        WelcomeMsg = f"{UserName} dołączył do chat'u"
        CypherWelcomeMsg = cipher.encrypt(bytes(WelcomeMsg,'UTF-8'))
        ServerToClients(f"{CypherWelcomeMsg}".encode())

        Wlcome = "Podłaczono do chat'u"
        CypherWlcome = cipher.encrypt(bytes(Wlcome,'UTF-8'))
        client.send(f"{CypherWlcome}".encode())

        thread = threading.Thread(target=ClientHandle, args = (client,))
        thread.start()

def Kick_User(name):
    if name in UserNamesList:
        
        UserIndex = UserNamesList.index(name)
        kicked_client = ClientsList[UserIndex]
        ClientsList.remove(kicked_client)

        Kickmsg = f"ZOSTAŁEŚ WYRZUCONY PRZEZ ADMINA!"
        CypherKickmsg = cipher.encrypt(bytes(Kickmsg,'UTF-8'))
        kicked_client.send(f"{CypherKickmsg}".encode())
        
        kicked_client.close()
        UserNamesList.remove(name)

        KickmsgALL = f"{name} został wyrzucony przez Admina!"
        CypherKickmsgALL = cipher.encrypt(bytes(KickmsgALL,'UTF-8'))
        ServerToClients(CypherKickmsgALL)
        

print("Serwer został uruchomiony...")
ReceiveMessages()