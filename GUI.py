import customtkinter as ctk
from Client import ChatClient
from PIL import Image
import time



class appGUI(ctk.CTk):
    def __init__(self, RootApp):
        super().__init__()
        self.app = RootApp
        self.app.configure(fg_color="#873600")
        self.FirstLaunch = True
        ctk.set_appearance_mode("dark")
        self.MainPage()
        
        



    def start_main_page(self):
        self.app.geometry("1200x700")


        ####
        
        my_tab = ctk.CTkTabview(self.app ,
	    width=1100,
	    height=650,
	    corner_radius=10,
	    text_color="white",
	    state="normal",
	    segmented_button_fg_color="black",
	    segmented_button_selected_color="#873600",
	    segmented_button_unselected_color="black",
	    segmented_button_selected_hover_color="silver",
	    segmented_button_unselected_hover_color="silver",
	    
	    	)
        my_tab.pack(pady=10)

        
        tab_1 = my_tab.add("PUBLIC CHAT")
        tab_2 = my_tab.add("PRIVATE")

        ctk.set_appearance_mode("dark")
        self.app.scrollable_frame = ctk.CTkScrollableFrame(master=tab_1, width=1000, height=400, bg_color="black" , fg_color="silver",)
        self.app.scrollable_frame.place(relx=0.03,rely=0.04)
        
        self.app.Msgs = ctk.CTkLabel(
            self.app.scrollable_frame,
            text=chat_client.GetPublicConv(),
            width=950,
            height=600,
            text_color="black",
            corner_radius=10,
            fg_color="#873600",
            compound="left",
            font=("Century Gothic", 30),
            justify="left",
            anchor="w"
            )
        self.app.Msgs.pack(pady=10)

        
        
        
        self.app.entry = ctk.CTkEntry(
            tab_1, width=700, height=100, placeholder_text="Wprowadź wiadomość..." ,font=("Century Gothic", 20),
        )
        self.app.entry.place(relx=0.1, rely=0.80)

        def Action():
            message = self.app.entry.get()
            chat_client.PublicMessage(message)
            #UPDATE MAINPAGE
            time.sleep(1)
            self.public_msgs()
        
        def Refr():
            
            #UPDATE MAINPAGE
            time.sleep(1)
            self.public_msgs()

        
        my_image = ctk.CTkImage(
            light_image=Image.open("refresh.png"),
            dark_image=Image.open("refresh.png"),
            size=(50, 50)
        )
        self.app.button1 = ctk.CTkButton(tab_1,width=60, fg_color="white", anchor="center", image=my_image, text="",hover_color="#873600" ,command=Refr).place(
            relx=0.02, rely=0.83
        )

        self.app.button = ctk.CTkButton(
            tab_1, width=150, height=100, text="WYŚLIJ", fg_color="black",hover_color="#873600",font=("Century Gothic", 20), command=Action
        )
        self.app.button.place(relx=0.8, rely=0.80)


        

        
        
    


    def public_msgs(self):
        self.app.Msgs.destroy()
        self.app.Msgs = ctk.CTkLabel(
            self.app.scrollable_frame,
            text=chat_client.GetPublicConv(),
            width=950,
            height=600,
            text_color="black",
            corner_radius=10,
            fg_color="#873600",
            compound="left",
            font=("Century Gothic", 30),
            justify="left",
            anchor="w"
            )
        self.app.Msgs.pack(pady=10)




    def MainPage(self):
        self.app.title("Whats'APE")
        self.app.geometry("50x50")
        if self.FirstLaunch:
            self.LoginPage()
            self.FirstLaunch = False
        
        


    

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
        new_window.title.place(relx=0.11, rely=0.20)

        new_window.entry = ctk.CTkEntry(
            new_window, width=344, height=60, placeholder_text="LOGIN"
        )
        new_window.entry.place(relx=0.11, rely=0.45)




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
        new_window.title.place(relx=0.25, rely=0.20)


        new_window.entry = ctk.CTkEntry(
            new_window, width=344, height=60, placeholder_text="HASŁO"
        )
        new_window.entry.place(relx=0.11, rely=0.45)

        def Next():
            if chat_client._FLAG_Recv == "REGISTER_SUCCESS":
                
                chat_client.User_Password_input = new_window.entry.get()
                chat_client.RegPassFlag = True

                new_window.destroy()
                new_window.update()

                #UPDATE MAINPAGE
                self.start_main_page()

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
                    self.start_main_page()
            


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