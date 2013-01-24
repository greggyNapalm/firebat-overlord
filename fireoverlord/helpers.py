#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
firebat-overlord.helpers
~~~~~~~~~~~~~~~~~~~~~~~~

Common for whole app useful functions.
"""
import os
import imp
import math
import copy
from functools import wraps
import urllib
import pprint
pp = pprint.PrettyPrinter(indent=4)

import validictory
from flask import request, Response, session

from firebat.console.helpers import fire_cfg_schema, test_cfg_schema
from models import User, Token
from ya.helpers import auth as external_auth


def validate_fire(fire_sample):
    fire_schema = { 
        'type': 'object',
        'properties': {
            'cfg': {
                'type': fire_cfg_schema,
                'required': False,
            }
        }
    }
    validictory.validate(fire_sample, fire_schema)
    return True

def validate_test(test_sample):
    test_schema = { 
        'type': 'object',
        'properties': {
            'cfg': {
                'type': test_cfg_schema,
                'required': False,
            }
        }
    }
    validictory.validate(test_sample, test_schema)
    return True


def auth_required(f):
    ''' This decorator can be used on any view which should only be visited by
        authenticated clients. Two type of auth supported:
        * external by auth service provider.
        * internal by tokens(HTTP request param).
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        login = external_auth(request)
        if login:
            User.create_if_not_exists(login)
            session['login'] = login
            return f(*args, **kwargs)

        token = request.args.get('token', None)
        if token and Token.query.filter_by(value=token).first():
            return f(*args, **kwargs)

        return 'Not authenticated', 401
    return decorated


def get_app_cfg(envvar='FIRE_OVR_CFG'):
    cfg = {}
    cfg_path = os.environ[envvar]
    d = imp.new_module('app_config')
    d.__file__ = cfg_path
    execfile(cfg_path, d.__dict__)
    for key in dir(d):
        if key.isupper():
            cfg[key] = getattr(d, key)
    return cfg 


def paginate_query(request, query, def_per_page):
    def build_link_header():
        link = []
        qs = request.url.split('?')[0]
        args_orig = dict(request.args.items())
        for key, val in result.iteritems():
            if val:
                args = copy.deepcopy(args_orig)
                args.update({'page': val})
                data = {
                    'qs': qs,
                    'args': urllib.urlencode(args),
                    'rel': key,
                }
                link.append('<{qs}?{args}>; rel="{rel}"'.format(**data))
        
        return (', ').join(link)

    result = {}
    idxs = []
    cnt = query.count()
    if cnt == 0:
        return None

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', def_per_page))
    per_page = min(per_page, def_per_page)

    last_page = int(math.ceil(float(cnt) / per_page))
    result.update({'last': last_page})

    query_slice = {
        'limit': per_page,
        'offset': per_page * (page - 1),
    }

    if (page > last_page):
        return None, None
    elif (page == last_page):
        result.update({
            'next': None,
        })
    else:
        result.update({
            'next': int(page) + 1,
        })

    if (page == 1):
        result.update({
            'prev': None,
        })
        query_slice['offset'] = None
    else:
        result.update({
            'prev': int(page) - 1,
        })

    return build_link_header(), query_slice
