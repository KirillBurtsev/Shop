from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import shopDB


class AddProduct(Toplevel):
    """Окно добавления товара"""

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.products: shopDB.Products = master.products
        self.title('Add Product')
        self.resizable(False, False)
        self.geometry('+600+100')
        self.frame = Frame(self, padx=20, pady=10)
        self.product = Entry(self.frame, bd=5)
        self.price = Entry(self.frame, bd=5)
        self.widgets()
        self.grab_set()
        self.focus_set()

    def widgets(self):
        """"Инициализация виджетов"""
        Label(self.frame, text='Product:').grid(row=0, column=0)
        self.product.grid(row=0, column=1, pady=5)
        Label(self.frame, text='Price:').grid(row=1, column=0)
        self.price.grid(row=1, column=1, pady=5)
        Button(self.frame, text=' Save ', command=self.check).grid(row=2, column=0, padx=30)
        Button(self.frame, text=' Cancel ', command=self.destroy).grid(row=2, column=1, padx=30)
        self.frame.pack()

    def check(self):
        """Функция проверки полученных значений"""
        if self.product.get() == '':
            mb.showerror('Error', 'Please fill the description.')
        elif self.price.get() == '':
            mb.showerror('Error', 'Please fill the price.')
        elif self.price.get().isnumeric():
            self.set()
            self.master.update_table()
            self.destroy()
        else:
            mb.showerror('Error', 'Price must be numeric.')

    def set(self):
        """Функция сохранения полученных данных в базу"""
        self.products.add_product(self.product.get(), self.price.get())


class EditProduct(AddProduct):
    """Окно редактирования товара"""

    def __init__(self, master):
        super().__init__(master)
        self.product_id = self.master.chosen_id()
        self.title('Edit Product')
        self.set_old_info()

    def set(self):
        """Функция обновления полученных данных в базе"""
        self.products.edit_product(self.product_id, self.product.get(), self.price.get())

    def set_old_info(self):
        """Подставление старых данных из базы"""
        old_product = self.products.get_product(self.product_id)
        self.product.insert(0, old_product[1])
        self.price.insert(0, int(old_product[2]))


class UserState(Toplevel):
    """Окно изменения роли пользователя"""

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.users: shopDB.Users = master.users
        self.user = self.master.chosen_id()
        self.title('Change User State')
        self.resizable(False, False)
        self.geometry('+400+100')
        self.frame = Frame(self, padx=20, pady=10)
        self.state = ttk.Combobox(self.frame, state="readonly", values=['admin', 'storekeeper', 'user'], width=12)
        self.state.current(2)
        self.widgets()
        self.grab_set()
        self.focus_set()

    def widgets(self):
        """"Инициализация виджетов"""
        Label(self.frame, text='User:').grid(row=0, column=0, pady=5)
        Label(self.frame,
              text=f'{self.user} ({self.master.users.get_state(self.user)})').grid(row=0, column=1)
        Label(self.frame, text='State:').grid(row=1, column=0, pady=5)
        self.state.grid(row=1, column=1)
        Button(self.frame, text=' Save ', command=self.set).grid(row=2, column=0, padx=30)
        Button(self.frame, text=' Cancel ', command=self.destroy).grid(row=2, column=1, padx=30)
        self.frame.pack()

    def set(self):
        """Функция сохранения полученных данных в базу"""
        self.master.users.set_state(self.user, self.state.get())
        self.master.update_table()
        self.destroy()


class UpdateOrder(Toplevel):
    """Окно изменения статуса заказа"""

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.orders: shopDB.Orders = master.orders
        self.order = self.master.chosen_id()
        self.title('Change Order State')
        self.resizable(False, False)
        self.geometry('+400+100')
        self.frame = Frame(self, padx=20, pady=10)
        self.state = ttk.Combobox(self.frame, state="readonly", values=['paid', 'sent'], width=12)
        self.state.current(1)
        self.widgets()
        self.grab_set()
        self.focus_set()

    def widgets(self):
        """"Инициализация виджетов"""
        Label(self.frame, text='Order:').grid(row=0, column=0, pady=5)
        Label(self.frame,
              text=f'''#{self.order} (to {self.orders.get_order_user(self.order)})''').grid(row=0, column=1)
        Label(self.frame, text='State:').grid(row=1, column=0, pady=5)
        self.state.grid(row=1, column=1)
        Button(self.frame, text=' Save ', command=self.set).grid(row=2, column=0, padx=30)
        Button(self.frame, text=' Cancel ', command=self.destroy).grid(row=2, column=1, padx=30)
        self.frame.pack()

    def set(self):
        """Функция сохранения полученных данных в базу"""
        self.orders.set_state(self.order, self.state.get())
        self.master.load_table(self.master.orders.get_all())
        self.destroy()
