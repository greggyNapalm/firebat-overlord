#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
firebat-overlord
~~~~~~~~~~~~~~~~

Describes WSGI application.
"""

import os

from flask import flash, url_for, render_template, redirect, Flask, request
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required,\
        logout_user, current_user
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView


version_info = (0, 0, 1)
__version__ = ".".join(map(str, version_info))
__path = os.path.dirname(__file__)

app = Flask(__name__)
app.config.from_envvar('FIRE_OVR_CFG')
app.wsgi_app = ProxyFix(app.wsgi_app)  # Fix for old proxyes
db = SQLAlchemy(app)

# Register different apps and extensions
from models import User
from forms import LoginForm

# Flask-Login
login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=int(userid)).first()


@app.route("/login", methods=["GET", "POST"])
def login_in():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# Flask-Admin
def admin_only():
    try:
        is_super = current_user.is_superuser
    except AttributeError:
        return False
    return current_user.is_authenticated()


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        is_allowed = admin_only()
        return is_allowed


class MyView(BaseView):
    def is_accessible(self):
        is_allowed = admin_only()
        return is_allowed

    @expose('/')
    def index(self):
        return self.render('index.html')


class ModelViewRestricted(ModelView):
    def is_accessible(self):
        is_allowed = admin_only()
        return is_allowed


admin = Admin(app, name='Firebat Admin', index_view=MyAdminIndexView())
admin.add_view(MyView(name='Hello'))
admin.add_view(ModelViewRestricted(User, db.session))


@app.route('/', methods=['GET'])
@login_required
def index():
    return 'Hello Worlds -->!'

#from status import status
from test import test
#app.register_blueprint(status, url_prefix='/v1/status')
app.register_blueprint(test, url_prefix='/v1/test')
