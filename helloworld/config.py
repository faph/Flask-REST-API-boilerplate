# -*- coding: utf-8 -*-
import os

here = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'app.db')
