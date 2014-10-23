#!/usr/bin/env python
#fileencoding=utf-8

import logging
from tornado.options import define

def define_app_options():
    define('site_name', default='First Blog')

    define('debug', default=True)
    define('log_level', default=logging.INFO)
    define('cookie_secret', default='Overide this.')

    define('mongodb_host', default="127.0.0.1")
    define('mongodb_port', default=27017)
    define('mongodb_name', default="firstblog")

    define('port', default=8004)

    define('img_prefix', '/upload/')
    define('img_store_path', 'upload/')

    define('smtp_host', 'smtp.xx.com')
    define('smtp_username', 'user@domain')
    define('smtp_password', 'idontknow')
    define('smtp_port', 465)


    try:
        import local_settings
    except ImportError:
        pass
