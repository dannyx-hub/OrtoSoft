# """
# Kod odpowiadajacy za generowanie wszystkich potrzebnych query do bazy danych.
# Kazde zapytanie do bazy powinno byc tutaj
# """
# from database import Database
#
#
# class Query:
#
#     def __init_(self):
#         self.db = Database()
#         self.cursor = self.db.cursor
#
#     def exec_select(self, query):
#         query_exec = self.db.cursor.execute(query)
#         if query_exec:
#             self.db.cnx.close()
#             return query_exec.fetchall()
#
#
# ### Test
#
# q = Query()
# query = "select * from klienci limit 10;"
# r = q.exec_select(query)
# print(r)
