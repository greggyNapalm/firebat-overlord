#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
firebat-overlord.models
~~~~~~~~~~~~~~~~~~~~~~~

Objects mapping for whole app
"""

from datetime import datetime

from sqlalchemy import *
from . import db


class Status(db.Model):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Status %r>' % (self.name)


class Test(db.Model):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    celery_task_id = Column(String)
    celery_out = Column(String)
    status_id = Column(Integer, ForeignKey('status.id'))
    added_at = Column(DateTime)

    def __init__(self, id=None, name=None, status_id=None):
        self.id = id
        self.name = name
        self.status_id = status_id
        self.added_at = datetime.utcnow()

    def __repr__(self):
        return '<Test %r>' % (self.id)
