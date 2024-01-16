import customtkinter as ctk
from Client import ChatClient
from PIL import Image
import time


class appGUI(ctk.CTk):
    def __init__(self, RootApp):
        super().__init__()
        self.app = RootApp
        self.app.configure(fg_color="#873600")
        ctk.set_appearance_mode("dark")
        self.MainPage()


    def MainPage(self):
        self.app.title("Whats'APE")
        self.app.geometry("1000x800")
        self.LoginPage()

        '''
        self.app.title = ctk.CTkLabel(
            self.app,
            text="What'sAPE",
            width=200,
            height=70,
            text_color="white",
            fg_color="#873600",
            compound="center",
            font=("Century Gothic", 40),
        )
        self.app.title.place(relx=0.26, rely=0.1)

        
        my_image = ctk.CTkImage(
            light_image=Image.open("Maupka.png"),
            dark_image=None,
            size=(200, 200),
        )

        self.app.title = ctk.CTkLabel(self.app, image=my_image, text="", anchor="center").place(
            relx=0.25, rely=0.28
        )




        self.app.button = ctk.CTkButton(
            self.app, width=150, height=50, text="ZALOGUJ SIĘ", fg_color="black"
        )
        self.app.button.place(relx=0.1, rely=0.75)

        self.app.button = ctk.CTkButton(
            self.app, width=150, height=50, text="ZAREJESTRUJ SIĘ", fg_color="black",
        )
        self.app.button.place(relx=0.56, rely=0.75)'''



    

    def LoginPage(self):
        new_window = ctk.CTkToplevel(self.app)
        new_window.configure(fg_color="#873600")
        new_window.title("WITAMY w Whats'APE")
        new_window.geometry("450x440")
        new_window.grab_set()
        
        new_window.label = ctk.CTkLabel(
            new_window,
            text="What'sAPE",
            width=200,
            height=70,
            text_color="white",
            fg_color="#873600",
            compound="center",
            font=("Century Gothic", 40),
        )
        new_window.label.place(relx=0.26, rely=0.1)

        def Log():
            new_window.destroy()
            new_window.update()
            chat_client.LogType = "2"
            chat_client.LogRejFlag = True
            self.Login()

        def Rej():
            new_window.destroy()
            new_window.update()
            chat_client.LogType = "1"
            chat_client.LogRejFlag = True
            self.Login()

        
        my_image = ctk.CTkImage(
            light_image=Image.open("Maupka.png"),
            dark_image=None,
            size=(200, 200),
        )
        new_window.title = ctk.CTkLabel(new_window, image=my_image, text="", anchor="center").place(
            relx=0.25, rely=0.28
        )

        new_window.button = ctk.CTkButton(
            new_window, width=150, height=50, text="ZALOGUJ SIĘ", fg_color="black", command=Log
        )
        new_window.button.place(relx=0.1, rely=0.75)
        new_window.button = ctk.CTkButton(
            new_window, width=150, height=50, text="ZAREJESTRUJ SIĘ", fg_color="black",command=Rej
        )
        new_window.button.place(relx=0.56, rely=0.75)



        


    def Login(self):
        new_window = ctk.CTkToplevel(self.app)
        new_window.configure(fg_color="#873600")
        new_window.title("Login")
        new_window.geometry("450x440")
        new_window.grab_set()
        
        new_window.title = ctk.CTkLabel(
            new_window,
            text="Wpisz nazwę użytkownika:",
            width=200,
            height=70,
            text_color="white",
            fg_color="#873600",
            compound="center",
            font=("Simple Bold Jut Out", 30),
        )
        new_window.title.place(relx=0.18, rely=0.1)

        new_window.entry = ctk.CTkEntry(
            new_window, width=344, height=60, placeholder_text="LOGIN"
        )
        new_window.entry.place(relx=0.11, rely=0.30)




        def Next():
            
            chat_client.UserNameInput = new_window.entry.get()
            chat_client.LoginFlag = True
            time.sleep(1)
            if chat_client._FLAG_Recv == "FLAG_BAN":
                new_window.title.configure(text="TEN UŻYTKOWNIK JEST ZBANOWANY! \n Nastąpi zamknięcie aplikacji!")
                time.sleep(5)
                new_window.destroy()
                new_window.update()
                self.app.destroy()
                self.app.update()
                

            elif chat_client._FLAG_Recv == "USERNAME_TAKEN":
                new_window.title.configure(text="TA NAZWA JEST ZAJETA!")
                
            elif chat_client._FLAG_Recv == "No_User":
                new_window.title.configure(text="NIE MA TAKIEGO KONTA! WYBIERZ REJESTRACJĘ!")
                time.sleep(5)
                new_window.destroy()
                new_window.update()
                self.app.destroy()
                self.app.update()

            elif chat_client._FLAG_Recv == "REGISTER_SUCCESS":
                new_window.destroy()
                new_window.update()
                self.Password()

            elif chat_client._FLAG_Recv == "LOGIN_SUCCESS":
                new_window.destroy()
                new_window.update()
                self.Password()
            
                



        new_window.button = ctk.CTkButton(
            new_window, width=150, height=50, text="Dalej", fg_color="black", command=Next
        )
        new_window.button.place(relx=0.34, rely=0.75)
        
        
        



    def Password(self):
        new_window = ctk.CTkToplevel(self.app)
        new_window.configure(fg_color="#873600")
        new_window.title("Login")
        new_window.geometry("450x440")
        new_window.grab_set()
        
        new_window.title = ctk.CTkLabel(
            new_window,
            text="Wpisz hasło:",
            width=200,
            height=70,
            text_color="white",
            fg_color="#873600",
            compound="center",
            font=("Simple Bold Jut Out", 30),
        )
        new_window.title.place(relx=0.18, rely=0.1)


        new_window.entry = ctk.CTkEntry(
            new_window, width=344, height=60, placeholder_text="HASŁO"
        )
        new_window.entry.place(relx=0.11, rely=0.30)

        def Next():
            if chat_client._FLAG_Recv == "REGISTER_SUCCESS":
                
                chat_client.User_Password_input = new_window.entry.get()
                chat_client.RegPassFlag = True

                new_window.destroy()
                new_window.update()

                #UPDATE MAINPAGE
                self.app.title = ctk.CTkLabel(
                self.app,
                text="What'sAPE",
                width=200,
                height=70,
                text_color="white",
                fg_color="#873600",
                compound="center",
                font=("Century Gothic", 40),
                )
                self.app.title.place(relx=0.26, rely=0.1)

            elif chat_client._FLAG_Recv == "LOGIN_SUCCESS":
                chat_client.User_Password_input = new_window.entry.get()
                chat_client.LogPassFlag = True
                time.sleep(2)

                if chat_client.FlagWrongPassword =="FLAG_Wrong_Password":
                    new_window.title.configure(text="TA NAZWA JEST ZAJETA!\nWprowadź inną!")

                elif chat_client.FlagWrongPassword =="FLAG_Good_Password":
                    new_window.destroy()
                    new_window.update()

                    #UPDATE MAINPAGE
                    self.app.title = ctk.CTkLabel(
                    self.app,
                    text="What'sAPE",
                    width=200,
                    height=70,
                    text_color="white",
                    fg_color="#873600",
                    compound="center",
                    font=("Century Gothic", 40),
                    )
                    self.app.title.place(relx=0.26, rely=0.1)
            


        new_window.button = ctk.CTkButton(
            new_window, width=150, height=50, text="Dalej", fg_color="black", command=Next
        )
        new_window.button.place(relx=0.34, rely=0.75)
        
        
        


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.start_threads()
    
    app = ctk.CTk()
    appGUI(app)
    app.mainloop()