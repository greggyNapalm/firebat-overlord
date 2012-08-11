#!/usr/bin/env python

"""
firebat-overlord.populate_db
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command line script to create schema in existing postgresql database.
**For initial deployment only**
"""

from fireoverlord import db
from fireoverlord.models import Status, Test 


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
