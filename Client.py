import socket
import threading
import hashlib
from VigenerCipher import VigenersCipher
import customtkinter as ctk
import time

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
        self.SENDmessage =""
        self.OpenGate = False
        self.LogRejFlag = False
        self.LogType = ""
        self.LoginFlag = False
        self.RegPassFlag = False
        self.LogPassFlag = False
        self.User_Password_input = ""
        self.FlagWrongPassword =""

    def receive_from_server(self):
        while True:
            if self.stop_thread:
                break

            try:

                messageEncrypted = self.client.recv(4096).decode("utf-8")
                message = self.szyfr_vigenera.deszyfruj(messageEncrypted)
                if message == "FLAG_INIT":
                    while not self.LogRejFlag:
                        time.sleep(0.1)
                        continue

                    
                    self.client.send(f"{self.LogType}".encode("utf-8"))

                    while self.SuccesfullLoginAttempt != True:
                        
                        while not self.LoginFlag:
                            time.sleep(0.1)
                            continue

                        self.LoginFlag = False


                        UserName = self.UserNameInput
                        UserName = self.szyfr_vigenera.szyfruj(UserName)
                        self.client.send(f"{UserName}".encode("utf-8"))

                        _FLAG_Recv_Encrypted = self.client.recv(4096).decode("utf-8")
                        self._FLAG_Recv = self.szyfr_vigenera.deszyfruj(_FLAG_Recv_Encrypted)

                        CorrectPassword = False



                        if self._FLAG_Recv == "FLAG_BAN":
                            print("TEN UŻYTKOWNIK JEST ZBANOWANY!")
                            time.sleep(5)
                            self.client.close()
                            self.stop_thread = True
                        elif self._FLAG_Recv == "USERNAME_TAKEN":
                            print("TA NAZWA JEST ZAJETA!")
                            continue
                        elif self._FLAG_Recv == "REGISTER_SUCCESS":
                            while not self.RegPassFlag:
                                time.sleep(0.1)
                                continue

                            self.SuccesfullLoginAttempt = True
                            
                            HASH1 = hashlib.sha256()
                            HASH1.update(self.User_Password_input.encode())
                            self.User_Password = HASH1.hexdigest()

                            Encrypted_Password = self.szyfr_vigenera.szyfruj(
                                self.User_Password
                            )
                            self.client.send(f"{Encrypted_Password}".encode("utf-8"))

                        elif self._FLAG_Recv == "No_User":
                            print("NIE MA TAKIEGO KONTA! WYBIERZ REJESTRACJĘ!")
                            self.client.close()
                            self.stop_thread = True
                            break

                        elif self._FLAG_Recv == "LOGIN_SUCCESS":
                            self.SuccesfullLoginAttempt = True

                            while CorrectPassword != True:
                                while not self.LogPassFlag:
                                    time.sleep(0.1)
                                    continue

                                self.LogPassFlag = False


                                HASH2 = hashlib.sha256()
                                HASH2.update(self.User_Password_input.encode())
                                self.User_Password = HASH2.hexdigest()

                                Encrypted_Password = self.szyfr_vigenera.szyfruj(
                                    self.User_Password
                                )
                                self.client.send(
                                    f"{Encrypted_Password}".encode("utf-8")
                                )

                                WrongPasswordEncrypted = self.client.recv(4096).decode(
                                    "utf-8"
                                )
                                self.FlagWrongPassword = self.szyfr_vigenera.deszyfruj(
                                    WrongPasswordEncrypted
                                )
                                if self.FlagWrongPassword == "FLAG_Wrong_Password":
                                    print("Wprowadzono złe hasło!")

                                elif self.FlagWrongPassword == "FLAG_Good_Password":
                                    CorrectPassword = True
                                    continue

                    send_thread = threading.Thread(target=self.client_to_server)
                    send_thread.start()

                elif message.startswith("1"):
                    with open(f"PublicChats\{self.UserNameInput}.txt", "a") as f:
                            f.write(f"{message[2:]}\n")
                    self.PUBLICCHAT = f"PublicChats\{self.UserNameInput}.txt"
                    print(message[2:])
                    #wywołaj jakos okienko jesli zamkniete

                elif message.startswith("2"):
                    MsgParts = message.split("|")
                    self.Me = MsgParts[1]
                    SecondPerson = MsgParts[2]
                    MsgContent = MsgParts[3]
                    with open(f"PVChats\{self.Me}{SecondPerson}.txt", "a") as f:
                            f.write(f"{MsgContent}\n")
                    self.PVCHAT = f"PVChats\{self.Me}{SecondPerson}.txt"
                    print(message[2:])
                    #wywołaj jakos okienko jesli zamkniete
                    



            except:
                print("BŁĄD")
                self.client.close()
                break







    def client_to_server(self):
        while True:
            if self.stop_thread:
                break

            #while self.OpenGate
            self.SENDmessage = f'{self.UserNameInput}: {input("")}'
            self.OpenGate = False
            if len(self.SENDmessage) != (len(self.UserNameInput) + 2):
                if self.SENDmessage[len(self.UserNameInput) + 2].startswith("/"):
                    if self.UserNameInput == "admin":
                        if self.SENDmessage[(len(self.UserNameInput) + 2) :].startswith("/kick"):
                            messageKICK = (
                                f"KICK {self.SENDmessage[(len(self.UserNameInput)+2+6):]}"
                            )
                            EncryptedmessageKICK = self.szyfr_vigenera.szyfruj(
                                messageKICK
                            )
                            self.client.send(EncryptedmessageKICK.encode("utf-8"))

                        elif self.SENDmessage[(len(self.UserNameInput) + 2) :].startswith(
                            "/ban"
                        ):
                            messageBAN = (
                                f"BAN {self.SENDmessage[(len(self.UserNameInput)+2+5):]}"
                            )
                            EncryptedmessageBAN = self.szyfr_vigenera.szyfruj(
                                messageBAN
                            )
                            self.client.send(EncryptedmessageBAN.encode("utf-8"))
                    else:
                        print("Nie masz uprawnień admina!")
                else:
                    Encryptedmessage = self.szyfr_vigenera.szyfruj(self.SENDmessage)
                    self.client.send(f"{Encryptedmessage}".encode("utf-8"))

    def start_threads(self):
        recv_thread = threading.Thread(target=self.receive_from_server)
        recv_thread.start()


    def PublicMessage(self, message):
        self.SENDmessage =f"1|{self.UserNameInput}: {message}" 
        self.OpenGate = True

    def PrivateMessage(self, message, DestinationClient):
        self.SENDmessage =f"2|{DestinationClient}|{self.UserNameInput}|{self.UserNameInput}: {message}" 
        self.OpenGate = True
    
    def GetPublicConv(self):
        with open(self.PUBLICCHAT, "r") as f:
            Conv = f.read()
        return Conv
        
    def GetPVConv(self, SecondPerson):
        with open(f"PVChats\{self.Me}{SecondPerson}.txt", "r") as f:
            Conv = f.read()
        return Conv

    

