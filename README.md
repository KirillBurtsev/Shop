# Shop
Lightweight shop management system with tkinder and sqlite3
### Project: Simple Shop Management System

This Python project is a simple shop management system with functionalities to manage users, products, and orders. It uses SQLite as the database backend and provides classes to interact with the database tables.

### Table of Contents

1. [Users](#users)
2. [Products](#products)
3. [Orders](#orders)
4. [Running the Project](#running-the-project)
5. [Contributing](#contributing)
6. [License](#license)

---

### Users <a name="users"></a>

The `Users` class manages the users of the shop system. It provides methods to add, delete, retrieve, and modify user information such as username, password, and user role.

### Products <a name="products"></a>

The `Products` class handles the products available in the shop. It allows adding, editing, deleting, and retrieving product information such as product name and price.

### Orders <a name="orders"></a>

The `Orders` class manages the orders placed by users. It provides functionalities to add new orders, retrieve user orders, update order status, and delete orders.

### Running the Project <a name="running-the-project"></a>

To run the project, ensure you have Python installed on your system. Then, execute the main script `shop.py`. Make sure the `shop.db` file is present in the same directory.

```bash
python shop.py
