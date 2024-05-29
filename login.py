from tkinter import *

import shopDB
from shopDB import users
from tkinter import messagebox as mb
from mainframes import FrameOpener


class Login:
    """Окно входа в систему"""

    def __init__(self, root: Tk):
        self.root = root
        self.users: shopDB.Users = users
        self.login_frame = Frame(self.root, padx=20, pady=10)
        self.username_l = Entry(self.login_frame, bd=5)
        self.password_l = Entry(self.login_frame, bd=5, show='*')

        self.reg_frame = Frame(self.root, padx=20, pady=10)
        self.username_r = Entry(self.reg_frame, bd=5)
        self.password_r = Entry(self.reg_frame, bd=5, show='*')

        self.widgets()

    def to_reg(self):
        """Вызов интерфейса регистрации"""
        self.login_frame.pack_forget()
        self.username_l.delete(0, END)
        self.password_l.delete(0, END)
        self.reg_frame.pack()

    def to_log(self):
        """Вызов интерфейса логина"""
        self.reg_frame.pack_forget()
        self.username_r.delete(0, END)
        self.password_r.delete(0, END)
        self.login_frame.pack()

    def reg(self):
        """Регистрация пользователя"""
        if self.username_r.get() == '':
            mb.showerror('Error', 'Please fill the username.')
        elif self.users.check_username(self.username_r.get()):
            mb.showerror('Error', 'This username is already taken.')
        elif self.password_r.get() == '':
            mb.showerror('Error', 'Please fill the password')
        else:
            self.users.add_user(self.username_r.get(), self.password_r.get())
            mb.showinfo('Success', 'Account created.\nSign in please!')
            self.to_log()

    def login(self):
        """"Вход"""
        if self.username_l.get() == '':
            mb.showerror('Error', 'Please fill the username.')
        elif self.password_l.get() == '':
            mb.showerror('Error', 'Please fill the password')
        elif self.users.get_user(self.username_l.get(), self.password_l.get()):
            self.login_frame.pack_forget()
            FrameOpener(self.username_l.get(), self.users.get_state(self.username_l.get()), self.root)
        else:
            mb.showerror('Error', 'Incorrect username or password.')

    def widgets(self):
        """"Инициализация виджетов"""
        Label(self.login_frame, text='SIGN IN', font=('', 20), pady=10).grid(row=0, column=0, columnspan=2)
        Label(self.login_frame, text='Username: ').grid(row=1, column=0, pady=10)
        self.username_l.grid(row=1, column=1)
        Label(self.login_frame, text='Password: ').grid(row=2, column=0, pady=10)
        self.password_l.grid(row=2, column=1)
        Button(self.login_frame, text='Sign In', command=self.login).grid(row=3, column=0, padx=20, pady=10)
        Button(self.login_frame, text='Sign Up', command=self.to_reg).grid(row=3, column=1, padx=20)
        self.login_frame.pack()

        Label(self.reg_frame, text='SIGN UP', font=('', 20), pady=10).grid(row=0, column=0, columnspan=2)
        Label(self.reg_frame, text='Username: ').grid(row=1, column=0, pady=10)
        self.username_r.grid(row=1, column=1)
        Label(self.reg_frame, text='Password: ').grid(row=2, column=0, pady=10)
        self.password_r.grid(row=2, column=1)
        Button(self.reg_frame, text='Sign Up', command=self.reg).grid(row=3, column=0, padx=20, pady=10)
        Button(self.reg_frame, text='Sign In', command=self.to_log).grid(row=3, column=1, padx=20)
