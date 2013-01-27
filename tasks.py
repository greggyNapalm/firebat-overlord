# -*- encoding: utf-8 -*-

"""
tankmanager.helpers
~~~~~~~~~~~~~~~~~~

Common for whole app functions.
"""

from celery import Celery
import requests

import celeryconfig
from fireoverlord import db
from fireoverlord.models import User
from fireoverlord.helpers import get_app_cfg
from fireoverlord.ya.helpers import fetch_usr_data

celery = Celery()
celery.config_from_object(celeryconfig)


@celery.task
def add(x, y):
        #'a' + 4
        #assert False
        return x + y


@celery.task
def add1(x, y):
    z = 0
    for i in xrange(10 ** 10):
        z = x + y
    return z


@celery.task
def update_users_details():
    '''Get users details from 3rd side and push them to db.
    '''
    app_cfg = get_app_cfg()
    trans_tbl = {
        'work_email': 'email',
    }

    def trans_keys():
        for key in usr_details.keys():
            if key in trans_tbl:
                usr_details[trans_tbl[key]] = usr_details[key]
                del usr_details[key]

    for usr in User.query.all():
        try:
            usr_details = fetch_usr_data(usr.username, cfg=app_cfg)
            trans_keys()
            usr.update(**usr_details)
            db.session.add(usr)
        except requests.HTTPError:
            pass
    db.session.commit()
    return None
