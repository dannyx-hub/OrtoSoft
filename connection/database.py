from mysql.connector import connection
from mysql.connector import errorcode
from mysql.connector import Error
from lib.config import db_config
import mysql.connector
from lib.config import db_config


class Database:
    def __init__(self):

        self.cnx = None
        self.cursor = None
        self.error = Error
        self.error_code = errorcode
        self.config = db_config()

    def connect_to_database(self):
        try:
            self.cnx = connection.MySQLConnection(
                user=self.config['user'],
                password=self.config['password'],
                host=self.config['host'],
                database=self.config['database']
            )
            if self.cnx:
                self.cursor = self.cnx.cursor()
                print("polaczylem sie z baza")
                return self.cnx
        except Exception as e:
            print(e)

    def exec_query(self, query, type, cnx):
        cursor = cnx.cursor(buffered=True)
        if type == "select":
            try:
                cursor.execute(query)
                return cursor
            except Exception as e:
                print(e)
                return None
            # finally:
            #     cursor.close()
            #     cnx.close()

        else:
            try:
                cursor.execute(query)
                cnx.commit()
                return True
            except Exception as e:
                print(e)
                return False
            finally:
                cursor.close()
                cnx.close()





# # TEST
# db = Database()
# db.connect_to_database()
# print(db.exec_query("select * from klienci limit 1;", "select"))
# print(db.exec_query("update klienci set imie='Damian' where id=1;","update"))
