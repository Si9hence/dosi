import sqlite3
from disnake.ext import commands
import datetime
import disnake

## choice kaibai
class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="Sure!", style=disnake.ButtonStyle.blurple)
    async def bai(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Nah...", style=disnake.ButtonStyle.blurple)
    async def nobai(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()



async def check(user):
    table_name = "user_info"
    conn = sqlite3.connect('./data/db/test.db')
    async def check_exist():
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE userid = ?", (123,))
        info = cursor.fetchone()
        if info is None:
            cursor.execute(f"insert into user_info (userid, username, cookie, last_active) values ({user.id}, {user.name}, 0,{str(datetime.datetime.now())})")
            cursor.close()
            conn.commit()
            return False
        else:
            return True

    if not check_exist():

