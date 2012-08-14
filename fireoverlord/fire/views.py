# -*- encoding: utf-8 -*-

"""
firebat-overlord.fire
~~~~~~~~~~~~~~~~~~~~~

Fire related logic and operations.
"""

from flask import request, jsonify, current_app
import validictory
from firebat.console.helpers import validate as fb_validate
import pprint
pp = pprint.PrettyPrinter(indent=4)

import simplejson as json

from .. import db
from . import fire 
from ..models import Test, Test_cfg, Fire   
from ..helpers import validate_fire


@fire.route('/hello', methods=['GET'])
def fire_hello():
    return 'Hello from fire view'


@fire.route('/<fire_id>', methods=['PUT', 'PATCH'])
def edit_fire(fire_id):
    '''Modify existing fire entrie.'''
    fire = request.json
    #fire_cfg = request.json
    if not fire:
        print 'JSON body malformed'
        return 'JSON body malformed', 400

    if 'cfg' in fire:
        try:
            fb_validate(fire['cfg'], tgt='fire')
            #validate_fire(fire)
        except validictory.validator.ValidationError, e:
            print  'Fire schema malformed: %s', e
            return 'Fire schema malformed: %s' % e, 400

    f = Fire.query.filter_by(id=fire_id).first()
    if not f:
        return 'No such fire with id: %s' % fire['cfg']['id'], 404

    #ended_at
    if 'cfg' in fire:
        f.put_cfg(fire['cfg'])
    if 'status' in fire:
        f.status_id = fire['status']
    if 'ended_at' in fire:
        f.ended_at = fire['ended_at']
    db.session.add(f)
    db.session.commit()

    #cfg = Test_cfg(json.dumps(test_cfg))
    #db.session.add(cfg)
    #db.session.commit()

    #if not 'owner' in test_cfg:
    #    owner = test_cfg['uid']
    #test = Test(cfg.id, owner=owner)
    #db.session.add(test)
    #db.session.commit()
    #fires_ids = test.spread_fires()
    #
    #result = {
    #    'test_id': test.id,
    #    'fires_ids': fires_ids,
    #}
    result = {
        'msg': 'fire updated successfully.',
    }
    return jsonify(result), 204
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
