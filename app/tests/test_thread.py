import unittest
import datetime
import copy
from model.project import project
from model.thread import thread
from unittest import mock
from decimal import Decimal

# テスト途中で止めたい時は次の行を挿入する
# import pdb; pdb.set_trace()

class test_thread(unittest.TestCase):

    def setUp(self):
        # テストで使うthreadを1つ作成
        # 正しい値を持ったインスタンスを作成しデータベースに登録まで行う
        self.th = thread()
        self.th.attr["user_id"] = 2
        self.th.attr["title"] = "猫の手も借りたいスレ"

        # project.nameを書き換えておくことでテスト用のDBを利用する
        self.patcher = mock.patch('model.project.project.name', return_value="test_thread")
        self.mock_name = self.patcher.start()
        thread.migrate()
        self.th.save()

    def tearDown(self):
        # テストが終わるたびにテスト用DBをクリア
        thread.db_cleaner()
        self.patcher.stop()
        
    def test_db_is_working(self):
        th = thread.find(self.th.attr["id"])
        # findで帰ってきているのがidならDBに保存されている
        self.assertTrue(type(th) is thread)
        # 最初のheroなのでidは1になる
        self.assertTrue(th.attr["id"] == 1)

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.th.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invalid_attrs(self):
        th_wrong = copy.deepcopy(self.th)
        th_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(th_wrong.is_valid())
        th_wrong = copy.deepcopy(self.th)
        th_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(th_wrong.is_valid())
        th_wrong = copy.deepcopy(self.th)
        th_wrong.attr["user_id"] = None # user_id must be a int
        self.assertFalse(th_wrong.is_valid())
        th_wrong = copy.deepcopy(self.th)
        th_wrong.attr["title"] = 12345 # summary must be a sting
        self.assertFalse(th_wrong.is_valid())

    # default値を持ったthreadインスタンスを生成する
    # Controlerで入力フォームを作るのにも利用する
    def test_build(self):
        th = thread.build()
        self.assertTrue(type(th) is thread)

    # save関数のテストを行う
    # 正例だけ出なく負例もテストするとなお良い
    def test_save(self):
        th = thread.build()
        th.attr["user_id"] = 2
        th.attr["title"] = "テスト"
        th_id = th.save()
        #import pdb; pdb.set_trace()
        self.assertTrue(type(th_id) is int)
        self.assertTrue(th.attr["id"] is not None)
        self.assertTrue(th_id == th.attr["id"])
        self.assertTrue(th_id == 2)

    def test__index(self):
        self.assertEqual(len(thread._index(2)), 1)
        self.assertEqual(thread._index(2)[0], 1)
    

if __name__ == '__main__':
    # unittestを実行
    unittest.main()
