# -*- encoding: utf-8 -*-

"""
firebat-overlord.user
~~~~~~~~~~~~~~~~~~~~~

Application users related logic and operations.
"""


#from datetime import datetime
#import pprint
#pp = pprint.PrettyPrinter(indent=4)
import time

from flask import request, jsonify, session

from .. import db
from . import user 
from ..models import User
from ..helpers import auth_required 

@user.route('/settings', methods=['GET'])
@auth_required
def settings():
    if request.method == 'GET':
        result = {}
        usr = User.query.filter_by(username=session['login']).first()
        if usr and usr.is_superuser:
            result['is_superuser'] = usr.is_superuser
        result['login'] = session['login']
        return jsonify(result), 200
