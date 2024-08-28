import sqlite3
from cryptography.fernet import Fernet
import password_keeper
from tkinter import *  # Used for the graphical user interface (gui)
from tkinter import messagebox
def show_all(key, username):
   f = Fernet(key)
   conn = sqlite3.connect("registryUsers.db")
   c = conn.cursor()
   c.execute("SELECT rowid, * FROM " + username)
   items = c.fetchall()
   root = Tk()
   root.title("Your Passwords:")
   root.iconbitmap("ExtraSupportContent/florestechnologylogo.ico")
   width = 600
   height = 800
   root.geometry(str(width) + "x" + str(height))
   screen_width = root.winfo_screenwidth()
   screen_height = root.winfo_screenheight()
   x_coordinate = int((screen_width / 2) - (width / 2))
   y_coordinate = int((screen_height / 2) - (height / 2))
   root.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))
   main_frame = Frame(root)
   main_frame.pack(fill=BOTH, expand=1)
   my_canvas = Canvas(main_frame)
   my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
   my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
   my_scrollbar.pack(side=RIGHT, fill=Y)
   my_canvas.configure(yscrollcommand=my_scrollbar.set)
   my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

   second_frame = Frame(my_canvas)
   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   sb = Scrollbar(root)
   sb.pack(side=RIGHT, fill=Y)
   mylist = Listbox(root, yscrollcommand=sb.set, width=width, height=(height-20))
   for item in items:
       decrypted_user = f.decrypt(item[1])
       original_user = decrypted_user.decode()
       decrypted_pass = f.decrypt(item[2])
       original_pass = decrypted_pass.decode()
       decrypted_email = f.decrypt(item[3])
       original_email = decrypted_email.decode()
       decrypted_info = f.decrypt(item[4])
       original_info = decrypted_info.decode()
       mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
       mylist.insert(END, "Id: " + str(item[0]))
       mylist.insert(END, "User/Website: " + original_user)
       mylist.insert(END, "Password: " + original_pass)
       mylist.insert(END, "Email: " + original_email)
       mylist.insert(END, "Info: " + original_info)
       mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
       mylist.insert(END, "")
   def go_back():
        root.destroy()
        password_keeper.mainPasswordKeeper(username)
        Button(root, text="Return", command=go_back).pack()

        mylist.pack(side=LEFT)
        sb.config(command=mylist.yview)
        conn.commit()
        conn.close()
   def add_one(username, user, password, email, info):
        conn = sqlite3.connect("registryUsers.db")
        c = conn.cursor()
        c.execute("INSERT INTO " + username + " VALUES (?, ?, ?, ?)", (user, password, email, info))
        conn.commit()
        conn.close()

   def delete_one(username, id_var):
        conn = sqlite3.connect("registryUsers.db")
        c = conn.cursor()
        c.execute("DELETE from " + username + " WHERE rowid = " + id_var)
        conn.commit()
        conn.close()

   def name_lookup(key, username, name):
     f = Fernet(key)
     conn = sqlite3.connect("registryUsers.db")
   c = conn.cursor()
   c.execute("SELECT rowid, * FROM " + username)
   items = c.fetchall()
   toplvl = Toplevel()
   toplvl.title("Search...")
   toplvl.iconbitmap("ExtraSupportContent/florestechnologylogo.ico")
   width = 600
   height = 800
   screen_width = toplvl.winfo_screenwidth()
   screen_height = toplvl.winfo_screenheight()
   x_coordinate = int((screen_width / 2) - (width / 2))
   y_coordinate = int((screen_height / 2) - (height / 2))
   toplvl.geometry(str(width) + "x" + str(height))
   toplvl.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))
   sb = Scrollbar(toplvl)
   sb.pack(side=RIGHT, fill=Y)
   mylist = Listbox(toplvl, yscrollcommand=sb.set, width=width, height=(height - 20))
   for item in items:
       decrypted_name = f.decrypt(item[1])  # The rowid is in the '0' position, so name is in '1'
       original_name = decrypted_name.decode()
       if original_name == name:
           decrypted_pass = f.decrypt(item[2])
           original_pass = decrypted_pass.decode()
           decrypted_email = f.decrypt(item[3])
           original_email = decrypted_email.decode()
           decrypted_info = f.decrypt(item[4])
           original_info = decrypted_info.decode()
           mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
           mylist.insert(END, "Id: " + str(item[0]))
           mylist.insert(END, "User/Website: " + original_name)
           mylist.insert(END, "Password: " + original_pass)
           mylist.insert(END, "Email: " + original_email)
           mylist.insert(END, "Info: " + original_info)
           mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
           mylist.insert(END, "")
   def go_back():
        toplvl.destroy()
        Button(toplvl, text="Return", command=go_back).pack()
        mylist.pack(side=LEFT)
        sb.config(command=mylist.yview)
        toplvl.mainloop()

        conn.commit()
        conn.close()
   def id_lookup(key, username, id):
        f = Fernet(key)
        conn = sqlite3.connect("registryUsers.db")
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM " + username + " WHERE rowid = (?)", id)
        items = c.fetchall()
        toplvl = Toplevel()
        toplvl.title("Search...")
        toplvl.iconbitmap("ExtraSupportContent/florestechnologylogo.ico")
        width = 600
        height = 800
        screen_width = toplvl.winfo_screenwidth()
        screen_height = toplvl.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        toplvl.geometry(str(width) + "x" + str(height))
        toplvl.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

        try:
            for item in items:
                decrypted_name = f.decrypt(item[1])
                original_name = decrypted_name.decode()
                if int(id) == item[0]:  # The rowid is in the '0' position
                    decrypted_pass = f.decrypt(item[2])
                    original_pass = decrypted_pass.decode()
                    decrypted_email = f.decrypt(item[3])
                    original_email = decrypted_email.decode()
                    decrypted_info = f.decrypt(item[4])
                    original_info = decrypted_info.decode()
                    info = "Id: " + str(item[0]) + "\n" + "User/Website: " + original_name + "\n" + "Password: " + original_pass \
                                    + "\n" + "Email: " + original_email + "\n\n" + "Info: " + original_info
                    Label(toplvl, text=info, font=("Times New Roman", 15)).pack()
        except:
            messagebox.showerror("Error", "There is no registry with that ID.")
   def go_back():
        toplvl.destroy()
        Button(toplvl, text="Return", font=("Times New Roman", 15), command=go_back).pack()
        toplvl.mainloop()
        conn.commit()
        conn.close()
   def email_lookup(key, username, email):

    f = Fernet(key)
    conn = sqlite3.connect("registryUsers.db")

   c = conn.cursor()
   c.execute("SELECT rowid, * FROM " + username)
   items = c.fetchall()
   toplvl = Toplevel()
   toplvl.title("Search...")
   toplvl.iconbitmap("ExtraSupportContent/florestechnologylogo.ico")
   width = 600
   height = 800
   screen_width = toplvl.winfo_screenwidth()
   screen_height = toplvl.winfo_screenheight()
   x_coordinate = int((screen_width / 2) - (width / 2))
   y_coordinate = int((screen_height / 2) - (height / 2))
   toplvl.geometry(str(width) + "x" + str(height))
   toplvl.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))
   sb = Scrollbar(toplvl)
   sb.pack(side=RIGHT, fill=Y)
   mylist = Listbox(toplvl, yscrollcommand=sb.set, width=width, height=(height - 20))
   for item in items:
       decrypted_name = f.decrypt(item[1])  # The rowid is in the '0' position, so name is in '1'
       original_name = decrypted_name.decode()
       decrypted_email = f.decrypt(item[3])  # The email is in position '3'
       original_email = decrypted_email.decode()
       if original_email == email:
           decrypted_pass = f.decrypt(item[2])
           original_pass = decrypted_pass.decode()
           decrypted_info = f.decrypt(item[4])
           original_info = decrypted_info.decode()
           mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
           mylist.insert(END, "Id: " + str(item[0]))
           mylist.insert(END, "User/Website: " + original_name)
           mylist.insert(END, "Password: " + original_pass)
           mylist.insert(END, "Email: " + original_email)
           mylist.insert(END, "Info: " + original_info)
           mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
           mylist.insert(END, "")
   def go_back():
        toplvl.destroy()
        Button(toplvl, text="Return", command=go_back).pack()
        mylist.pack(side=LEFT)
        sb.config(command=mylist.yview)
        toplvl.mainloop()

        conn.commit()
        conn.close()
def update_one(username, user, password, email, info, id):
   conn = sqlite3.connect("registryUsers.db")
   c = conn.cursor()
   c.execute(" UPDATE " + username + " SET username = (?) WHERE rowid = (?)", (user, id))
   c.execute(" UPDATE " + username + " SET password = (?) WHERE rowid = (?)", (password, id))
   c.execute(" UPDATE " + username + " SET email = (?) WHERE rowid = (?)", (email, id))
   c.execute(" UPDATE " + username + " SET info = (?) WHERE rowid = (?)", (info, id))
   conn.commit()
   conn.close()
def createTable(username):
   connection = sqlite3.connect("registryUsers.db")
   cursor = connection.cursor()
   cursor.execute("CREATE TABLE " + username + "(username text, password text, email text, info text)")
   connection.commit()
   connection.close()
