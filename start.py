#!/usr/bin/env python
#encoding=utf-8
import os

from shireweb import ShireWeb

if __name__ == "__main__":
    routes = [
        (r'/', 'controller.HomeHandler'),
        (r'/users/?', 'handlers.UserListHandler'),
        (r'/user/?(\w*)', 'handlers.UserHandler'),
        (r'/account', 'handlers.AccountHandler'),

        (r'/_', 'controller.AdminHandler'),
        (r'/_/(.*)', 'controller.PageEditHandler'),

        (r'/signin', 'handlers.SigninHandler'),
        (r'/signup', 'handlers.SignupHandler'),
        (r'/signout', 'handlers.SignoutHandler'),

        (r'/paper/(.*)', 'controller.PageHandler'),
        ]
    template_path = os.path.abspath(__file__ + '/../templates')
    server = ShireWeb(routes, template_path)
    server.run()
