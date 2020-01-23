import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.cashbook import cashbook
from model.profile import profile
from controller.AuthenticationHandlers import SigninBaseHandler

class ProfileUpdateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # profile.htmlへリダイレクト
        nick_name = self.get_argument("nick-name", "")
        introduction = self.get_argument("introduction", "")

        pf = profile.build()
        pf.attr["user_id"] = int(_id)
        pf.attr["nick_name"] = nick_name
        pf.attr["introduction"] = introduction
        pf.save()

        self.render("profile.html",
            user=_signedInUser,
            profile=pf,
            mode="registered",
            errors=[])

class ProfileShowHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # モデルから全てのユーザ情報を取得
        pf = profile.select_by_user_id(int(_id))
        if pf.attr["nick_name"] is None:
            pf.attr["nick_name"] = ""
        if pf.attr["introduction"] is None:
            pf.attr["introduction"] = ""

        # profile.htmlへリダイレクト
        self.render("profile.html",
            user=_signedInUser,
            profile=pf,
            mode="",
            errors=[])

class ProfileShowReadonlyHandler(SigninBaseHandler):
    def get(self, user_id, thread_id):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(user_id)

        # モデルから全てのユーザ情報を取得
        pf = profile.select_by_user_id(user_id)
        if pf.attr["nick_name"] is None:
            pf.attr["nick_name"] = ""
        if pf.attr["introduction"] is None:
            pf.attr["introduction"] = ""

        # profile.htmlへリダイレクト
        self.render("profile.html",
            user=_signedInUser,
            profile=pf,
            mode="readonly",
            thread=thread_id,
            errors=[])