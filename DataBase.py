# таблицы:
# 1 - данные для входа: логин*, пароль
# 2 - Пользователи: логин*, фио, статус, телефон, пол, дата рождения, мыло, симптомы, дата поступления, аватарка, лечущий врач
import sqlite3

db = sqlite3.connect('users.db')

c = db.cursor()

# c.execute("""CREATE TABLE accounts (
#     login text,
#     password text,
#     name text,
#     status text,
#     phone text,
#     male text,
#     date_of_birth date,
#     email text
# )""")
c.execute('DELETE FROM accounts')
c.execute("INSERT INTO accounts VALUES ('Goverd', '123', 'Danil', 'doctor', '88005553535', 'm', '2002-12-23', 'giver_225@mail.ru')")
# c.execute('DELETE FROM accounts')
# c.execute('SELECT * FROM accounts')
# print(c.fetchall())
db.commit()
db.close()
