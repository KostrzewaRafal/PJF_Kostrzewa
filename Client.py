import socket
import threading
import hashlib

from VigenerCipher import VigenersCipher

class ClassClient:
    def __init__(self, host, port,UserNam):
        self.UserNameInput=UserNam
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.szyfr_vigenera = VigenersCipher("WHATSAPE")

        self.stop_thread = False

    def receive_from_server(self):
        while True:
            
            if self.stop_thread:
                break

            try:
                messageEncrypted = self.client.recv(1024).decode("utf-8")
                message = self.szyfr_vigenera.deszyfruj(messageEncrypted)
                if message == "FLAG_INIT":
                    UserName=self.UserNameInput
                    UserName = self.szyfr_vigenera.szyfruj(UserName)

                    self.client.send(f"{UserName}".encode("utf-8"))
                    Admin_Password_FLAG_Recv_Encrypted = self.client.recv(1024).decode("utf-8")
                    Admin_Password_FLAG_Recv = self.szyfr_vigenera.deszyfruj(
                        Admin_Password_FLAG_Recv_Encrypted
                    )
                    if Admin_Password_FLAG_Recv == "FLAG_ADMIN_PASSWORD":
                        Encrypted_Admin_Password = self.szyfr_vigenera.szyfruj(Admin_Password)
                        self.client.send(f"{Encrypted_Admin_Password}".encode("utf-8"))
                        WrongPasswordEncrypted = self.client.recv(1024).decode("utf-8")
                        FlagWrongPassword = self.szyfr_vigenera.deszyfruj(WrongPasswordEncrypted)
                        if FlagWrongPassword == "FLAG_Wrong_Password":
                            print("Wprowadzono złe hasło dla admina!")
                            self.stop_thread = True
                    elif Admin_Password_FLAG_Recv == "FLAG_BAN":
                        print("TEN UŻYTKOWNIK JEST ZBANOWANY!")
                        self.client.close()
                        self.stop_thread = True

                else:
                    print(message)
            except:
                print("BŁĄD")
                self.client.close()
                break

    def client_to_server(self):
        while True:
                if self.stop_thread:
                    break
                
                message = f'{self.UserNameInput}: {input("")}'

                if len(message) != (len(self.UserNameInput) + 2):
                    if message[len(self.UserNameInput) + 2].startswith("/"):
                        if self.UserNameInput == "admin":
                            if message[(len(self.UserNameInput) + 2) :].startswith("/kick"):
                                messageKICK = f"KICK {message[(len(self.UserNameInput)+2+6):]}"
                                EncryptedmessageKICK = self.szyfr_vigenera.szyfruj(messageKICK)
                                self.client.send(EncryptedmessageKICK.encode("utf-8"))

                            elif message[(len(self.UserNameInput) + 2) :].startswith("/ban"):
                                messageBAN = f"BAN {message[(len(self.UserNameInput)+2+5):]}"
                                EncryptedmessageBAN = self.szyfr_vigenera.szyfruj(messageBAN)
                                self.client.send(EncryptedmessageBAN.encode("utf-8"))
                        else:
                            print("Nie masz uprawnień admina!")
                    else:
                        Encryptedmessage = self.szyfr_vigenera.szyfruj(message)
                        self.client.send(f"{Encryptedmessage}".encode("utf-8"))

    def start_threads(self):
        recv_thread = threading.Thread(target=self.receive_from_server)
        recv_thread.start()
        send_thread = threading.Thread(target=self.client_to_server)
        send_thread.start()

if __name__ == "__main__":
    
    user_name_input = input("Podaj nazwe dla użytkownika:")
    if user_name_input == "admin":
        Admin_Password = input("Podaj hasło dla admina:")#123
        HASH1= hashlib.sha256()
        HASH1.update(Admin_Password.encode())
        Admin_Password = HASH1.hexdigest()
        print(Admin_Password)
    client = ClassClient(socket.gethostbyname(socket.gethostname()), 12345,user_name_input )
    client.start_threads()

  

