import sqlite3
from config import sqlite3_info


# 自定义row构造器，返回字典对象，可以通过列名索引
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# https://blog.bombox.org/2016-06-22/python-sqlite/
class SqliteHandler():
    # 数据库连接
    con = None
    # 游标
    cur = None

    def __init__(self, db_path = sqlite3_info['sqlite3']):
        self.path = db_path
        self.__connect()

    def __connect(self):
        try:
            self.con = sqlite3.connect(self.path)
            self.con.row_factory = dict_factory
            self.cur = self.con.cursor()
        except Exception as e:
            print('error: %s' % e)

    def close(self):
        try:
            self.cur.close()
            self.con.close()
        except Exception as e:
            print('error: %s' % e)

    def execute_select(self, sql, params = ()):
        try:
            self.cur.execute(sql, params)
            result =  self.cur.fetchall()
            return result
        except Exception as e:
            print('error: %s' % e)
            return False


    def execute_select_one(self, sql, params = ()):
        try:
            self.cur.execute(sql, params)
            result = self.cur.fetchone()
            return result
        except Exception as e:
            print('error: %s' % e)
            return False

    def insert_one(self, sql, params = ()):
        try:
            self.cur.execute(sql, params)
            result_row = self.cur.lastrowid
            self.con.commit()
            return result_row
        except Exception as e:
            print('error: %s' % e)
            self.con.rollback()
            return False


    def insert_many(self, sql, params):
        try:
            self.cur.executemany(sql, params)
            result_rows = self.cur.rowcount
            self.con.commit()
            return result_rows
        except Exception as e:
            print('error: %s' % e)
            self.con.rollback()
            return False


    def execute_update(self, sql, params = ()):
        try:
            self.cur.execute(sql, params)
            result_rows = self.cur.rowcount
            self.con.commit()
            if not result_rows:
                result_rows = True
            return result_rows
        except Exception as e:
            print('error: %s'%e)
            self.con.rollback()
            return False

    def execute_sql(self, sql, params = ()):
        try:
            self.cur.execute(sql, params)
            self.con.commit()
            return True
        except Exception as e:
            print('error: %s' % e)
            self.con.rollback()
            return False

