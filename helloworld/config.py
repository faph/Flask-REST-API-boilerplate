# -*- coding: utf-8 -*-
import os

here = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'app.db')

AUTH_CLIENT_ID = os.environ['AUTH_CLIENT_ID']
AUTH_CLIENT_SECRET = os.environ['AUTH_CLIENT_SECRET']