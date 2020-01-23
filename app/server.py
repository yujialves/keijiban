#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import sys
from model.thread import thread
from model.user import user
from model.chats import chats
from model.profile import profile
from controller.AuthenticationHandlers import SigninBaseHandler, SigninHandler, SignupHandler, SignoutHandler
from controller.ProfileHandlers import ProfileUpdateHandler, ProfileShowHandler
from controller.ThreadsHandlers import ThreadsHandler, ThreadsCreateHandler
from controller.ChatsHandlers import ChatsShowHandler, ChatsInsertHandler
from controller.ProfileHandlers import ProfileShowHandler, ProfileUpdateHandler, ProfileShowReadonlyHandler
# from controller.ChatsHandler import ChatDeleteHandler, ChatUpdateHandler, ChatShowHandler, ChatsInsertHandler
from controller.WebAPIHandlers import IncomeRankHandler, ExpensesRankHandler, MonthlyReportHandler


class MainHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        # ダッシュボードを表示
        # self.render("dashboard.html", user=_signedInUser)
        self.redirect("/thread")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/signin", SigninHandler),
    (r"/signup", SignupHandler),
    (r"/signout", SignoutHandler),
    (r"/api/incomerank", IncomeRankHandler),    # 摘要別収入ランキング
    (r"/api/expensesrank", ExpensesRankHandler),  # 摘要別支出ランキング
    (r"/api/monthlyreport/([0-9]+)", MonthlyReportHandler),  # 月別日別レポート
    (r"/thread", ThreadsHandler),  # 月別日別レポート
    (r"/thread/new", ThreadsCreateHandler),  # 月別日別レポート
    (r"/chats/([0-9]+)", ChatsShowHandler),  # 月別日別レポート
    (r"/chats/([0-9]+)/insert", ChatsInsertHandler),  # 月別日別レポート
    (r"/profile", ProfileShowHandler),  # 月別日別レポート
    (r"/profile/update", ProfileUpdateHandler),  # 月別日別レポート
    (r"/profile/([0-9]+)/([0-9]+)", ProfileShowReadonlyHandler),  # 月別日別レポート

],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
    # cookieの暗号化キー(システムごとにランダムな文字列を設定する)
    cookie_secret="x-D-#i&0S?R6w9qEsZB8Vpxw@&t+B._$",
)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "migrate":
            thread.migrate()
            user.migrate()
            chats.migrate()
            profile.migrate()
        if args[1] == "db_cleaner":
            thread.db_cleaner()
            user.db_cleaner()
            chats.db_cleaner()
            profile.db_cleaner()
        if args[1] == "help":
            print("usage: python server.py migrate # prepare DB")
            print("usage: python server.py db_cleaner # remove DB")
            print("usage: python server.py # run web server")
    else:
        application.listen(3000, "0.0.0.0")
        tornado.ioloop.IOLoop.instance().start()
