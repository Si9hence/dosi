from pydoc import describe
import sqlite3
import aiosqlite 

class Sql:
    def __init__(self, db='./data/db/test.db') -> None:
        self.db = db

    def execute(self, query):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()

    def fetch(self, query, header=True, order='reversed'):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        if header:
            names = [description[0] for description in cursor.description]
            tmp = list()
            for item in res:
                tmp.append(dict((names, item) for names, item in zip(names, item)))
        cursor.close()
        conn.commit()
        conn.close()

        res = tmp
        res.sort(key=lambda x: str(x["expires"]))
        if order == 'reversed':
            res = res [::-1]
        # res = 1
        return res

    async def execuate_a(self, query):
        conn = await aiosqlite.connect(self.db)
        cursor = await conn.cursor()
        await cursor.execute(query)
        await cursor.close()
        await conn.commit()
        await conn.close()

    def create_table(self, table: str, columns: list, replace=False):
        """
        the first element in keys will be the primary key
        """

        if replace == True:
            self.drop_ie(table)
            print(f'table {table} has been dropped successfully')
        query = f"CREATE TABLE IF NOT EXISTS {table} ("
        for idx, column in enumerate(columns):
            if idx == 0:
                query += " ".join(column) + " PRIMARY KEY, "
            else:
                query += " ".join(column)
                if idx != len(columns) - 1:
                    query += ", "
        query += ");"
        # print(query)
        self.execute(query)
        print(f'table {table} has been created successfully')

    def drop_ie(self, table:str):
        query = f"DROP TABLE IF EXISTS {table};"
        self.execute(query)
    
    def insert(self, table:str, columns: list):
        query = f"INSERT INTO {table}"
        cols, vals = map(list, zip(*columns))
        query += f"""({",".join(cols)}) VALUES("""
        for idx, val in enumerate(vals):
            query += "\"" + val + "\""
            if idx != len(vals)-1:
                query += ","
        query += ");"
        print(query)
        self.execute(query)

    async def insert_a(self, table:str, columns: list):
        query = f"INSERT INTO {table}"
        cols, vals = map(list, zip(*columns))
        query += f"({','.join(cols)}) VALUES({','.join(vals)});"
        await self.execute(query)

    def select(self, table:str, columns:list=list(), limit:int=0):
        if not columns:
            columns="*"
        query = f"SELECT {columns} FROM {table}"
        if limit:
            query += f" LIMIT {limit}"
    
    def clear(self, table:str):
        query = f"DELETE FROM {table}"
        self.execute(query)
# conn = sqlite3.connect('./data/db/test.db')
# cursor = conn.cursor()
# # cursor.execute('CREATE TABLE user_info (userid varchar(50) primary key, username varchar(50), cookie NUMBER(1))')
# # cursor.execute("insert into user_info (userid, username, cookie) values (1,1,1)")
# # cursor.execute("insert into rec (ts, name, before, after) values (\'2022-03-10 00:20:15.695505\', \'Si9H#0724\', '941248155415093261', 'None')")
# cursor.close()
# conn.commit()
# conn.close()
