# -*- encoding: utf-8 -*-

"""
firebat-overlord.test
~~~~~~~~~~~~~~~~~~~~~

Tests related logic and operations.
"""


from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)

from flask import request, jsonify, current_app
import simplejson as json
import validictory

from .. import db
from . import test
from ..models import User, Test, Test_cfg, TestStatus, Fire   
from ..helpers import validate_test, validate_fire

@test.route('/ping', methods=['GET'])
def test_ping():
    return 'Firebat Overlord REST API', 204


@test.route('/test', methods=['GET', 'POST', 'PATCH'])
def test_firebat():
    '''get, add or modify firebat test'''
    if request.method == 'GET':
        result = {
            'tests': [],
        }
        q = db.session.query(Test,
                             Test_cfg.cfg.label('cfg'),
                             TestStatus.name.label('status_name'))

        status = request.args.get('status', None)
        if status:
            q = q.join(TestStatus).join(Test_cfg).\
                filter(TestStatus.name == status)

        owner = request.args.get('owner', None)
        if owner:
            q = q.join(User).\
                filter(User.username == owner)

        ids = request.args.get('id', None)
        if ids:
            ids = ids.split(',')
            q = q.filter(Test.id.in_(ids))

        for row in q:
            result['tests'].append(dict_from_test_query(row))

        return jsonify(result), 200

    test = request.json
    if not test:
        return 'JSON body malformed', 400

    if request.method == 'POST':
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

    if request.method == 'PATCH':
        t = Test.query.filter_by(id=test['id']).first()
        if not t:
            return 'No such test with id: %s' % test['id'], 404
        try:
            t.update(test)
        except Exception, e:
            print e
            return 'Can\'t update test. Call support', 500

        result = {
            'msg': 'test updated successfully.',
        }
        return jsonify(result), 204

        
@test.route('/fire', methods=['PATCH'])
def fire():
    '''Modify fire'''
    fire = request.json
    if not fire:
        return 'JSON body malformed', 400

    #try:
    #    validate_fire(test)
    #except validictory.validator.ValidationError, e:
    #    return 'Test schema malformed: %s' % e, 400

    f = Fire.query.filter_by(id=fire['id']).first()
    if not f:
        return 'No such fire with id: %s' % fire['id'], 404

    try:
        f.update(fire)
    except Exception, e:
        print e
        return 'Can\'t update fire. Call support', 500

    result = {
        'msg': 'fire updated successfully.',
    }
    return jsonify(result), 204

def dict_from_test_query(row):
    ''' Compile *Test* query join data to one dict.
    Args:
        row: named tuple, qury result.
    Returns:
        result: dict, ready to jsonify.
    '''
    result = {}
    for key in Test.__table__.columns:
        val = getattr(row.Test, key.name)
        if isinstance(val, datetime):
            val = val.isoformat()
        result[key.name] = val

    result['cfg'] = json.loads(row.cfg)
    result['status_name'] = row.status_name

    return result

