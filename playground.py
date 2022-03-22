# import sqlite3

# conn = sqlite3.connect('./data/db/test.db')
# cursor = conn.cursor()
# # cursor.execute('CREATE TABLE user_info (userid varchar(50) primary key, username varchar(50), cookie NUMBER(1))')
# cursor.execute("insert into user_info (userid, username, cookie) values (1,1,1)")
# # cursor.execute("insert into rec (ts, name, before, after) values (\'2022-03-10 00:20:15.695505\', \'Si9H#0724\', '941248155415093261', 'None')")
# cursor.close()
# conn.commit()
# conn.close()

# import requests
# r = requests.get(f'https://g.tenor.com/v1/random?&key=HAQEG9GS7Y2X&q=cat&limit=1')

class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth