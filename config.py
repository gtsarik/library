# -*- coding: utf8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'library_user_request_safe'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'library.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
