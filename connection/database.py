from mysql.connector import connection
from mysql.connector import errorcode
from mysql.connector import Error
import mysql.connector
from lib.config import db_config


class Database:
    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.error = Error
        self.error_code = errorcode
        # self.config = db_config()

    def connect_to_database(self):
        try:
            self.cnx = connection.MySQLConnection(
                user="ortoszyna",
                password="ortoszyna",
                host="127.0.0.1",
                database="ortosoft"
            )
            if self.cnx:
                self.cursor = self.cnx.cursor()
                print("polaczylem sie z baza")
                return True
        except Exception as e:
            print(e)

    def exec_query(self, query, type):
        if type == "select":
            try:
                self.cursor.execute(query)
                return self.cursor.fetchall()
            except Exception as e:
                print(e)
                return None
        else:
            try:
                self.cursor.execute(query)
                self.cnx.commit()
                return True
            except Exception as e:
                print(e)
                return False
            finally:
                self.cursor.close()
                self.cnx.close()





# # TEST
# db = Database()
# db.connect_to_database()
# # print(db.exec_query("select * from klienci limit 1;", "select"))
# print(db.exec_query("update klienci set imie='Damian' where id=1;","update"))
