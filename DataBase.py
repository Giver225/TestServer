# таблицы:
# 1 - данные для входа: логин*, пароль
# 2 - Пользователи: логин*, фио, статус, телефон, пол, дата рождения, мыло, симптомы, дата поступления, аватарка, лечущий врач
import sqlite3

db = sqlite3.connect('users.db')

c = db.cursor()

# c.execute("""CREATE TABLE accounts (
#     login text,
#     password text
# )""")
c.execute('SELECT * FROM accounts')
print(c.fetchall())

db.commit()
db.close()
