from sqlite3.dbapi2 import OperationalError
from tkinter import *

#When there are no databases, create a new one
from post_register_db import create_databases
try:
    create_databases()
except OperationalError:
    pass

#Internal functions
from master_password import encrypt_password, verify_master_password, add_master_password
from dbFunctions import add_password, check_existing_entry, delete_entry, get_password, edit_password, get_all_passwords
from password_generator import password_generator
from dbMemory import get_site, send_to_temp
from first_time import first_time_check, change_first_time_to_false
from master_password_hash_generator import master_password_hash_generator

class PasswordManager(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        if first_time_check():
            self.switch_frame(Register)
        else:
            self.switch_frame(Login)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
class Login(Frame):
    def __init__(self, master):

        def checkPassword(master_password):
        
            verification = verify_master_password(master_password)

            if verification:
                master.switch_frame(Menu)
            else:
                Label(self, text="Wrong password, try again").pack()

        Frame.__init__(self, master)
        Label(self, text="Please enter your username and master password").pack(side="top", fill="x", pady=10, padx=5)
        
        username_entry = Entry(self)
        username_entry.pack(pady=10)
        
        master_password_entry = Entry(self, show="*")
        master_password_entry.pack(pady=10)

        Button(self, text="Access", command=lambda:
                        checkPassword(master_password_entry.get())).pack(side="top", pady=10, padx=5)


class Register(Frame):
    def __init__(self, master):

        def checkPassword(master_password, master_password2, username):
            if master_password == master_password2:
                encrypted_master_password = master_password_hash_generator(master_password)
                add_master_password(encrypted_master_password, username)
                change_first_time_to_false()
                master.switch_frame(Login)
            else:
                Label(self, text="The passwords do not match").pack()

        Frame.__init__(self, master)
        Label(self, text="Welcome to Pedranji's Password Manager").pack(side="top", fill="x", pady=10)
        Label(self, text="Please enter a username of your choice").pack()

        username_entry = Entry(self)
        username_entry.pack(pady=5)

        Label(self, text="Enter a master password").pack()
        master_password_entry = Entry(self, show="*")
        master_password_entry.pack(pady=5)

        Label(self, text="Re-enter the password").pack()
        master_password_entry2 = Entry(self, show="*")
        master_password_entry2.pack(pady=5)



        Button(self, text="Access", 
            command=lambda:checkPassword(master_password_entry.get(), master_password_entry2.get(), username_entry.get())).pack()

class Menu(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is the menu").pack(side="top", fill="x", pady=10, padx=7)
        Button(self, text="Access passwords",
                  command=lambda: master.switch_frame(AccessPasswords)).pack(side="top", fill="x", pady=10, padx=20)
        Button(self, text="Show all passwords", 
            command=lambda: master.switch_frame(ShowAllPasswords)).pack(side="top", fill="x", pady=10, padx=20)
        Button(self, text="Add a safe password", 
                  command=lambda: master.switch_frame(GeneratePassword)).pack(side="top", fill="x", pady=10, padx=20)        
        Button(self, text="Add an existing password", 
                  command=lambda: master.switch_frame(AddExistingPassword)).pack(side="top", fill="x", pady=10, padx=20)
        Button(self, text="Update a password", 
                  command=lambda: master.switch_frame(UpdatePassword)).pack(side="top", fill="x", pady=10, padx=20)
        Button(self, text="Update an username", 
                  command=lambda: master.switch_frame(UpdateUsername)).pack(side="top", fill="x", pady=10, padx=20)
        Button(self, text="Delete a password", 
                  command=lambda: master.switch_frame(DeletePassword)).pack(side="top", fill="x", pady=10, padx=20)

class AccessPasswords(Frame):
    def __init__(self, master):

        def send_data(website, username):
            send_to_temp(website, username)
            master.switch_frame(ShowPassword)
            
        Frame.__init__(self, master)
        Label(self, text="Access saved passwords").pack(side="top", fill="x", pady=10, padx=5)
        Label(self, text="Enter the website").pack(side="top", fill="x", pady=10, padx=5)
        website_entry = Entry(self)
        website_entry.pack(side="top", pady=5, padx=5)
        Label(self, text="Enter the username of the account").pack(side="top", fill="x", pady=10, padx=10)
        username_entry = Entry(self)
        username_entry.pack(side="top", pady=5, padx=5)
        Button(self, text="Submit", command=lambda: send_data(website_entry.get(), username_entry.get())).pack(side="top", pady=10, padx=5)

        Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)

class AddExistingPassword(Frame):
    def __init__(self, master):
        def add(password, website, username):
            try:
                add_password(encrypt_password(password), website, username)
                Label(self, text="Your password has been succesfully encrypted and added to the database").pack(fill="x", pady=10)
            except TypeError:
                Label(self, text="Sorry, a type error has ocurred").pack()
                Button(self, text="Return to start page",
                                    command=lambda: master.switch_frame(Menu)).pack()                

        Frame.__init__(self, master)
        Label(self, text="Add an existing password to the database").pack(side="top", fill="x", pady=10, padx=5)
        Label(self, text="Enter the website:").pack(side="top", fill="x", pady=5, padx=5)
        website = Entry(self)
        website.pack(side="top", pady=5, padx=5)
        Label(self,text="Enter the username:").pack(side="top", fill="x", pady=5, padx=5)
        username = Entry(self)
        username.pack(side="top", pady=5, padx=5)
        Label(self, text="Enter the password").pack(side="top", fill="x", pady=5, padx=5)
        password = Entry(self)
        password.pack(side="top", pady=5, padx=5)

        Button(self, text="Submit", 
                command=lambda:add(password.get(), website.get(), username.get())).pack(side="top", pady=5, padx=5)

        Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)

class GeneratePassword(Frame):
    def __init__(self, master):
        def gen_password(website, username):
            if check_existing_entry(website, username) is False:
                #Changes immediately to show the generated password
                password = password_generator(20)
                add_password(password, website, username)
                send_to_temp(website, username)
                master.switch_frame(ShowPassword)
            else:
                #Shows a screen and gives the option to show the existing password
                def send_and_change():
                    send_to_temp(website, username)
                    master.switch_frame(ShowPassword)
                for widget in Frame.winfo_children(self):
                    widget.destroy() 
                Label(self, text="You already have a password in that website with the same username").pack(side="top", fill="x", pady=10, padx=5) 
                Button(self, text="Access the password", 
                    command=send_and_change).pack(side="top", pady=10, padx=5)          
                Button(self, text="Return to start page",
                    command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)

        Frame.__init__(self, master)
        Label(self, text="Generate a new password").pack(side="top", fill="x", pady=10, padx=5)
        Label(self, text="Enter the website:").pack(side="top", fill="x", pady=10, padx=5)
        website = Entry(self)
        website.pack(side="top", pady=5, padx=5)
        Label(self, text="Enter your username:").pack(side="top", fill="x", pady=10, padx=5)
        username = Entry(self)
        username.pack(side="top", pady=5, padx=5)
        Button(self, text="Generate", command=lambda: gen_password(website.get(), username.get())).pack(side="top", pady=10, padx=10)
        Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)

class ShowPassword(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.config(width=200)
        try:
            #Retrieves data from temp
            temp_website, temp_username = get_site()
            #Retrieves data from actual database with the data retrieved from temp
            password, website, username = get_password(temp_website, temp_username)
            Label(self, text=f"This is the data from your password").pack(side="top", fill="x", pady=10)

            #This large website_text code is due to the fact that it is copyable this way
            Label(self,text="Website:").pack()
            website_text = Text(self, height=1, borderwidth=0, width=30)
            website_text.insert(1.0, website)
            website_text.pack()
            website_text.configure(state="disabled")

            Label(self,text="Username:").pack()
            username_text = Text(self, height=1, borderwidth=0, width=30)
            username_text.insert(1.0, username)
            username_text.pack()
            username_text.configure(state="disabled")    
            
            Label(self,text="Password:").pack()
            password_text = Text(self, height=1, borderwidth=0, width=30)
            password_text.insert(1.0, password)
            password_text.pack()
            password_text.configure(state="disabled")
            
            Button(self, text="Return to start page",
                    command=lambda: master.switch_frame(Menu)).pack(pady=10)
        except TypeError:
            Label(self, text="That website and username are not registered in our database").pack(side="top", fill="x", pady=10, padx=5)
            Button(self, text="Return to start page",
                                command=lambda: master.switch_frame(Menu)).pack(side="top", fill="x", pady=10, padx=5)


class ShowAllPasswords(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        all_passwords = get_all_passwords()
        if all_passwords == []:
            Label(self, text="You have not registered any passwords in the database yet").pack(side="top", fill="x", pady=10, padx=5)
            Button(self, text="Return to start page",
                                command=lambda: master.switch_frame(Menu)).pack(side="top", fill="x", pady=10, padx=5)

        for entry in all_passwords:
            password, website, username = entry[0], entry[1], entry[2]

            Label(self,text="Website:").pack()
            website_text = Text(self, height=1, borderwidth=0, width=30)
            website_text.insert(1.0, website)
            website_text.pack()
            website_text.configure(state="disabled")

            Label(self,text="Username:").pack()
            username_text = Text(self, height=1, borderwidth=0, width=30)
            username_text.insert(1.0, username)
            username_text.pack()
            username_text.configure(state="disabled")    
            
            Label(self,text="Password:").pack()
            password_text = Text(self, height=1, borderwidth=0, width=30)
            password_text.insert(1.0, password)
            password_text.pack()
            password_text.configure(state="disabled")     

            Label(self, text="").pack(pady=15)


class UpdatePassword(Frame):
    def __init__(self,master):
        def update(new_password, website):
            try:
                edit_password(new_password, website)
                Label(self, text="You have succesfully changed your password").pack(side="top", fill="x", pady=10)
            except TypeError:
                    for widget in Frame.winfo_children(self):
                        widget.destroy()
                    Label(self, text="Sorry, we couldn't find that website in our database").pack(side="top", fill="x", pady=10, padx=5)
                    Button(self, text="Return to start page",
                             command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)
            except OperationalError:
                Label(self, text="Sorry, it seems like you have not added any passwords yet.").pack(side="top", fill="x", pady=10, padx=5)
                Button(self, text="Return to start page",
                            command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)                

        Frame.__init__(self, master)
        Label(self, text="You can update an existing password here").pack(side="top", fill="x", pady=10, padx=5)
        Label(self, text="Website:").pack(side="top", fill="x", pady=10)
        website_entry = Entry(self)
        website_entry.pack(side="top",pady=5, padx=5)      
        Label(self, text="New password:").pack(side="top", fill="x", pady=10)
        password_entry = Entry(self)
        password_entry.pack(side="top", pady=5, padx=5)            
        Button(self, text="Update", command=lambda: update(password_entry.get(), website_entry.get())).pack(side="top", pady=5, padx=5)
        Button(self, text="Return to start page",
                command=lambda: master.switch_frame(Menu)).pack(side="top", pady=10, padx=5)    

class UpdateUsername(Frame):
    def __init__(self,master):
        def update(new_username, website):
            try:
                edit_password(new_username, website)
                Label(self, text="You have succesfully changed your username").pack()
            except TypeError:
                    for widget in Frame.winfo_children(self):
                        widget.destroy()
                    Label(self, text="Sorry, we couldn't an entry with that website in our database").pack()
                    Button(self, text="Return to start page",
                             command=lambda: master.switch_frame(Menu)).pack()        


        Frame.__init__(self, master)
        Label(self, text="Update your username").pack(side="top", fill="x", pady=10, padx=5)
        Label(self, text="Website:").pack(side="top", fill="x", pady=10)
        website_entry = Entry(self)
        website_entry.pack(side="top", pady=5, padx=5)      
        Label(self, text="New username:").pack(side="top", fill="x", pady=10)
        username_entry = Entry(self)
        username_entry.pack(side="top", pady=5, padx=5)             
        Button(self, text="Update", command=lambda: update(username_entry.get(), website_entry.get())).pack(side="top", pady=10)
        Button(self, text="Return to start page",
                command=lambda: master.switch_frame(Menu)).pack(side="top", pady=5, padx=5)        

class DeletePassword(Frame):
    def __init__(self, master):
        def delete(website, username):
            try:
                delete_entry(website, username)
                for widget in Frame.winfo_children(self):
                    widget.destroy()
                Label(self, text="You have succesfully deleted that entry").pack(
                                            side="top", fill="x", pady=10, padx=5)
                Button(self, text="Return to start page",
                            command=lambda: master.switch_frame(Menu)).pack()                                                
            except TypeError:
                for widget in Frame.winfo_children(self):
                        widget.destroy()
                Label(self, text="Sorry, we couldn't find that entry in our database").pack()
                Button(self, text="Return to start page",
                            command=lambda: master.switch_frame(Menu)).pack()    
        Frame.__init__(self, master)
        Label(self, text="Delete a password entry along with its website and username").pack(side="top", fill="x", pady=10, padx=5)
        Label(self, text="Website:").pack(side="top", fill="x", pady=10, padx=5)
        website_entry = Entry(self)
        website_entry.pack()
        Label(self, text="Username:").pack(side="top", fill="x", pady=10, padx=5)
        username_entry = Entry(self)
        username_entry.pack()
        Button(self, text="Delete password entry", command= lambda: delete(website_entry.get(), username_entry.get())).pack(side="top", pady=5)
        Label(self, text="Warning, this action is permanent and cannot be undone.", font=("bold")).pack(side="top", fill="x", pady=10, padx=5)



if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()



