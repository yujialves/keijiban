import MySQLdb
import datetime
from decimal import Decimal
import time

from db import DBConnector
from model.project import project

class chats:
    """チャットモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None
        self.attr["user_id"] = None
        self.attr["thread_id"] = None
        self.attr["content"] = None
        self.attr["datetime"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_chats;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_chats` (
                `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `user_id` int(11) unsigned NOT NULL,
                `thread_id` int(11) unsigned NOT NULL,
                `datetime` DATETIME NOT NULL,
                `content` varchar(1000) NOT NULL,
                PRIMARY KEY (`id`),
                KEY `user_id` (`user_id`),
                KEY `thread_id` (`user_id`)
                )""")
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(id, thread_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_chats
                WHERE  id = %s and thread_id %s;
            """, (id,thread_id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        cb = chats()
        cb.attr["id"] = data["id"]
        cb.attr["user_id"] = data["user_id"]
        cb.attr["datetime"] = data["datetime"]
        cb.attr["content"] = data["content"]
        return ch

    def is_valid(self):
        return all([
            self.attr["id"] is None or type(self.attr["id"]) is int,
            self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
            self.attr["thread_id"] is not None and type(self.attr["thread_id"]) is int,
            self.attr["datetime"] is not None and type(self.attr["datetime"]) is datetime.datetime,
            self.attr["content"] is not None and type(self.attr["content"]) is str and len(self.attr["content"]) > 0,
        ])

    @staticmethod
    def build():
        ch = chats()
        # defaultが設定されている変数はdefault値にしておくと良い
        # 日付も予め値が入っていた方が良い
        # 入力が必要な物はNoneのままにしておく
        ch.attr["datetime"] = datetime.datetime.now()
        ch.attr["content"] = ""
        return ch

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
                INSERT INTO table_chats
                    (user_id, thread_id, content, datetime)
                VALUES
                    (%s, %s, %s, %s); """,
                (self.attr["user_id"],
                self.attr["thread_id"],
                self.attr["content"],
                self.attr["datetime"],
            ))

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
                UPDATE table_chats
                SET user_id = %s,
                    thread_id = %s,
                    content = %s,
                    datetime = %s,
                WHERE id = %s; """,
                (self.attr["user_id"],
                self.attr["thread_id"],
                self.attr["content"],
                self.attr["datetime"],
                self.attr["id"]))
            con.commit()

        return self.attr["id"]

    def delete(self):
        if self.attr["id"] == None: return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_cashbook
                WHERE id = %s; """,
                (self.attr["id"],))
            con.commit()
        return self.attr["id"]

    @staticmethod
    def select(thread_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT * FROM table_chats WHERE thread_id = %s
                """, (thread_id,))
            results = cursor.fetchall()
        records = []
        for data in results:
            ch = chats()
            ch.attr["id"] = data["id"]
            ch.attr["user_id"] = data["user_id"]
            ch.attr["thread_id"] = data["thread_id"]
            ch.attr["datetime"] = data["datetime"]
            ch.attr["content"] = data["content"]
            records.append(ch)
        return records
