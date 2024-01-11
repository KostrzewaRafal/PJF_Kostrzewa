import socket
import threading
from VigenerCipher import VigenersCipher

class Server:
    def __init__(self, host, port, max_clients=20):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_clients)

        self.clients_list = []
        self.user_names_list = []
        self.vigeners_cipher = VigenersCipher("WHATSAPE")

    def send_to_clients(self, message):
        cipher_text = self.vigeners_cipher.szyfruj(message)
        for client in self.clients_list:
            client.send(cipher_text.encode("utf-8"))

    def client_handle(self, client):
        while True:
            try:
                message0 = client.recv(1024)
                message0 = message0.decode("utf-8")
                message1 = message2 = self.vigeners_cipher.deszyfruj(message0)

                if message1.startswith("KICK"):
                    if self.user_names_list[self.clients_list.index(client)] == "admin":
                        to_be_kicked = message1[5:]
                        self.kick_user(to_be_kicked)
                    else:
                        msg = "Nie masz uprawnień!"
                        cipher_msg = self.vigeners_cipher.szyfruj(msg)
                        client.send(cipher_msg.encode("utf-8"))

                if message1.startswith("BAN"):
                    if self.user_names_list[self.clients_list.index(client)] == "admin":
                        ToBeBanned = message1[4:]
                        to_be_kicked(ToBeBanned)
                        with open("BAN_LIST.txt", "a") as f:
                            f.write(f"{ToBeBanned}\n")
                        print(f"{ToBeBanned} został zbanowany!")
                    else:
                        msg = "Nie masz uprawnień!"
                        Cypher = self.vigeners_cipher.szyfruj(msg)
                        client.send(Cypher.encode("utf-8"))

                else:
                    self.send_to_clients(message2)

            except :
                if client in self.clients_list:
                    index = self.clients_list.index(client)
                    self.clients_list.remove(client)
                    client.close()

                    user_name = self.user_names_list[index]
                    exit_message = f"{user_name} opuścił chat"
                    self.send_to_clients(exit_message)

                    self.user_names_list.remove(user_name)
                    break

    def receive_messages(self):
        while True:
            client, ip_address = self.server_socket.accept()
            connect_message = f"Połączono z {str(ip_address)}"
            print(connect_message)

            flag_init = "FLAG_INIT"
            cipher_flag_init = self.vigeners_cipher.szyfruj(flag_init)
            client.send(cipher_flag_init.encode("utf-8"))

            user_name_encrypted = client.recv(1024).decode("utf-8")
            user_name = self.vigeners_cipher.deszyfruj(user_name_encrypted)

            
            
            with open("BAN_LIST.txt", "r") as f:
                bans = f.readlines()



            
            if user_name + "\n" in bans:
                FlagBAN = "FLAG_BAN"
                CypherFlagBAN = self.vigeners_cipher.szyfruj(FlagBAN)
                client.send(f"{CypherFlagBAN}".encode("utf-8"))

                client.close()
                continue


            if user_name == "admin":
                FlagAdminPass = "FLAG_ADMIN_PASSWORD"
                CypherFlagAdmPass = self.vigeners_cipher.szyfruj(FlagAdminPass)
                client.send(f"{CypherFlagAdmPass}".encode("utf-8"))
                print("Próba zalogowania na admina")

                AdminPasswordEncrypt = client.recv(1024).decode("utf-8")
                AdminPassword = self.vigeners_cipher.deszyfruj(AdminPasswordEncrypt)
                # tutaj zamienic haslo na hash hasła
                if str(AdminPassword) != "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3":
                    FlagWrng = "FLAG_Wrong_Password"
                    CypherFlagWrng = self.vigeners_cipher.szyfruj(FlagWrng)
                    client.send(f"{CypherFlagWrng}".encode("utf-8"))
                    client.close()
                    continue
                    

            self.user_names_list.append(user_name)
            self.clients_list.append(client)

            print(f"Nowy użytkownik: {user_name}")
            welcome_msg = f"{user_name} dołączył do chat'u"
            self.send_to_clients(welcome_msg)

            welcome = "Podłaczono do chat'u"
            cipher_welcome = self.vigeners_cipher.szyfruj(welcome)
            client.send(cipher_welcome.encode("utf-8"))

            thread = threading.Thread(target=self.client_handle, args=(client,))
            thread.start()

    def kick_user(self, name):
        if name in self.user_names_list:
            user_index = self.user_names_list.index(name)
            kicked_client = self.clients_list[user_index]
            self.clients_list.remove(kicked_client)

            kick_msg = "ZOSTAŁEŚ WYRZUCONY PRZEZ ADMINA!"
            cipher_kick_msg = self.vigeners_cipher.szyfruj(kick_msg)
            kicked_client.send(cipher_kick_msg.encode("utf-8"))

            kicked_client.close()
            self.user_names_list.remove(name)

            kick_msg_all = f"{name} został wyrzucony przez Admina!"
            self.send_to_clients(kick_msg_all)

if __name__ == "__main__":
    server_instance = Server(socket.gethostbyname(socket.gethostname()), 12345)
    print("Server has been started...")
    server_instance.receive_messages()