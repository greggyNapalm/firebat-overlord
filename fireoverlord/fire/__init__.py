# -*- encoding: utf-8 -*-
import flask

fire = flask.Blueprint('fire', __name__,)

from . import views
