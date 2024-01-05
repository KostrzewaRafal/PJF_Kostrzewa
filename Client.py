import socket
import threading


host_IP = socket.gethostbyname(socket.gethostname()) #Pobranie ip hosta 
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host_IP, port))

UserNameInput = input("Podaj nazwę użytkownika:")
if UserNameInput == "admin":
    Admin_Password = input("Podaj hasło dla admina:")

stop_thread = False

def RecevieFromServer():
    while True:
        global stop_thread
        if stop_thread == True:
            break

        try:
            message = client.recv(1024).decode('utf-8')
            if message == "FLAG_INIT":
                client.send(UserNameInput.encode('utf-8'))
                Admin_Password_FLAG_Recv = client.recv(1024).decode('utf-8')
                if Admin_Password_FLAG_Recv == "FLAG_ADMIN_PASSWORD":
                    client.send(Admin_Password.encode("utf-8"))
                    if client.recv(1024).decode("utf-8") == "FLAG_Wrong_Password":
                        print("Wprowadzono złe hasło dla admina!")
                        stop_thread = True
                elif Admin_Password_FLAG_Recv == "FLAG_BAN":
                    print("TEN UŻYTKOWNIK JEST ZBANOWANY!")
                    client.close()
                    stop_thread = True

            else:
                print(message)
        except:
            print("BŁĄD")
            client.close()
            break

def ClientToServer():
    while True:
        if stop_thread == True:
            break
        
        message = f'{UserNameInput}: {input("")}'
        
        if len(message) != (len(UserNameInput)+2):
            if message[len(UserNameInput)+2].startswith('/'):
                if UserNameInput == "admin":
                    if message[(len(UserNameInput)+2):].startswith('/kick'):
                        client.send(f"KICK {message[(len(UserNameInput)+2+6):]}".encode("utf-8"))
                        
                    elif message[(len(UserNameInput)+2):].startswith('/ban'):
                        client.send(f"BAN {message[(len(UserNameInput)+2+5):]}".encode("utf-8"))
                else:
                    print("Nie masz uprawnień admina!")
            else:
                client.send(message.encode('utf-8'))

Client_Recv_Thread = threading.Thread(target=RecevieFromServer)
Client_Recv_Thread.start()

Client_Send_Thread = threading.Thread(target=ClientToServer)
Client_Send_Thread.start()