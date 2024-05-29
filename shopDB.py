import sqlite3


class Users:
    """Таблица пользователей"""

    def __init__(self):
        self.db = sqlite3.connect('shop.db')
        self.c = self.db.cursor()
        self.__create_table()
        if not self.check_username('a'):  # Создание дефолтной учетной записи админа при ее отсутствии
            self.add_user('a', 'a')
        if self.get_state('a') != 'admin':
            self.set_state('a', 'admin')

    def __create_table(self):
        """Создание таблицы пользователей"""
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL PRIMARY KEY,
                                                            password TEXT NOT NULL, 
                                                            state TEXT NOT NULL)''')
        self.db.commit()

    def add_user(self, username, password):
        """Добавление записи пользователя"""
        self.c.execute('''INSERT INTO users (username, password, state) VALUES(?,?,?)''', (username, password, 'user'))
        self.db.commit()

    def del_user(self, username):
        """Удаление записи пользователя"""
        self.c.execute('''DELETE FROM users WHERE username=?''', (username,))
        self.db.commit()

    def get_user(self, username, password):
        """Получение записи пользователя"""
        self.c.execute('''SELECT * FROM users WHERE username=? and password=?''', (username, password))
        return self.c.fetchone()

    def check_username(self, username):
        """Проверка наличия юзернейма в базе"""
        self.c.execute('''SELECT username FROM users WHERE username=?''', (username,))
        return self.c.fetchone()

    def get_state(self, username):
        """Получение роли"""
        self.c.execute('''SELECT state FROM users WHERE username=?''', (username,))
        return self.c.fetchone()[0]

    def set_state(self, username, state):
        """Смена роли пользователя"""
        self.c.execute('''UPDATE users SET state=? WHERE username=?''', (state, username))
        self.db.commit()

    def get_all(self):
        """Получение всех записей из таблицы"""
        self.c.execute('''SELECT * FROM users''')
        return self.c.fetchall()


class Products:
    """Таблица продуктов"""

    def __init__(self):
        self.db = sqlite3.connect('shop.db')
        self.c = self.db.cursor()
        self.__create_table()

    def __create_table(self):
        """Создание таблицы продуктов"""
        self.c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY,
                                                               name TEXT NOT NULL, 
                                                               price REAL NOT NULL)''')
        self.db.commit()

    def add_product(self, product_name, product_price):
        """Добавление записи продукта"""
        self.c.execute('''INSERT INTO products (name, price) VALUES (?,?)''', (product_name, product_price))
        self.db.commit()

    def edit_product(self, product_id: int, product_name, product_price):
        """Изменение записи продукта"""
        self.c.execute('''UPDATE products SET name=?, price=? WHERE id=?''', (product_name, product_price, product_id))
        self.db.commit()

    def del_product(self, product_id):
        """Удаление записи продукта"""
        self.c.execute('''DELETE FROM products WHERE id=?''', (product_id,))
        self.db.commit()

    def get_all(self):
        """Получение всех записей из таблицы"""
        self.c.execute('''SELECT * FROM products''')
        return self.c.fetchall()

    def get_product(self, product_id):
        """Получение записи продукта"""
        self.c.execute('''SELECT * FROM products WHERE id=?''', (product_id,))
        return self.c.fetchone()


class Orders:
    """Таблица заказов"""

    def __init__(self):
        self.db = sqlite3.connect('shop.db')
        self.c = self.db.cursor()
        self.__create_table()

    def __create_table(self):
        """Создание таблицы заказов"""
        self.c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, 
                                                             user TEXT NOT NULL,
                                                             order_list TEXT NOT NULL,                                                             
                                                             total REAL NOT NULL, 
                                                             state TEXT NOT NULL);''')
        self.db.commit()

    def get_all(self):
        """Получение всех записей из таблицы"""
        self.c.execute('''SELECT id, user, order_list, state FROM orders''')
        return self.c.fetchall()

    def get_user_orders(self, username):
        """Получение всех записей о заказах покупателя"""
        self.c.execute('''SELECT id, state, total FROM orders WHERE user=? ''', (username,))
        return self.c.fetchall()

    def get_order_user(self, order_id):
        """Получение юзернейма заказчика"""
        self.c.execute('''SELECT user FROM orders WHERE id=?''', (order_id,))
        return self.c.fetchone()[0]

    def add_order(self, user, order_list, total: int):
        """Создание записи заказа"""
        self.c.execute('''INSERT INTO orders(user, order_list, total, state) VALUES(?,?,?,?)''',
                       (user, order_list, total, 'paid'))
        self.db.commit()

    def set_state(self, order_id, state):
        """Обновление статуса заказа"""
        self.c.execute('''UPDATE orders SET state=? WHERE id=?''', (state, order_id))
        self.db.commit()

    def delete_order(self, order_id):
        """Удаление записи заказа"""
        self.c.execute('''DELETE FROM orders WHERE id=?''', (order_id,))
        self.db.commit()


users = Users()
products = Products()
orders = Orders()
