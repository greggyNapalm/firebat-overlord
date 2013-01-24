#!/usr/bin/env python

"""
firebat-overlord.dev-run
~~~~~~~~~~~~~~~~~~~~~~~~

Launch single instance of app with debug and autoreload on changes.
**For development only.**
"""

import sys

from werkzeug.contrib.profiler import ProfilerMiddleware
from werkzeug.contrib import profiler

from fireoverlord import app


def main():
    host, port = '0.0.0.0', 8080

    if len(sys.argv) == 2:
        port = sys.argv[1]

        if ':' in port:
            host, port = port.split(':')

        port = int(port)

    
    app.run(debug=True, host=host, port=port)
    #action_profile = profiler.make_action(app)

if __name__ == '__main__':
    main()
