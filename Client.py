import socket
import threading
import hashlib
from VigenerCipher import VigenersCipher

class ChatClient:
    def __init__(self):
        self.host_IP = socket.gethostbyname(socket.gethostname())
        self.port = 12345
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host_IP, self.port))
        self.klucz = "WHATSAPE"
        self.szyfr_vigenera = VigenersCipher(self.klucz)
        self.UserNameInput = ""
        self.User_Password = ""
        self.SuccesfullLoginAttempt = False
        self.stop_thread = False

    
    def receive_from_server(self):
        while True:
            if self.stop_thread:
                break

            try:
                messageEncrypted = self.client.recv(1024).decode("utf-8")
                message = self.szyfr_vigenera.deszyfruj(messageEncrypted)
                if message == "FLAG_INIT":
                    LogType = input("Chcesz sie Zarejestrować(1) czy Zalogować(2):")
                    self.client.send(f"{LogType}".encode("utf-8"))


                    while self.SuccesfullLoginAttempt != True:
                        self.UserNameInput = input("Podaj nazwę użytkownika:")
                        UserName=self.UserNameInput
                        UserName = self.szyfr_vigenera.szyfruj(UserName)
                        self.client.send(f"{UserName}".encode("utf-8"))
                        
                        _FLAG_Recv_Encrypted = self.client.recv(1024).decode("utf-8")
                        _FLAG_Recv = self.szyfr_vigenera.deszyfruj(_FLAG_Recv_Encrypted)
                        
                        CorrectPassword = False

                        if _FLAG_Recv == "FLAG_BAN":
                            print("TEN UŻYTKOWNIK JEST ZBANOWANY!")
                            self.client.close()
                            self.stop_thread = True
                        elif _FLAG_Recv == "USERNAME_TAKEN":
                            print("TA NAZWA JEST ZAJETA!")
                            continue
                        elif _FLAG_Recv == "REGISTER_SUCCESS":
                            self.SuccesfullLoginAttempt = True
                            User_Password_input = input(f"Podaj hasło dla '{self.UserNameInput}':")
                            HASH1 = hashlib.sha256()
                            HASH1.update(User_Password_input.encode())
                            self.User_Password = HASH1.hexdigest()
                            
                            Encrypted_Password = self.szyfr_vigenera.szyfruj(self.User_Password)
                            self.client.send(f"{Encrypted_Password}".encode("utf-8"))

                        elif _FLAG_Recv == "No_User":
                            print("NIE MA TAKIEGO KONTA! WYBIERZ REJESTRACJĘ!")
                            self.client.close()
                            self.stop_thread = True
                            break
                            
                        elif _FLAG_Recv == "LOGIN_SUCCESS":
                            self.SuccesfullLoginAttempt = True


                            while CorrectPassword != True:
                                User_Password_input = input(f"Podaj hasło dla '{self.UserNameInput}':")
                                HASH2 = hashlib.sha256()
                                HASH2.update(User_Password_input.encode())
                                self.User_Password = HASH2.hexdigest()

                                Encrypted_Password = self.szyfr_vigenera.szyfruj(self.User_Password)
                                self.client.send(f"{Encrypted_Password}".encode("utf-8"))

                                WrongPasswordEncrypted = self.client.recv(1024).decode("utf-8")
                                FlagWrongPassword = self.szyfr_vigenera.deszyfruj(WrongPasswordEncrypted)
                                if FlagWrongPassword == "FLAG_Wrong_Password":
                                    print("Wprowadzono złe hasło!")
                                    
                                elif FlagWrongPassword == "FLAG_Good_Password":
                                    CorrectPassword = True
                                    continue
                    send_thread = threading.Thread(target=self.client_to_server)
                    send_thread.start()

            
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



if __name__ == "__main__":
    
  
    chat_client = ChatClient()
    chat_client.start_threads()