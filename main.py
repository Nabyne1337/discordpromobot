import discord
import sqlite3
from random import randint
import re

Db = sqlite3.connect('database.db')
curDb = Db.cursor()
cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dicord_id INTEGER,
            name TEXT,
            promo_id INTEGER,
            referals_count INTEGER,
            used_promo INTEGER)
    ''')
conn.commit()
conn.close()
def getUser(userTg):
    curDb.execute("SELECT * FROM users;")
    users = curDb.fetchall()
    for i in users:
        if str(i[0]) == str(userTg):
            return i

    return -1

def getPromo(userTg):
    curDb.execute("SELECT * FROM users;")
    users = curDb.fetchall()
    for i in users:
        if str(i[2]) == str(userTg):
            return i

    return -1

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if getUser(message.author.id) == -1: 
            curDb.execute(f"""INSERT INTO users (discord_id, name, promo_id, referals_count, used_promo) 
                VALUES('{str(message.author.id)}', '{message.author.name}', '{randint(100000, 999999)}', '0', '0');""")
            Db.commit()

        if message.author == self.user:
            return

        if message.content.lower() == '!моя стата':
            user = getUser(message.author.id)
            return await message.channel.send(f'Твоя стата: \n\nDiscord Id: {user[0]}\nКоличество рефералов: {user[3]}\n\nВаш промокод: {user[2]}')

        words = message.content.lower().split(' ')

        if re.search('\d+', message.content.strip()) is not None:
            promocode = ''.join(i for i in message.content.strip() if not i.isalpha())
            if int(promocode) < 100000:
                return

            get_promo = getPromo(promocode)
            if not get_promo == -1:
                if not str(getUser(message.author.id)[4]) == '0':
                    return await message.channel.send("Вы уже использовали промокод!")

                if not str(getUser(message.author.id)[2]) == str(promocode):
                    return await message.channel.send("Вы не можете использовать свой же промокод!")

                curDb.execute(f"UPDATE users SET referals_count = '{int(get_promo[3]) + 1}' WHERE promo_id = '{promocode}';")
                Db.commit()

                curDb.execute(f"UPDATE users SET used_promo = '{promocode}' WHERE discord_id = '{message.author.id}';")
                Db.commit()

                return await message.channel.send("Промокод принят.")

            else:
                return await message.channel.send("Данного промокода не существует.")


client = MyClient()
client.run('')
