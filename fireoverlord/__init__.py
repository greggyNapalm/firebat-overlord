#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
firebat-overlord
~~~~~~~~~~~~~~~~

Describes WSGI application.
"""

import os

from flask import flash, url_for, redirect, Flask, request, session
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView


version_info = (0, 0, 1)
__version__ = ".".join(map(str, version_info))
__path = os.path.dirname(__file__)

app = Flask(__name__)
app.config.from_envvar('FIRE_OVR_CFG')
app.wsgi_app = ProxyFix(app.wsgi_app)  # Fix for old proxyes
db = SQLAlchemy(app)

# Register different 3rd party apps and extensions
from models import User, Server, Fire, Token

# Flask-Admin
def is_admin():
    login = session.get('login', None)
    usr = User.query.filter_by(username=login).first()
    if usr:
        if usr.is_superuser:
            return True
    return False


class MyAdminIndexView(AdminIndexView):
    pass

MyAdminIndexView.is_accessible = staticmethod(is_admin)


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

MyView.is_accessible = staticmethod(is_admin)


class ModelViewRestricted(ModelView):
    pass

ModelViewRestricted.is_accessible = staticmethod(is_admin)

admin = Admin(app, name='Firebat Admin', index_view=MyAdminIndexView())
admin.add_view(MyView(name='Links'))
admin.add_view(ModelViewRestricted(User, db.session))
admin.add_view(ModelViewRestricted(Token, db.session))
admin.add_view(ModelViewRestricted(Server, db.session))
admin.add_view(ModelViewRestricted(Fire, db.session))

# fire-overlord sub apps
from test import test
from user import user

app.register_blueprint(test, url_prefix='/api/v1')
app.register_blueprint(user, url_prefix='/api/v1/user')
