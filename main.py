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
        json_format = {"username": username, "password": password, "tasks": []}
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
    def __init__(self, password, confirm_password, username, message_frame):
        self.password = password
        self.confirm_password = confirm_password
        self.username = username
        self.message_frame = message_frame

    def clear(self):
        for widget in self.message_frame.winfo_children():
            widget.destroy()

    def check_number(self):
        for letter in self.password:
            if letter.isnumeric():
                return True
        number_message = Label(
            self.message_frame, text="you need at least 1 number")
        number_message.pack()

    def check_capital(self):
        for letter in self.password:
            if letter.isupper():
                return True
        capital_message = Label(
            self.message_frame, text="you need at least 1 capital letter")
        capital_message.pack()

    def check_punctuation(self):
        for letter in self.password:
            if letter in string.punctuation:
                return True
        punctuation_message = Label(
            self.message_frame, text="you need at least 1 punctuation")
        punctuation_message.pack()

    def check_length(self):
        length = len(self.password)
        if length >= 8:
            return True
        length_message = Label(
            self.message_frame, text="password needs to be at least 8 characters long")
        length_message.pack()

    def check_confirm_password(self):
        if self.password == self.confirm_password:
            return True
        confirm_password_message = Label(
            self.message_frame, text="password do not match")
        confirm_password_message.pack()

    def check_username(self):
        json_file = JsonTools()
        json_accounts = json_file.json_open()

        for acc in range(len(json_accounts)):
            if self.username == "":
                username_message = Label(
                    self.message_frame, text="invalid username")
                username_message.pack()
                return False
            elif self.username in json_accounts[acc].values():
                username_message = Label(
                    self.message_frame, text="invalid username")
                username_message.pack()
                return False
        return True

    def main(self):
        self.clear()
        check_number = self.check_number()
        check_capital = self.check_capital()
        check_punctuation = self.check_punctuation()
        check_length = self.check_length()
        confirm_password = self.check_confirm_password()
        username = self.check_username()

        # if not all are true, prints out error message
        if username:
            if confirm_password:
                if check_number and check_capital and check_punctuation and check_length:
                    self.clear()
                    account_created_message = Label(
                        self.message_frame, text="account created")
                    account_created_message.pack()
                    return True
        return False


class ToDoList:
    def __init__(self, current_user):
        self.focused_frame = None
        self.current_user = current_user

        self.root = Tk()
        self.root.geometry("1000x1300")
        self.root.title("To-Do-List")

        self.button_frame = Frame(self.root)
        self.label_frame = Frame(self.root)

        self.button_frame.pack(pady=10)
        self.label_frame.pack(pady=10)

        self.add_button = Button(self.button_frame, width=5, text="Add",
                                 command=lambda: self.AddTask(self.task_container, self.focused_frame,
                                                              self.focus_frame))
        self.delete_button = Button(
            self.button_frame, width=5, text="Delete", command=self.delete_task)
        self.edit_button = Button(self.button_frame, width=5, text="Edit",
                                  command=lambda: self.EditTask(self.focused_frame).original_text())
        self.save_file_button = Button(self.button_frame, width=5, text="Save",
                                       command=lambda: self.SaveFile(self, self.current_user).main())

        self.add_button.grid(row=1, column=0)
        self.delete_button.grid(row=1, column=1)
        self.edit_button.grid(row=1, column=2)
        self.save_file_button.grid(row=1, column=3)

        self.task_name_label = Label(
            self.label_frame, text="Task Name", width=50)
        self.task_desc_label = Label(
            self.label_frame, text="Task Desc", width=30)
        self.task_date_label = Label(
            self.label_frame, text="Due Date", width=50)

        self.task_name_label.grid(row=0, column=0)
        self.task_desc_label.grid(row=0, column=1)
        self.task_date_label.grid(row=0, column=2)

        self.task_container = Frame(self.root)
        self.task_container.pack(pady=10)

        self.LoadTask(self, self.current_user).main()

        self.root.mainloop()

    # determine the selected frame
    # highlights it in yellow for visual clarity
    def focus_frame(self, event):
        if self.focused_frame:
            for i in self.focused_frame.winfo_children():
                i.configure(bg="white")

            parent_widget = self.root.nametowidget(event.widget.winfo_parent())
            child_widgets = parent_widget.winfo_children()

            self.focused_frame = parent_widget

            for i in child_widgets:
                i.configure(bg="yellow")

            print(child_widgets)
        else:
            parent_widget = self.root.nametowidget(event.widget.winfo_parent())
            child_widgets = parent_widget.winfo_children()

            self.focused_frame = parent_widget

            for i in child_widgets:
                i.configure(bg="yellow")

            print(child_widgets)

    def delete_task(self):
        try:
            self.focused_frame.destroy()
            self.focused_frame = None
        except AttributeError:
            print("focused frame does not exist")

    class SaveFile:
        def __init__(self, ToDoList_class, current_user):
            self.ToDoList_class = ToDoList_class
            self.current_user = current_user
            self.json_tools = JsonTools()

        def format_tasks(self, task_name, task_desc, task_date):
            format_task = {
                "task name": task_name,
                "description": task_desc,
                "due date": task_date
            }
            return format_task

        def get_contents(self, task_container):
            for i in task_container.winfo_children():
                task_labels = [j.cget("text") for j in i.winfo_children()]
                formatted_task = self.format_tasks(
                    task_labels[0], task_labels[1], task_labels[2])
                new_task = self.append_tasks(formatted_task)
                self.save(new_task)

        def append_tasks(self, task_labels):
            data = self.json_tools.json_open()
            for i in data:
                if i["username"] == self.current_user:
                    if task_labels not in i["tasks"]:
                        i["tasks"].append(task_labels)
            return data

        def refresh_tasks(self):
            data = self.json_tools.json_open()
            for i in data:
                if i["username"] == self.current_user:
                    i["tasks"] = []
            return data  # save this one first

        def save(self, data):
            with open(self.json_tools.json_file, "w") as f:
                json.dump(data, f, indent=4)

        def main(self):
            self.save(self.refresh_tasks())
            task_container = self.ToDoList_class.task_container
            self.get_contents(task_container)

    class LoadTask:
        def __init__(self, ToDoList_class, current_user):
            self.json_tools = JsonTools()
            self.ToDoList_class = ToDoList_class
            self.current_user = current_user

        def add_task(self, name, desc, date):
            task_date = name
            task_desc = desc
            task_name = date

            task_frame = Frame(self.ToDoList_class.task_container)
            task_frame.pack(pady=2)

            task_name_label = Label(
                task_frame, text=task_name, width=40, bg="white")
            task_desc_label = Label(
                task_frame, text=task_desc, width=40, bg="white")
            task_date_label = Label(
                task_frame, text=task_date, width=40, bg="white")

            task_name_label.grid(row=0, column=0)
            task_desc_label.grid(row=0, column=1)
            task_date_label.grid(row=0, column=2)

            # calls the focus_frame function after clicking on the label
            task_name_label.bind(
                "<Button-1>", lambda event: self.ToDoList_class.focus_frame(event))
            task_desc_label.bind(
                "<Button-1>", lambda event: self.ToDoList_class.focus_frame(event))
            task_date_label.bind(
                "<Button-1>", lambda event: self.ToDoList_class.focus_frame(event))

        def main(self):
            data = self.json_tools.json_open()
            for i in data:
                if i["username"] == self.current_user:
                    for j in i["tasks"]:
                        self.add_task(j["task name"],
                                      j["description"], j["due date"])

    class AddTask:
        def __init__(self, task_container, focused_frame, focus_frame):
            self.task_container = task_container
            self.focused_frame = focused_frame
            self.focus_frame = focus_frame

            self.root = Tk()
            self.root.geometry("400x100")
            self.root.title("Add Task")

            self.task_frame = Frame(self.root)
            self.task_frame.pack(pady=5)

            self.task_name_label = Label(self.task_frame, text="Task Name")
            self.task_desc_label = Label(self.task_frame, text="Task Desc")
            self.task_date_label = Label(self.task_frame, text="Task Date")

            self.task_name_label.grid(row=0, column=0)
            self.task_desc_label.grid(row=0, column=1)
            self.task_date_label.grid(row=0, column=2)

            self.task_name_entry = Entry(self.task_frame)
            self.task_desc_entry = Entry(self.task_frame)
            self.task_date_entry = Entry(self.task_frame)

            self.task_name_entry.grid(row=1, column=0)
            self.task_desc_entry.grid(row=1, column=1)
            self.task_date_entry.grid(row=1, column=2)

            self.add_button = Button(
                self.root, text="Add Task", command=self.add_task)
            self.add_button.pack(pady=10)

        def add_task(self):
            task_date = self.task_date_entry.get()
            task_desc = self.task_desc_entry.get()
            task_name = self.task_name_entry.get()

            task_frame = Frame(self.task_container)
            task_frame.pack(pady=2)

            task_name_label = Label(
                task_frame, text=task_name, width=40, bg="white")
            task_desc_label = Label(
                task_frame, text=task_desc, width=40, bg="white")
            task_date_label = Label(
                task_frame, text=task_date, width=40, bg="white")

            task_name_label.grid(row=0, column=0)
            task_desc_label.grid(row=0, column=1)
            task_date_label.grid(row=0, column=2)

            # calls the focus_frame function after clicking on the label
            task_name_label.bind(
                "<Button-1>", lambda event: self.focus_frame(event))
            task_desc_label.bind(
                "<Button-1>", lambda event: self.focus_frame(event))
            task_date_label.bind(
                "<Button-1>", lambda event: self.focus_frame(event))

            self.root.destroy()

    class EditTask:
        def __init__(self, focused_frame):
            self.focused_frame = focused_frame

            self.root = Tk()
            self.root.geometry("400x100")
            self.root.title("Edit Task")

            self.task_frame = Frame(self.root)
            self.task_frame.pack(pady=5)

            self.task_name_label = Label(self.task_frame, text="Task Name")
            self.task_desc_label = Label(self.task_frame, text="Task Desc")
            self.task_date_label = Label(self.task_frame, text="Due Date")

            self.task_name_label.grid(row=0, column=0)
            self.task_desc_label.grid(row=0, column=1)
            self.task_date_label.grid(row=0, column=2)

            self.task_name_entry = Entry(self.task_frame)
            self.task_desc_entry = Entry(self.task_frame)
            self.task_date_entry = Entry(self.task_frame)

            self.task_name_entry.grid(row=1, column=0)
            self.task_desc_entry.grid(row=1, column=1)
            self.task_date_entry.grid(row=1, column=2)

            self.save_button = Button(
                self.task_frame, text="Save", command=self.save_new_text)
            self.save_button.grid(row=2, column=1)

        def original_text(self):
            try:
                # gets all the labels from the selected frame and appends it into a list
                # adds each one into the entry as a default text
                child_widget_list = [
                    i.cget("text") for i in self.focused_frame.winfo_children()]
                self.task_name_entry.insert(-1, child_widget_list[0])
                self.task_desc_entry.insert(-1, child_widget_list[1])
                self.task_date_entry.insert(-1, child_widget_list[2])
            except AttributeError:
                self.root.destroy()

        def save_new_text(self):
            child_widget_list = [
                i for i in self.focused_frame.winfo_children()]
            child_widget_list[0].configure(text=self.task_name_entry.get())
            child_widget_list[1].configure(text=self.task_desc_entry.get())
            child_widget_list[2].configure(text=self.task_date_entry.get())
            self.root.destroy()


class Login:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x300")
        self.root.title("Login")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(pady=5)

        self.login_title = Label(self.main_frame, text="Login")
        self.login_title.grid(row=0, column=0)

        self.username_label = Label(self.main_frame, text="Username")
        self.password_label = Label(self.main_frame, text="Password")

        self.username_entry = Entry(self.main_frame)
        self.password_entry = Entry(self.main_frame, show="*")

        self.username_entry.grid(row=2, column=0)
        self.username_label.grid(row=1, column=0)
        self.password_entry.grid(row=4, column=0)
        self.password_label.grid(row=3, column=0)

        self.login_button = Button(
            self.main_frame, width=20, text="Login", command=self.main)
        self.signup_button = Button(
            self.main_frame, width=20, text="Signup", command=self.signup_gui)

        self.login_button.grid(row=5, column=0)
        self.signup_button.grid(row=6, column=0)

        self.error_message = Label(self.main_frame, text="")
        self.error_message.grid(row=7, column=0)

        self.root.mainloop()

    def check_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # opens json file
        json_file = JsonTools()
        json_account = json_file.json_open()

        for i in json_account:
            if username == i["username"]:
                if password == i["password"]:
                    self.root.destroy()
                    return username
        else:
            self.error_message.configure(
                text="Username or Password is invalid", fg="red")

    def signup_gui(self):
        Signup()
        self.root.destroy()

    def main(self):
        founded_account = self.check_account()
        if founded_account:
            ToDoList(founded_account)


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
        self.password_label = Label(self.main_frame, text="Password")
        self.confirm_password_label = Label(
            self.main_frame, text="Confirm Password")

        self.username_entry = Entry(self.main_frame)
        self.password_entry = Entry(self.main_frame, show="*")
        self.confirm_password_entry = Entry(self.main_frame, show="*")

        self.username_label.grid(row=1, column=0)
        self.password_label.grid(row=3, column=0)
        self.confirm_password_label.grid(row=5, column=0)

        self.username_entry.grid(row=2, column=0)
        self.password_entry.grid(row=4, column=0)
        self.confirm_password_entry.grid(row=6, column=0)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=5)

        self.signup_button = Button(
            self.button_frame, width=20, text="Signup", command=self.check_password)
        self.login_button = Button(
            self.button_frame, width=20, text="Login", command=self.login_gui)

        self.signup_button.grid(row=0, column=0)
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

        check_pwd = PasswordChecker(
            password, confirm_password, username, self.message_frame)
        if check_pwd.main():
            # if requirements are met
            # saves the username, password into json file
            json_file = JsonTools()
            json_file.json_save(username, password)
            self.root.destroy()
            ToDoList(username)


def main():
    Login()


if __name__ == "__main__":
    main()
