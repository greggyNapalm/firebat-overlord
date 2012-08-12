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

from .. import db
from . import test
from ..models import Test, Test_cfg, Fire   


@test.route('/hello', methods=['GET'])
def test_hello():
    return 'Reply to hello'


@test.route('/firebat', methods=['POST'])
def firebat():
    '''Add new firebat test job'''
    test_cfg = request.json
    if not test_cfg:
        return 'JSON body malformed', 400

    #try:
    #    test_id = int(test['id'])
    #except KeyError:
    #    return 'Attribute *id* in JSON document is necessary', 400

    #if Test.query.filter_by(id=test_id).first():
    #    return 'Test with id=%s allready exist' % test_id, 400

    try:
        fb_validate(test_cfg)
    except validictory.validator.ValidationError, e:
        return 'Test schema malformed: %s' % e, 400

    cfg = Test_cfg(test_cfg)
    test = Test(cfg.id)

    db.session.add(t)
    db.session.commit()

    #task = add.delay(4, 4)
    base_path = current_app.config['TEST_BASE_PATH']
    armorer_api_url = current_app.config['ARMORER_API_URL']
    logs_path = current_app.config['TEST_LOGS_PATH']
    task = launch_fire.delay(test_id, test, base_path,
                             armorer_api_url=armorer_api_url,
                             logs_path=logs_path)

    t.celery_task_id = task.id
    t.status_id = Status.query.filter_by(name='celery_assigned').first().id
    db.session.commit()

    return 'Accepted', 201
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
