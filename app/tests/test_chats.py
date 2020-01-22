import unittest
import datetime
import copy
from model.project import project
from model.chats import chats
from unittest import mock
from decimal import Decimal

# テスト途中で止めたい時は次の行を挿入する
# import pdb; pdb.set_trace()

class test_chats(unittest.TestCase):

    def setUp(self):
        # テストで使うchatsを1つ作成
        # 正しい値を持ったインスタンスを作成しデータベースに登録まで行う
        self.ch = chats()
        self.ch.attr["user_id"] = 2
        self.ch.attr["thread_id"] = 2
        self.ch.attr["content"] = "こんにちは"
        self.ch.attr["datetime"] = datetime.datetime.now().date()

        # project.nameを書き換えておくことでテスト用のDBを利用する
        self.patcher = mock.patch('model.project.project.name', return_value="test_chats")
        self.mock_name = self.patcher.start()
        chats.migrate()
        self.ch.save()

    def tearDown(self):
        # テストが終わるたびにテスト用DBをクリア
        chats.db_cleaner()
        self.patcher.stop()

    def test_db_is_working(self):
        ch = chats.find(self.ch.attr["id"], self.ch.attr["thread_id"])
        # findで帰ってきているのがidならDBに保存されている
        self.assertTrue(type(ch) is chats)
        # 最初のchatなのでidは1になる
        self.assertTrue(ch.attr["id"] == 1)

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.ch.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invalid_attrs(self):
        ch_wrong = copy.deepcopy(self.ch)
        ch_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(ch_wrong.is_valid())
        ch_wrong = copy.deepcopy(self.ch)
        ch_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(ch_wrong.is_valid())
        ch_wrong = copy.deepcopy(self.ch)
        ch_wrong.attr["user_id"] = None # user_id must be a int
        self.assertFalse(ch_wrong.is_valid())
        ch_wrong = copy.deepcopy(self.ch)
        ch_wrong.attr["thread_id"] = None # thread_id must be a int
        self.assertFalse(ch_wrong.is_valid())
        ch_wrong = copy.deepcopy(self.ch)
        ch_wrong.attr["content"] = 12345 # content must be str
        self.assertFalse(ch_wrong.is_valid())
        ch_wrong = copy.deepcopy(self.ch)
        ch_wrong.attr["datetime"] = 12345 # datetime must be a datatime.date object
        self.assertFalse(ch_wrong.is_valid())


    # default値を持ったcashbookインスタンスを生成する
    # Controlerで入力フォームを作るのにも利用する
    def test_build(self):
        ch = chats.build()
        self.assertTrue(type(ch) is chats)

    # save関数のテストを行う
    # 正例だけ出なく負例もテストするとなお良い
    def test_save(self):
        ch = chats.build()
        ch.attr["user_id"] = 2
        ch.attr["thread_id"] = 2
        ch.attr["content"] = "テスト"
        ch_id = ch.save()
        #import pdb; pdb.set_trace()
        self.assertTrue(type(ch_id) is int)
        self.assertTrue(ch.attr["id"] is not None)
        self.assertTrue(ch_id == ch.attr["id"])
        self.assertTrue(ch_id == 2)

    def test_select(self):
        self.assertEqual(len(chats._select(2)), 1)
        self.assertEqual(chats._select(2)[0], 1)

if __name__ == '__main__':
    # unittestを実行
    unittest.main()
