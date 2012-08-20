# -*- encoding: utf-8 -*-

"""
firebat-overlord.models
~~~~~~~~~~~~~~~~~~~~~~~

Objects mapping for whole app
"""

from datetime import datetime
import socket

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
    settings = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    is_authenticated = Column(Boolean, default=False)
    last_login = Column(DateTime)
    date_joined = Column(DateTime)

    def __init__(self, username, first_name, last_name, email, password,
                 is_staff=None, is_active=None, is_superuser=None,
                 is_authenticated=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_staff = is_staff
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_authenticated = is_authenticated

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
    '''Hw or Vm host, can be load generator and load target.'''
    __tablename__ = 'server'
    id = Column(Integer, autoincrement=True, primary_key=True)
    fqdn = Column(String, nullable=False)
    is_test = Column(Boolean, nullable=False)
    date_added = Column(DateTime)
    description = Column(String)
    last_ip = Column(postgresql.INET, nullable=False)
    last_dc = Column(Integer, default=0)
    is_spec_tank = Column(Boolean, default=False)
    is_reachable = Column(Boolean, default=False)
    is_tank = Column(Boolean, default=False)
    line = Column(Integer, default=None)
    host_serv = Column(Integer, default=None)

    def __init__(self, fqdn, last_ip, is_test=False,):
        self.fqdn = fqdn
        self.last_ip = last_ip
        self.is_test = is_test
        self.date_added = datetime.utcnow()

    @classmethod
    def get_or_create(cls, last_ip=None, fqdn=None, lookup_to=5):
        if fqdn:
            s = cls.query.filter_by(fqdn=fqdn).first()
        elif last_ip:
            s = cls.query.filter_by(last_ip=last_ip).first()
        else:
            raise ValueError(
                    'At least one of kwargs: last_ip or fqdn shud present')
        if not s:
            invalid_names = ['any.yandex.ru',]
            socket.setdefaulttimeout(lookup_to)
            if fqdn:
                last_ip = socket.gethostbyname(fqdn)

            if not fqdn and last_ip:
                fqdn = socket.gethostbyaddr(last_ip)[0]
                if fqdn in invalid_names:
                    raise ValueError('Can\'t resolve fqdn by last_ip: %s' % fqdn)
            s = cls(fqdn, last_ip)
            db.session.add(s)
            db.session.commit()
        return s


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


class TestStatus(db.Model):
    '''Test status.'''
    __tablename__ = 'test_status'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    def __init__(self, name):
        self.name = name


class Test(db.Model):
    '''Test'''
    __tablename__ = 'test'
    id = Column(Integer, unique=True, primary_key=True)
    status_id = Column(Integer, ForeignKey('test_status.id'), nullable=False)
    cfg_id = Column(Integer, ForeignKey('test_cfg.id'), nullable=False)
    owner = Column(Integer, ForeignKey('user.id'))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    def __init__(self, cfg_id, status_id, owner=None, started_at=None):
        self.cfg_id = cfg_id
        self.status_id = status_id
        if owner:
            self.owner = User.query.filter_by(username=owner).first()
        if not self.owner:
            self.owner = 1
        if not started_at:
            self.started_at = datetime.utcnow()

    def spread_fires(self):
        '''Create fires this test belong by test_cfg data.'''
        cfg_json = Test_cfg.query.filter_by(id=self.cfg_id).first().cfg
        cfg = json.loads(cfg_json)
        host_from = Server.get_or_create(fqdn=cfg['src_host'])
        fiers = []
        status_created_id = TestStatus.query.filter_by(name='created').first().id
        for f in cfg['fire']:
            host_to = Server.get_or_create(last_ip=f['addr'].split(':')[0])
            f = Fire(self.id, status_created_id, host_from.id, host_to.id)
            db.session.add(f)
            fiers.append(f)
        db.session.commit()
        return [f.id for f in fiers]


class Fire(db.Model):
    '''Test part, one Phantom job.'''
    __tablename__ = 'fire'
    id = Column(Integer, unique=True, primary_key=True)
    status_id = Column(Integer, ForeignKey('test_status.id'), nullable=False)
    test_id = Column(Integer, ForeignKey('test.id'), nullable=False)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    host_from = Column(Integer, ForeignKey('server.id'), nullable=False)
    host_to = Column(Integer, ForeignKey('server.id'), nullable=False)
    cfg = Column(String)
    result = Column(String)

    def __init__(self, test_id, status_id, host_from, host_to, started_at=None):
        self.test_id = test_id
        self.status_id = status_id
        self.host_from = host_from
        self.host_to = host_to
        if not started_at:
            self.started_at = datetime.utcnow()

    def put_cfg(self, fire_cfg):
        '''Create or update fire configuration.'''
        if self.cfg:
            self.cfg = json.dumps(json.loads(self.cfg).update(fire_cfg))
        else:
            self.cfg = json.dumps(fire_cfg)
