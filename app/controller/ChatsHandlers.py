import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.chats import chats
from controller.AuthenticationHandlers import SigninBaseHandler

class ChatsShowHandler(SigninBaseHandler):
    def get(self, thread_id):
        # ログインしていなければログイン画面へリダイレクト
        if not self.current_user:
            self.redirect("/signin")
            return

        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # モデルから全てのチャットを取得
        ch = chats.select(thread_id)
        if ch is None: raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す

        # chats.htmlへリダイレクト
        self.render("chats.html", user=_signedInUser, mode="show", chats=ch, messages=[], errors=[], thread=thread_id)

class ChatsInsertHandler(SigninBaseHandler):
    def get(self, thread_id):
        # ログインしていなければログイン画面へリダイレクト
        if not self.current_user:
            self.redirect("/signin")
            return

        # サインインユーザの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 他の画面からinsert-textの取得
        insert_text = self.get_argument("insert-text", None)

        ch = chats.build()
        ch.attr["user_id"] = int(_id)
        ch.attr["content"] = insert_text
        ch.attr["thread_id"] = thread_id

        # DBにテキストの内容を挿入
        ch._db_save()

        self.redirect("/chats/" + thread_id)
