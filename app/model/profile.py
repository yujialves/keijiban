import MySQLdb
import datetime
from decimal import Decimal

from db import DBConnector
from model.project import project

class profile:
    """プロフィールモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None
        self.attr["user_id"] = None
        self.attr["introduction"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_profile;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_profile` (
                `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
                `user_id` INT(11) NOT NULL,
                `profile_name` VARCHAR(50),
                `introduction` VARCHAR(500)
                )""")
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
          self.attr["introduction"] is not None and type(self.attr["introduction"]) is int and len(str(self.attr["introduction"])) > 0,
        ])

    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    def _db_save(self):
        if self.attr["id"] == None:
            return self._db_save_insert()
        return self._db_save_update()

    def _db_save_insert(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_profile
                    (user_id, introduction)
                VALUES
                    (%s, %s); """,
                (self.attr["user_id"],
                self.attr["introduction"]))
            
            # INSERTされたAUTO INCREMENT値を取得
            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]
    
    def _db_save_update(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_profile
                SET user_id = %s,
                    introduction = %s,
                WHERE id = %s; """,
                (self.attr["user_id"],
                self.attr["introduction"],
                self.attr["id"]))
            con.commit()
        
        return self.attr["id"]

    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_profile
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()
        
        records = []
        for data in results:
            pf = profile()
            pf.attr["id"] = data["id"]
            pf.attr["user_id"] = data["user_id"]
            pf.attr["introduction"] = data["introduction"]
            records.append(pf)

        return records