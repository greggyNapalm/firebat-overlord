# -*- encoding: utf-8 -*-
import flask

user = flask.Blueprint('user', __name__,)

from . import views
