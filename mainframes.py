from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import shopDB
from miscframes import AddProduct, EditProduct, UserState, UpdateOrder


class FrameOpener:
    """Управляющий клас вызова окон"""

    def __init__(self, username, state, root: Tk):
        self.root = root
        self.username = username
        self.state = state
        self.run()

    def run(self):
        """"Функция инициализации рабочего пространства """
        match self.state:
            case 'admin':
                Admin(self.username, self.root).pack()
            case 'user':
                User(self.username, self.root).pack()
            case 'storekeeper':
                Storekeeper(self.username, self.root).pack()


class DefaultFrame(Frame):
    """Шаблон рабочего пространства"""

    def __init__(self, username, root):
        super().__init__(root)
        self.root: Tk = root
        self.root.maxsize(470, 350)
        self.username = username

        self.users: shopDB.Users = shopDB.users
        self.products: shopDB.Products = shopDB.products
        self.orders: shopDB.Orders = shopDB.orders

        self.table = ttk.Treeview(self, height=25, show='headings', selectmode="browse")
        self.scroll_table = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scroll_table.set)
        self.table_state = StringVar()
        self.top_bar = Menu(self)
        self.root.config(menu=self.top_bar)

    def chosen_id(self):
        """Получение id выделенной записи"""
        try:
            return self.table.item(self.table.focus(), 'values')[0]
        except IndexError:
            mb.showinfo('Error', 'Select the row!')

    def load_table(self, data: list):
        """"Заполнение таблицы данными"""
        self.table.delete(*self.table.get_children())
        for row in data:
            self.table.insert('', 'end', values=row)


class Admin(DefaultFrame):
    """Рабочее пространство Админа"""

    def __init__(self, username, root):
        super().__init__(username, root)
        self.root.title(f"Shop | Admin {self.username}")
        self.widgets()

    def user_table(self):
        """Генерация отображения таблицы users"""
        self.scroll_table.pack_forget()
        self.table.pack_forget()

        self.table.configure(columns=('username', 'password', 'state',))
        self.load_table(self.users.get_all())

        self.table.column('username', width=150, anchor=CENTER)
        self.table.column('password', width=150, anchor=CENTER)
        self.table.column('state', width=150, anchor=CENTER)

        self.table.heading('username', text='Username')
        self.table.heading('password', text='Password')
        self.table.heading('state', text='State')

        self.table_state.set('user')
        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)

    def change_state(self):
        """Функция смены роли пользователя"""
        if self.table_state.get() == 'user' and self.chosen_id():
            UserState(self)

    def del_user(self):
        """Функция удаления пользователя"""
        if self.table_state.get() == 'user' and self.chosen_id():
            ok = mb.askyesno(title="Delete", message=f"Delete user «{self.chosen_id()}»?")
            if ok:
                self.users.del_user(self.chosen_id())
                self.update_table()

    def prod_table(self):
        """Генерация отображения таблицы products"""
        self.scroll_table.pack_forget()
        self.table.pack_forget()
        self.table.configure(columns=('id', 'name', 'price',))
        self.load_table(self.products.get_all())

        self.table.column('id', width=50, anchor=CENTER)
        self.table.column('name', width=250, anchor=CENTER)
        self.table.column('price', width=150, anchor=CENTER)

        self.table.heading('id', text='ID')
        self.table.heading('name', text='Product')
        self.table.heading('price', text='Price')
        self.table_state.set('prod')
        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)

    def del_product(self):
        """Функция удаления продукта"""
        if self.table_state.get() == 'prod' and self.chosen_id():
            ok = mb.askyesno(title="Delete", message=f"Delete product «{self.chosen_id()}»?")
            if ok:
                self.products.del_product(self.chosen_id())
                self.update_table()

    def add_product(self):
        """Функция добавления продукта"""
        if self.table_state.get() == 'prod':
            AddProduct(self)

    def edit_product(self):
        """Функция изменения продукта"""
        if self.table_state.get() == 'prod' and self.chosen_id():
            EditProduct(self)

    def update_table(self):
        """Функция инициализации обновления таблиц"""
        if self.table_state.get() == 'user':
            self.user_table()
        elif self.table_state.get() == 'prod':
            self.prod_table()

    def widgets(self):
        """"Инициализация виджетов"""
        self.user_table()
        user_menu = Menu(self.top_bar)
        user_menu.add_command(label="Open", command=self.user_table)
        user_menu.add_command(label="Change State", command=self.change_state)
        user_menu.add_command(label="Delete User", command=self.del_user)
        self.top_bar.add_cascade(label="Users", menu=user_menu)

        prod_menu = Menu(self.top_bar)
        prod_menu.add_command(label="Open", command=self.prod_table)
        prod_menu.add_command(label="Add Product", command=self.add_product)
        prod_menu.add_command(label="Edit Product", command=self.edit_product)
        prod_menu.add_command(label="Delete Product", command=self.del_product)
        self.top_bar.add_cascade(label="Products", menu=prod_menu)

        self.top_bar.add_cascade(label="Refresh", command=self.update_table)
        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)


class User(DefaultFrame):
    """Рабочее пространство Покупателя"""

    def __init__(self, username, root):
        super().__init__(username, root)
        self.root.title(f"Shop | Customer {self.username}")
        self.cart_ids = []
        self.widgets()

    def prod_table(self, data):
        """Генерация отображения таблицы products"""
        self.scroll_table.pack_forget()
        self.table.pack_forget()
        self.table.configure(columns=('id', 'name', 'price',))
        self.load_table(data)

        self.table.column('id', width=50, anchor=CENTER)
        self.table.column('name', width=250, anchor=CENTER)
        self.table.column('price', width=150, anchor=CENTER)

        self.table.heading('id', text='ID')
        self.table.heading('name', text='Product')
        self.table.heading('price', text='Price')

        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)

    def add_cart(self):
        """Функция добавления продукта в корзину"""
        if self.table_state.get() != 'orders' and self.chosen_id() not in self.cart_ids:
            ok = mb.askyesno(title="Add to Cart", message=f"Add product «{self.chosen_id()}» to Cart?")
            if ok and self.chosen_id() not in self.cart_ids:
                self.cart_ids.append(self.chosen_id())

    def del_cart(self):
        """Функция удаления продукта из корзины"""
        if self.table_state.get() != 'orders' and self.chosen_id() in self.cart_ids:
            ok = mb.askyesno(title="Delete from Cart", message=f"Delete product «{self.chosen_id()}» from Cart?")
            if ok:
                self.cart_ids.remove(self.chosen_id())
                self.update_table()

    def full_prod_table(self):
        """Функция отображения таблицы товаров"""
        self.table_state.set('prod')
        self.prod_table(self.products.get_all())

    def cart_prod_table(self):
        """Функция отображения таблицы товаров в корзине"""
        self.table_state.set('cart')
        data = []
        for product_id in self.cart_ids:
            data.append(self.products.get_product(product_id))
        self.prod_table(data)

    def order_table(self):
        """Генерация отображения таблицы orders"""
        self.scroll_table.pack_forget()
        self.table.pack_forget()
        self.table_state.set('order')
        self.table.configure(columns=('id', 'state', 'total'))
        self.load_table(self.orders.get_user_orders(self.username))

        self.table.column('id', width=50, anchor=CENTER)
        self.table.column('state', width=250, anchor=CENTER)
        self.table.column('total', width=150, anchor=CENTER)

        self.table.heading('id', text='ID')
        self.table.heading('state', text='Order State')
        self.table.heading('total', text='Total')

        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)

    def new_order(self):
        """Функция вызова окна заказа"""
        if self.cart_ids:
            total = 0
            items = []
            for product_id in self.cart_ids:
                items.append(self.products.get_product(product_id)[1])
                total += self.products.get_product(product_id)[2]
            text = f'Products in order:\n{", ".join(items)}\n\nTotal: ${total}\n\nApprove order?'
            ok = mb.askyesno(title="New Order", message=text)
            if ok:
                print(self.username, self.cart_ids, int(total))
                self.orders.add_order(self.username, ', '.join(self.cart_ids), int(total))
                self.cart_ids = []
                self.order_table()

    def update_table(self):
        """Функция инициализации обновления таблиц"""
        if self.table_state.get() == 'prod':
            self.full_prod_table()
        elif self.table_state.get() == 'cart':
            self.cart_prod_table()
        elif self.table_state.get() == 'order':
            self.order_table()

    def widgets(self):
        """"Инициализация виджетов"""
        self.full_prod_table()
        prod_menu = Menu(self.top_bar)
        prod_menu.add_command(label="Open Showcase", command=self.full_prod_table)
        prod_menu.add_command(label="Add to Cart", command=self.add_cart)
        prod_menu.add_command(label="Show Cart", command=self.cart_prod_table)
        prod_menu.add_command(label="Delete from Cart", command=self.del_cart)
        self.top_bar.add_cascade(label="Products", menu=prod_menu)

        order_menu = Menu(self.top_bar)
        order_menu.add_command(label="My Orders", command=self.order_table)
        order_menu.add_command(label="New Order", command=self.new_order)
        self.top_bar.add_cascade(label="Orders", menu=order_menu)

        self.top_bar.add_cascade(label="Refresh", command=self.update_table)
        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)


class Storekeeper(DefaultFrame):
    """Рабочее пространство"""

    def __init__(self, username, root):
        super().__init__(username, root)
        self.root.title(f"Shop | Storekeeper {self.username}")
        self.widgets()

    def del_order(self):
        """"Функция удаления заказа"""
        if self.chosen_id():
            ok = mb.askyesno(title="Delete Order", message=f"Delete order «{self.chosen_id()}»?")
            if ok:
                self.orders.delete_order(self.chosen_id())
                self.load_table(self.orders.get_all())

    def update_order(self):
        """Функция измененя статуска заказа"""
        if self.chosen_id():
            UpdateOrder(self)

    def widgets(self):
        """"Инициализация виджетов"""
        self.table.configure(columns=('id', 'user', 'order_list', 'state'))
        self.load_table(self.orders.get_all())

        self.table.column('id', width=50, anchor=CENTER)
        self.table.column('user', width=50, anchor=CENTER)
        self.table.column('order_list', width=200, anchor=CENTER)
        self.table.column('state', width=150, anchor=CENTER)

        self.table.heading('id', text='ID')
        self.table.heading('user', text='Client')
        self.table.heading('order_list', text='Products List')
        self.table.heading('state', text='Order State')

        order_menu = Menu(self.top_bar)
        order_menu.add_command(label="Change State", command=self.update_order)
        order_menu.add_command(label="Delete Order", command=self.del_order)
        self.top_bar.add_cascade(label="Order", menu=order_menu)

        self.top_bar.add_cascade(label="Refresh", command=lambda: self.load_table(self.orders.get_all()))
        self.table.pack(side=LEFT)
        self.scroll_table.pack(side=LEFT, fill=Y)
