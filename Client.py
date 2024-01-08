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
            messageEncrypted = client.recv(1024)
            message = d_cipher.decrypt(messageEncrypted).decode("utf-8")
            if message == "FLAG_INIT":
                EncryptedUserNameInput = cipher.encrypt(bytes(UserNameInput,'UTF-8'))
                client.send(f"{EncryptedUserNameInput}".encode())
                Admin_Password_FLAG_Recv_Encrypted = client.recv(1024)
                Admin_Password_FLAG_Recv = d_cipher.decrypt(Admin_Password_FLAG_Recv_Encrypted).decode("utf-8")
                if Admin_Password_FLAG_Recv == "FLAG_ADMIN_PASSWORD":
                    Encrypted_Admin_Password = cipher.encrypt(bytes(Admin_Password,'UTF-8'))
                    client.send(f"{Encrypted_Admin_Password}".encode())
                    WrongPasswordEncrypted = client.recv(1024)
                    FlagWrongPassword = d_cipher.decrypt(WrongPasswordEncrypted).decode("utf-8")
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
                        EncryptedmessageKICK = cipher.encrypt(bytes(messageKICK,'UTF-8'))
                        client.send(f"{EncryptedmessageKICK}".encode())
                        
                    elif message[(len(UserNameInput)+2):].startswith('/ban'):
                        messageBAN = f"BAN {message[(len(UserNameInput)+2+5):]}"
                        EncryptedmessageBAN = cipher.encrypt(bytes(messageBAN,'UTF-8'))
                        client.send(f"{EncryptedmessageBAN}".encode())
                else:
                    print("Nie masz uprawnień admina!")
            else:
                Encryptedmessage = cipher.encrypt(bytes(message,'UTF-8'))
                client.send(f"{Encryptedmessage}".encode())

Client_Recv_Thread = threading.Thread(target=RecevieFromServer)
Client_Recv_Thread.start()

Client_Send_Thread = threading.Thread(target=ClientToServer)
Client_Send_Thread.start()