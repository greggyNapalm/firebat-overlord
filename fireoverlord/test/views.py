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
