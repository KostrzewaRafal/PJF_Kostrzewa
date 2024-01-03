import socket
import threading


host_IP = socket.gethostbyname(socket.gethostname()) #Pobranie ip hosta 
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host_IP, port))

UserNameInput = input("Podaj nazwę użytkownika:")

def RecevieFromServer():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "FLAG_INIT":
                client.send(UserNameInput.encode('utf-8'))
            else:
                print(message)
        except:
            print("BŁĄD")
            client.close()
            break

def ClientToServer():
    while True:
        message = f'{UserNameInput}: {input("")}'
        client.send(message.encode('utf-8'))

Client_Recv_Thread = threading.Thread(target=RecevieFromServer)
Client_Recv_Thread.start()

Client_Send_Thread = threading.Thread(target=ClientToServer)
Client_Send_Thread.start()