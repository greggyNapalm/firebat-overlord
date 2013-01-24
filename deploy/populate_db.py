#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
firebat-overlord.populate_db
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command line script to create schema in existing postgresql database.
**For initial deployment only**
"""


import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fireoverlord import db
from fireoverlord.models import User, Server, Line, Route, Dc, Test_cfg,\
        Test, Fire, TestStatus, Permission, Token


def main():
    db.create_all()

    # Default test statuses.
    test_statuses = [
        TestStatus('created'),
        TestStatus('started'),
        TestStatus('running'),
        TestStatus('aborted'),
        TestStatus('finished'),
    ]

    for ts in test_statuses:
        db.session.add(ts)

    # At least one admin account at the begining.
    admin = User('admin', 'admin', 'admin', 'admin@localhost.io',
                 password='changeme', is_staff=True, is_active=True,
                 is_superuser=True, is_authenticated=True)

    db.session.add(admin)

    # Not necessary
    servers = [
        Server('localhost', '127.0.0.1', is_test=False),
    ]
    for s in servers:
        db.session.add(s)

    # Dfault permissions for API clients.
    perms = [
        Permission('ro - read only'),
        Permission('rwo - read and write'),
        Permission('rwd - read, write and delete'),
    ]

    for p in perms:
        db.session.add(p)

    # Test API client.
    db.session.commit()
    db.session.add(Token('valera', admin.id, perms[0].id,
                         'test RO token for admin'))

    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    main()
