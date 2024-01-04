import socket
import threading



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
            message = client.recv(1024)
            ServerToClients(message)
        except:
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
        UserNamesList.append(UserName)
        ClientsList.append(client)

        print(f"Nowy użytkownik: {UserName}")
        ServerToClients(f"{UserName} dołączył do chat'u".encode("utf-8"))

        client.send("Podłaczono do chat'u".encode("utf-8"))

        thread = threading.Thread(target=ClientHandle, args = (client,))
        thread.start()


ReceiveMessages()