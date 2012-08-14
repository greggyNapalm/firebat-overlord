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
        Test, Fire, TestStatus


def main():
    db.create_all()
    test_statuses = [
        TestStatus('created'),
        TestStatus('started'),
        TestStatus('running'),
        TestStatus('aborted'),
        TestStatus('finished'),
    ]

    for ts in test_statuses:
        db.session.add(ts)

    admin = User('admin', 'admin', 'admin', 'admin@localhost.io', 'changeme',
                 is_staff=True, is_active=True, is_superuser=True,
                 is_authenticated=True)

    db.session.add(admin)

    servers = [
        Server('localhost', '127.0.0.1', is_test=False),
        Server('lucid.t80.tanks.yandex.net', '84.201.161.219', is_test=False),
    ]
    for s in servers:
        db.session.add(s)

    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    main()
