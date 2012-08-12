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
        Test, Fire


def main():
    db.create_all()
    #statuses = [
    #    Status('added'),
    #    Status('celery_assigned'),
    #    Status('working'),
    #    Status('finishing'),
    #    Status('ended'),
    #    Status('failed'),
    #]

    #for s in statuses:
    #    db.session.add(s)

    db.session.commit()

if __name__ == '__main__':
    main()
