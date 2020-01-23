import MySQLdb

from db import DBConnector
from model.project import project


class thread:
    """スレッドモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None
        self.attr["user_id"] = None
        self.attr["name"] = None
        self.attr["title"] = None
        self.attr["user_id"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' %
                           project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_thread;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_thread` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `user_id` int(11) unsigned NOT NULL,
                    `name` varchar(100),
                    `title` varchar(1000) NOT NULL,
                    PRIMARY KEY (`id`),
                    KEY `user_id` (`user_id`),
                    KEY `title` (`title`)
                    )""")
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_thread
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        th = thread()
        th.attr["id"] = data["id"]
        th.attr["user_id"] = data["user_id"]
        th.attr["title"] = data["title"]

        return th

    def is_valid(self):
        return all([
            self.attr["id"] is None or type(self.attr["id"]) is int,
            self.attr["user_id"] is not None and type(
                self.attr["user_id"]) is int,
            self.attr["title"] is not None and type(
                self.attr["title"]) is str and len(self.attr["title"]) > 0
        ])

    @staticmethod
    def build():
        th = thread()
        # defaultが設定されている変数はdefault値にしておくと良い
        # 入力が必要な物はNoneのままにしておく
        th.attr["title"] = None
        return th

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
                INSERT INTO table_thread
                    (user_id, title)
                VALUES
                    (%s, %s); """, (self.attr["user_id"], self.attr["title"]))

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
                UPDATE table_thread
                SET user_id = %s,
                    title = %s
                WHERE id = %s; """, (self.attr["user_id"], self.attr["title"]))
            con.commit()

        return self.attr["id"]

    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_thread
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()

        records = []
        for data in results:
            th = thread()
            th.attr["id"] = data["id"]
            th.attr["user_id"] = data["user_id"]
            th.attr["title"] = data["title"]
            records.append(th)

        return records

    @staticmethod
    def select_titles():
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_thread
                LEFT OUTER JOIN table_profile 
                USING(user_id);
            """)
            results = cursor.fetchall()

        records = []
        for data in results:
            th = thread()
            th.attr["id"] = data["id"]
            th.attr["user_id"] = data["user_id"]
            th.attr["name"] = data["name"]
            th.attr["title"] = data["title"]
            if data["nick_name"] is not None:
                th.attr["nick_name"] = data["nick_name"]
            else:
                th.attr["nick_name"] = None
            records.append(th)

        return records

    def delete(self):
        if self.attr["id"] == None:
            return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_thread
                WHERE id = %s; """,
                           (self.attr["id"],))
            con.commit()

        return self.attr["id"]

    @staticmethod
    def _index(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT id FROM table_thread
                WHERE user_id = %s; """,
                           (user_id,))
            con.commit()
            recodes = cursor.fetchall()

        ids = [recode[0] for recode in recodes]
        return ids
