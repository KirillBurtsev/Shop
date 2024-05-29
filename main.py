import tkinter as tk

from login import Login

if __name__ == '__main__':
    """Запуск приложения"""
    root = tk.Tk()                # инициализация пустого окна приложения
    root.title('Shop')
    root.resizable(False, False)

    Login(root)                  # Вызов окна входа
    root.mainloop()


