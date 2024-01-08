import socket
import threading

from VigenerCipher import VigenersCipher

klucz = "ONLYMESSAGE"
szyfr_vigenera = VigenersCipher(klucz)




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
            messageEncrypted = client.recv(1024).decode("utf-8")
            message = szyfr_vigenera.deszyfruj(messageEncrypted)
            if message == "FLAG_INIT":
                EncryptedUserNameInput = szyfr_vigenera.szyfruj(UserNameInput)
                client.send(f"{EncryptedUserNameInput}".encode("utf-8"))
                Admin_Password_FLAG_Recv_Encrypted = client.recv(1024).decode("utf-8")
                Admin_Password_FLAG_Recv = szyfr_vigenera.deszyfruj(Admin_Password_FLAG_Recv_Encrypted)
                if Admin_Password_FLAG_Recv == "FLAG_ADMIN_PASSWORD":
                    Encrypted_Admin_Password = szyfr_vigenera.szyfruj(Admin_Password)
                    client.send(f"{Encrypted_Admin_Password}".encode("utf-8"))
                    WrongPasswordEncrypted = client.recv(1024).decode("utf-8")
                    FlagWrongPassword = szyfr_vigenera.deszyfruj(WrongPasswordEncrypted)
                    if FlagWrongPassword == "FLAG_Wrong_Password":
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
                        messageKICK = f"KICK {message[(len(UserNameInput)+2+6):]}"
                        EncryptedmessageKICK = szyfr_vigenera.szyfruj(messageKICK)
                        client.send(EncryptedmessageKICK.encode("utf-8"))
                        
                    elif message[(len(UserNameInput)+2):].startswith('/ban'):
                        messageBAN = f"BAN {message[(len(UserNameInput)+2+5):]}"
                        EncryptedmessageBAN = szyfr_vigenera.szyfruj(messageBAN)
                        client.send(EncryptedmessageBAN.encode("utf-8"))
                else:
                    print("Nie masz uprawnień admina!")
            else:
                Encryptedmessage = szyfr_vigenera.szyfruj(message)
                client.send(f"{Encryptedmessage}".encode("utf-8"))

Client_Recv_Thread = threading.Thread(target=RecevieFromServer)
Client_Recv_Thread.start()

Client_Send_Thread = threading.Thread(target=ClientToServer)
Client_Send_Thread.start()