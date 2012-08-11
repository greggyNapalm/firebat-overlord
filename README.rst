firebat-overlord
================

Netwrok application with manages all test tasks, store results and display trough Web UI.

Documentation
-------------

Coming soon

Requirements
------------

* GNU Linux
* Python >= 2.7 (Not Python3)

Installation
------------

Use pip and `vurtualev/virtualenvwrapper <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_

Stable version:

::

    Coming soon

Development version:

::

    $ git clone git://github.com/greggyNapalm/firebat-overlord.git; cd firebat-overlord
    $ pip install -r requirements-dev.txt
    $ cp -p firebat-overlord.default.cfg firebat-overlord.local.cfg
    $ export FIRE_OVR_CFG=`readlink -e firebat-overlord.local.cfg`
    $ ./run.py

or

::

    pip install -e git+git://github.com/greggyNapalm/firebat-overlord.git#egg=firebat-overlord


Issues
------

Find a bug? Want a feature? Submit an `here <https://github.com/greggyNapalm/firebat-manager/issues>`_. Patches welcome!

License
-------
BSD `Read more <http://opensource.org/licenses/BSD-3-Clause>`_
