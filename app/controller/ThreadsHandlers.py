import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.thread import thread
from model.profile import profile
from controller.AuthenticationHandlers import SigninBaseHandler


class ThreadsHandler(SigninBaseHandler):
    def get(self):

        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 新規スレッドのタイトルを取得
        p_title = self.get_argument("title", None)
        th = thread.build()
        th.attr["title"] = p_title

        # スレッドを検索する部分文字列を取得
        thread_name = self.get_argument("thread-name", None)

        if p_title is None:
            # ユーザーごとの現金出納帳データを取得
            if thread_name is None:
                results = thread.select_titles()
                self.render("thread.html",
                            thread=results,
                            user=_signedInUser,
                            mode="new",
                            errors=[])
            else:
                results = thread.select_from_titles(thread_name)
                self.render("thread.html",
                            thread=results,
                            user=_signedInUser,
                            mode="new",
                            errors=[])
        else:
            # ユーザーごとの現金出納帳データを取得
            self.render("thread_form.html",
                        thread=th,
                        user=_signedInUser,
                        mode="new",
                        errors=[])


class ThreadsCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        th = thread.build()
        self.render("thread_form.html", user=_signedInUser,
                    mode="new", thread=th, errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_title = self.get_argument("form-title", None)

        # 現金出納帳データの組み立て
        th = thread.build()
        th.attr["user_id"] = int(_id)  # ユーザーIDはサインインユーザーより取得
        th.attr["title"] = p_title

        # パラメータエラーチェック
        errors = []
        if p_title is None:
            errors.append("スレの名前は必須です")

        if len(errors) > 0:  # エラーは新規登録画面に渡す
            self.render("thread_form.html", user=_signedInUser, mode="new", thread=th, errors=[])
            return

        # 登録
        # print(vars(cb))
        th_id = th.save()
        if th_id == False:
            self.render("thread_form.html", user=_signedInUser,
                        mode="new", cashbook=th, errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/thread?title=%s" % tornado.escape.url_escape("登録が完了しました。"))
