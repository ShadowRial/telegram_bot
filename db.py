import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # Проверяем пользователя в БД
    def check(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)

    # Добавляем пользователя
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users ('user_id') VALUES(?)", (user_id,))

    # Устанавливаем активность пользователя
    def set_active(self, active, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET active =? WHERE user_id =?", (active, user_id))

    # Получаем всех активных пользователей
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users WHERE active =1").fetchall()