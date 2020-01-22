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
        _nick_name = self.get_argument("nick-name", None)
        _introduction = self.get_argument("introduction", None)
        introduction = []
        nick_name = []
        if _introduction is not None: introduction.append(_introduction)
        if _nick_name is not None: nick_name.append(_nick_name)

        self.render("cashbooks.html",
            user=_signedInUser,
            nick_name=nick_name,
            introduction=introduction,
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

        # profile.htmlへリダイレクト
        self.render("profile.html",
            user=_signedInUser,
            profile=pf,
            errors=[])