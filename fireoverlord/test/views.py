# -*- encoding: utf-8 -*-

"""
firebat-overlord.test
~~~~~~~~~~~~~~~~~~~~~

Tests related logic and operations.
"""


from datetime import datetime
import string
import pprint
pp = pprint.PrettyPrinter(indent=4)

from flask import request, jsonify, current_app, session
import simplejson as json
import validictory

from .. import db
from . import test
from ..models import User, Test, Test_cfg, TestStatus, Fire   
from ..helpers import validate_test, validate_fire, auth_required,\
    paginate_query 

DEFAULT_TESTS_PER_PAGE = 5

@test.route('/ping', methods=['GET'])
@auth_required
def test_ping():
    return 'Firebat Overlord REST API', 200


@test.route('/test', methods=['GET', 'POST', 'PATCH'])
@auth_required
def test_firebat():
    '''get, add or modify firebat test'''
    def validate_params():
        page = request.args.get('page')
        if page:
            if not ((page.isdigit()) and (int(page) >= 0)):
                raise ValueError('*page* parameter error')
        
        per_page = request.args.get('per_page')
        if per_page:
            if not (per_page.isdigit() and (per_page > 0)):
                raise ValueError('*per_page* parameter error')

    if request.method == 'GET':
        try:
            validate_params()
        except ValueError as e:
            msg = {
                'msg': 'Validation Failed',
                'error': str(e),
            }
            return jsonify(msg), 422

        result = {
            'tests': [],
        }

        q = db.session.query(Test, User.username,
                Test_cfg.cfg).join(User).join(Test_cfg)

        owner = request.args.get('owner', None)
        if owner:
            q = q.filter(User.username == owner)

        ids = request.args.get('id', None)
        if ids:
            ids = ids.split(',')
            q = q.filter(Test.id.in_(ids))

        link_header, q_slice = paginate_query(request, q, DEFAULT_TESTS_PER_PAGE) 
        
        if not q_slice:
            result['tests'] = []
        else:
            q = q.limit(q_slice['limit']).offset(q_slice['offset'])
            for row in q:
                result['tests'].append(dict_from_test_query2(row))

        resp = jsonify(result)
        resp.status_code = 200
        if link_header:
            resp.headers['Link'] = link_header
        return resp

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
            return 'Can\'t update test. Call support', 500

        result = {
            'msg': 'test updated successfully.',
        }
        return jsonify(result), 204

        
@test.route('/fire', methods=['PATCH'])
@auth_required
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

def dict_from_test_query1(row):
    ''' Compile *Test* query join data to one dict.
    Args:
        row: named tuple, qury result.
    Returns:
        result: dict, ready to jsonify.
    '''
    result = {}
    print row.Test.owner
    #for key in Test.__table__.columns:
    #    val = getattr(row.Test, key.name)
    #    if isinstance(val, datetime):
    #        val = val.isoformat()
    #    result[key.name] = val

    #result['cfg'] = json.loads(row.cfg)
    result['id'] = row.Test.id
    result['status_name'] = row.status_name

    return result


def dict_from_test_query2(row):
    ''' Compile *Test* query joins data to one dict.
    Args:
        row: named tuple, qury result.
    Returns:
        result: dict, ready to jsonify.
    '''
    #print json.loads(row[2])['fire']
    tags = set()
    for fire in json.loads(row[2])['fire']:
        for tag in fire['tag']:
            tags.add(tag)
    #print tags
    result = {}
    attrs = [
        'id',
        'started_at',
        'ended_at',
        'status_id',
    ]

    for attr in attrs:
        val = getattr(row[0], attr)
        if isinstance(val, datetime):
            val = val.isoformat()
        result[attr] = val

    result['owner'] = row[1]

    cfg = json.loads(row[2])
    result['title'] = cfg['title']

    tags = set()
    for fire in cfg['fire']:
        for tag in fire['tag']:
            tags.add(tag)
    result['tags'] = list(tags)
    #result['title'] = row[2]['title']

    return result
