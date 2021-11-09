# to do list
from tkinter import *
import json
import string


class JsonTools:
    def __init__(self):
        self.json_file = r"accounts.json"

    def json_save(self, username, password):
        # takes in the username and password
        # saves it into the json file
        json_format = {"username": username, "password": password}
        with open(self.json_file, "r") as f:
            read_file = f.read()
            json_dict = json.loads(read_file)
            json_dict.append(json_format)

        with open(self.json_file, "w") as f:
            json.dump(json_dict, f, indent=4)

    def json_open(self):
        # opens and returns the json file
        with open(self.json_file, "r") as f:
            read_file = f.read()
            json_dict = json.loads(read_file)
        return json_dict


class PasswordChecker:
    def __init__(self, password, confirm_password, message_frame):
        self.password = password
        self.confirm_password = confirm_password
        # pass in instance variable from Signup class
        self.message_frame = message_frame

    def clear(self):
        for widget in self.message_frame.winfo_children():
            widget.destroy()

    def check_number(self):
        for letter in self.password:
            if letter.isnumeric():
                return True
        print("you need at least 1 number")
        number_message = Label(self.message_frame, text="you need at least 1 number")
        number_message.pack()

    def check_capital(self):
        for letter in self.password:
            if letter.isupper():
                return True
        print("you need at least 1 capital letter")
        capital_message = Label(self.message_frame, text="you need at least 1 capital letter")
        capital_message.pack()

    def check_punctuation(self):
        for letter in self.password:
            if letter in string.punctuation:
                return True
        print("you need at least 1 punctuation")
        punctuation_message = Label(self.message_frame, text="you need at least 1 punctuation")
        punctuation_message.pack()

    def check_length(self):
        length = len(self.password)
        if length >= 8:
            return True
        print("password needs to be at least 8 characters long")
        length_message = Label(self.message_frame, text="password needs to be at least 8 characters long")
        length_message.pack()

    def check_confirm_password(self):
        if self.password == self.confirm_password:
            return True
        print("passwords do not match")
        confirm_password_message = Label(self.message_frame, text="password do not match")
        confirm_password_message.pack()

    def main(self):
        self.clear()
        check_number = self.check_number()
        check_capital = self.check_capital()
        check_punctuation = self.check_punctuation()
        check_length = self.check_length()
        confirm_password = self.check_confirm_password()

        if confirm_password:
            if check_number and check_capital and check_punctuation and check_length:
                self.clear()
                print("account created")
                account_created_message = Label(self.message_frame, text="account created")
                account_created_message.pack()

                return True
        return False


class ToDoList:  # needs to be finished
    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x900")
        self.root.title("To-Do-List")
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=10)
        self.entry_frame = Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.add_button = Button(
            self.button_frame, width=5, text="Add", command=self.add_button)
        self.add_button.grid(row=1, column=0)

        self.del_button = Button(
            self.button_frame, width=5, text="Delete", command=self.del_button)
        self.del_button.grid(row=1, column=1)

        self.edit_button = Button(self.button_frame, width=5, text="Edit", command=self.edit_button)
        self.edit_button.grid(row=1, column=2)

        self.task_name_label = Label(self.entry_frame, text="Task Name")
        self.task_name_label.grid(row=0, column=0)
        self.task_name_entry = Entry(self.entry_frame, width=20)
        self.task_name_entry.grid(row=1, column=0)

        self.task_desc_label = Label(self.entry_frame, text="Task Desc")
        self.task_desc_label.grid(row=0, column=1)
        self.task_desc_entry = Entry(self.entry_frame, width=20)
        self.task_desc_entry.grid(row=1, column=1)

        self.task_date_label = Label(self.entry_frame, text="Due Date")
        self.task_date_label.grid(row=0, column=3)
        self.task_date_entry = Entry(self.entry_frame, width=20)
        self.task_date_entry.grid(row=1, column=3)

        self.root.mainloop()

    def add_button(self):
        pass

    def del_button(self):
        pass

    def edit_button(self):
        pass


class Login:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x300")
        self.root.title("Login")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(pady=5)

        # title screen
        self.login_title = Label(self.main_frame, text="Login")
        self.login_title.grid(row=0, column=0)

        # username entry/label
        self.username_label = Label(self.main_frame, text="Username")
        self.username_entry = Entry(self.main_frame)
        self.username_entry.grid(row=2, column=0)
        self.username_label.grid(row=1, column=0)

        # password entry/label
        self.password_label = Label(self.main_frame, text="Password")
        self.password_entry = Entry(self.main_frame, show="*")
        self.password_entry.grid(row=4, column=0)
        self.password_label.grid(row=3, column=0)

        # error message
        self.error_message = Label(self.root, text="")
        self.error_message.pack()

        # login button
        self.login_button = Button(self.root, width=20, text="Login", command=self.main)
        self.login_button.pack()

        # signup button
        self.signup_button = Button(self.root, width=20, text="Signup", command=self.signup_gui)
        self.signup_button.pack()

        self.root.mainloop()

    def check_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        account = {"Username": username, "Password": password}

        # opens json file
        json_file = JsonTools()
        json_account = json_file.json_open()

        if account in json_account:
            # destroys login widget
            # opens the to-do-list widget
            self.root.destroy()
            return True
        else:
            print("Username or Password is invalid")
            self.error_message.configure(text="Username or Password is invalid", fg="red")
        return False

    def signup_gui(self):
        Signup()
        self.root.destroy()

    def main(self):
        if self.check_account():
            ToDoList()


class Signup:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x500")
        self.root.title("Signup")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(pady=5)

        self.login_title = Label(self.main_frame, text="Sign Up")
        self.login_title.grid(row=0, column=0)

        self.username_label = Label(self.main_frame, text="Username")
        self.username_label.grid(row=1, column=0)
        self.username_entry = Entry(self.main_frame)
        self.username_entry.grid(row=2, column=0)

        self.password_label = Label(self.main_frame, text="Password")
        self.password_label.grid(row=3, column=0)
        self.password_entry = Entry(self.main_frame, show="*")
        self.password_entry.grid(row=4, column=0)

        self.confirm_password_label = Label(self.main_frame, text="Confirm Password")
        self.confirm_password_label.grid(row=5, column=0)
        self.confirm_password_entry = Entry(self.main_frame, show="*")
        self.confirm_password_entry.grid(row=6, column=0)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=5)

        self.signup_button = Button(self.button_frame, width=20, text="Signup", command=self.main)
        self.signup_button.grid(row=0, column=0)

        self.login_button = Button(self.button_frame, width=20, text="Login", command=self.login_gui)
        self.login_button.grid(row=1, column=0)

        self.message_frame = Frame(self.root)
        self.message_frame.pack(pady=5)

    def login_gui(self):
        self.root.destroy()
        Login()

    def check_password(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        check_pwd = PasswordChecker(password, confirm_password, self.message_frame)
        if check_pwd.main():
            # if requirements are met
            # saves the username, password into json file
            json_file = JsonTools()
            json_file.json_save(username, password)
            self.root.destroy()

    def main(self):
        self.check_password()


def main():
    Login()


if __name__ == "__main__":
    main()
