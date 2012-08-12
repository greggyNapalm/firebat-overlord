# -*- encoding: utf-8 -*-
import flask

test = flask.Blueprint('test', __name__,)

from . import views
