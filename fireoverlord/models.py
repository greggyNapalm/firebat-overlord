# -*- encoding: utf-8 -*-

"""
firebat-overlord.models
~~~~~~~~~~~~~~~~~~~~~~~

Objects mapping for whole app
"""

from datetime import datetime

from sqlalchemy import *
from sqlalchemy.dialects import postgresql
import simplejson as json

from . import db


class User(db.Model):
    '''Application user'''
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    is_authenticated = Column(Boolean, default=False)
    last_login = Column(DateTime)
    date_joined = Column(DateTime)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<User %s %s>' % (self.id, self.email)

    def check_password(self, password):
        return self.password == password

    def is_active(self):
        return self.is_active

    def get_id(self):
        return str(self.id).decode('utf-8')

    def is_authenticated(self):
        return self.is_authenticated

    def is_anonymous(self):
        return False


class Server(db.Model):
    '''Host which can be load generator and load target.'''
    __tablename__ = 'server'
    id = Column(Integer, autoincrement=True, primary_key=True)
    fqdn = Column(String, nullable=False)
    is_test = Column(Boolean, nullable=False)
    date_added = Column(DateTime)
    description = Column(String)
    last_ip = Column(postgresql.INET)
    last_dc = Column(Integer, default=0)
    is_spec_tank = Column(Boolean, default=False)
    is_reachable = Column(Boolean, default=False)
    is_tank = Column(Boolean, default=False)
    line = Column(Integer, default=None)
    host_serv = Column(Integer, default=None)


class Dc(db.Model):
    '''Datacenter'''
    __tablename__ = 'dc'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, nullable=False)


class Line(db.Model):
    '''Datacenter part, separated from the rest by router.'''
    __tablename__ = 'line'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    dc_id = Column(Integer, ForeignKey('dc.id'), nullable=False)


class Route(db.Model):
    '''Network route between two hosts.'''
    __tablename__ = 'route'
    host_from = Column(Integer, ForeignKey('server.id'), nullable=False)
    host_to = Column(Integer, ForeignKey('server.id'), nullable=False)
    hops_num = Column(Integer, default=None)
    line = Column(String, nullable=False)
    __table_args__ = (PrimaryKeyConstraint(host_from, host_to),)


class Test_cfg(db.Model):
    '''Test configuration, can be used multiple times.'''
    __tablename__ = 'test_cfg'
    id = Column(Integer, unique=True, primary_key=True)
    cfg = Column(String)

    def __init__(self, cfg):
        self.cfg = cfg


class Test(db.Model):
    '''Test'''
    __tablename__ = 'test'
    id = Column(Integer, unique=True, primary_key=True)
    cfg_id = Column(Integer, ForeignKey('test_cfg.id'), nullable=False)
    owner = Column(Integer, ForeignKey('user.id'))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    def __init__(self, cfg_id, owner=None, started_at=None):
        self.cfg_id = cfg_id
        if owner:
            self.owner = owner
        if not started_at:
            self.started_at = datetime.utcnow()

    def spread_fires(self):
        cfg_json = Test_cfg.query.filter_by(id=self.cfg_id).first().cfg
        cfg = json.loads(cfg_json)
        host_from = Server.query.filter_by(fqdn=cfg['src_host']).first()
        host_to = Server.query.filter_by(fqdn=cfg['addr'].split(':')[0]).first()
        for f in cfg['fire']:
            db.session.add(Fire(self.id, host_from, host_to))
        db.session.commit()



class Fire(db.Model):
    '''Test part, one Phantom job.'''
    __tablename__ = 'fire'
    id = Column(Integer, unique=True, primary_key=True)
    test_id = Column(Integer, ForeignKey('test.id'), nullable=False)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    host_from = Column(Integer, ForeignKey('server.id'), nullable=False)
    host_to = Column(Integer, ForeignKey('server.id'), nullable=False)

    def __init__(self, test_id, host_from, host_to, started_at=None):
        self.test_id = test_id
        self.host_from = host_from
        self.host_to = host_to
        if not started_at:
            self.started_at = datetime.utcnow()
