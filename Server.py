import socket
import threading

from key_generator import KeyGenerator
from cryptography.fernet import Fernet


key_generator = KeyGenerator()



UserSeed = "1234"  
key = key_generator.generate_key(43, seed=UserSeed)

f = Fernet(key)
Cypher = f.encrypt(b"not encrypted")
print(Cypher)
Decoded=f.decrypt(Cypher)
print(Decoded)


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
        client.send(message)

def ClientHandle(client):
    while True:
        try:
            message1 = message2 = client.recv(1024)
            if message1.decode("utf-8").startswith("KICK"):
                if UserNamesList[ClientsList.index(client)] == 'admin':
                    ToBeKicked = message1.decode("utf-8")[5:]
                    
                    Kick_User(ToBeKicked)
                else:
                    client.send(f"Nie masz uprawnień!".encode("utf-8"))

            if message1.decode("utf-8").startswith("BAN"):
                if UserNamesList[ClientsList.index(client)] == 'admin':
                    ToBeBanned = message1.decode("utf-8")[4:]
                    Kick_User(ToBeBanned)
                    with open("BAN_LIST.txt", "a") as f:
                        f.write(f"{ToBeBanned}\n")
                    print(f"{ToBeBanned} został zbanowany!")
                else:
                    client.send(f"Nie masz uprawnień!".encode("utf-8"))
            else:
                ServerToClients(message2)
        except:
            if client in ClientsList:
                index = ClientsList.index(client)
                ClientsList.remove(client)
                client.close()
                
                UserName = UserNamesList[index]
                ExitMessage = f"{UserName} opuścił chat".encode('utf-8')
                ServerToClients(ExitMessage)

                UserNamesList.remove(UserName)
                break

def ReceiveMessages():
    while True:
        client, IP_Adress = server.accept()
        ConnectMessage = f"Połączono z {str(IP_Adress)}"

        
        print(ConnectMessage)
        
        client.send("FLAG_INIT".encode("utf-8"))
        UserName = client.recv(1024).decode("utf-8")
        
        with open("BAN_LIST.txt", "r") as f:
            bans = f.readlines()

        if UserName + "\n" in bans:
            client.send("FLAG_BAN".encode("utf-8"))
            client.close()
            continue

        if UserName == "admin":
            client.send("FLAG_ADMIN_PASSWORD".encode("utf-8"))
            print("Próba zalogowania na admina")
            AdminPassword = client.recv(1024).decode("utf-8")
            #tutaj zamienic haslo na hash hasła
            if AdminPassword != "123":
                client.send("FLAG_Wrong_Password".encode("utf-8"))
                client.close()
                continue
            


        UserNamesList.append(UserName)
        ClientsList.append(client)

        print(f"Nowy użytkownik: {UserName}")
        ServerToClients(f"{UserName} dołączył do chat'u".encode("utf-8"))

        client.send("Podłaczono do chat'u".encode("utf-8"))

        thread = threading.Thread(target=ClientHandle, args = (client,))
        thread.start()

def Kick_User(name):
    if name in UserNamesList:
        
        UserIndex = UserNamesList.index(name)
        kicked_client = ClientsList[UserIndex]
        ClientsList.remove(kicked_client)
        kicked_client.send(f"ZOSTAŁEŚ WYRZUCONY PRZEZ ADMINA!".encode("utf-8"))
        kicked_client.close()
        UserNamesList.remove(name)
        ServerToClients(f"{name} został wyrzucony przez Admina!".encode("utf-8"))
        

print("Serwer został uruchomiony...")
ReceiveMessages()