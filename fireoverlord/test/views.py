# -*- encoding: utf-8 -*-

"""
firebat-overlord.test
~~~~~~~~~~~~~~~~~~~~~

Tests related logic and operations.
"""

from flask import request, jsonify, current_app
import validictory
from firebat.console.helpers import validate as fb_validate
import pprint
pp = pprint.PrettyPrinter(indent=4)

import simplejson as json

from .. import db
from . import test
from ..models import Test, Test_cfg, Fire   
from ..helpers import validate_test

@test.route('/hello', methods=['GET'])
def test_hello():
    return 'Reply to hello'


@test.route('/firebat', methods=['POST', 'PATCH'])
def firebat():
    '''Add or modify firebat test job'''
    test = request.json
    if not test:
        return 'JSON body malformed', 400

    import time
    time.sleep(10)

    try:
        validate_test(test)
    except validictory.validator.ValidationError, e:
        return 'Test schema malformed: %s' % e, 400

    cfg = Test_cfg(json.dumps(test['cfg']))
    db.session.add(cfg)
    db.session.commit()

    if not 'owner' in test['cfg']:
        owner = test['cfg']['uid']
    test = Test(cfg.id, test['status'], owner=owner)
    db.session.add(test)
    db.session.commit()
    fires_ids = test.spread_fires()
    
    result = {
        'test_id': test.id,
        'fires_ids': fires_ids,
    }

    return jsonify(result), 201
#
#
#@test.route('/firebat/<test_id>', methods=['GET'])
#def firebat_c(test_id):
#    '''Get firebat test state by id'''
#    t = Test.query.filter_by(id=test_id).first()
#    if not t:
#        return 'No such test.', 404
#
#    if t.status_id == Status.query.filter_by(name='added').first().id:
#        return 'Test was added, but task scheduling failed. Call support.', 410
#
#    if t.status_id == Status.query.filter_by(name='celery_assigned').\
#                      first().id:
#        r = launch_fire.AsyncResult(t.celery_task_id)
#
#        result = {
#            'status': 'celery_assigned',
#            'ready': r.ready(),
#        }
#
#        if r.ready():
#            try:
#                result['result'] = r.get(timeout=5)
#            except Exception, e:
#                result['result'] = 'failed'
#                result['failed_info'] = 'Celery task fails with: %s' % e
#
#    return jsonify(result)
