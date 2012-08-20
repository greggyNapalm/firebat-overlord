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
        return 'JSON body malformed', 400

    if 'cfg' in fire:
        try:
            fb_validate(fire['cfg'], tgt='fire')
        except validictory.validator.ValidationError, e:
            return 'Fire schema malformed: %s' % e, 400

    f = Fire.query.filter_by(id=fire_id).first()
    if not f:
        return 'No such fire with id: %s' % fire['cfg']['id'], 404

    if 'cfg' in fire:
        f.put_cfg(fire['cfg'])
    if 'status' in fire:
        f.status_id = fire['status']
    if 'ended_at' in fire:
        f.ended_at = fire['ended_at']
    db.session.add(f)
    db.session.commit()

    result = {
        'msg': 'fire updated successfully.',
    }
    return jsonify(result), 204
