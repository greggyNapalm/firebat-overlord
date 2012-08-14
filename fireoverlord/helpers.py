#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
firebat-overlord.helpers
~~~~~~~~~~~~~~~~~~~~~~~~

Common for whole app useful functions.
"""
import validictory

from firebat.console.helpers import fire_cfg_schema, test_cfg_schema

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
