"""A self-daemonizing celeryd."""
import sys

from flaskext.script import Command, Option

import daemon
from celery.bin.celeryd import run_worker, OPTION_LIST, parse_options

# Convert optparse options into argparse options.
opts = [Option(*(o._short_opts + o._long_opts), help=o.help)
        for o in OPTION_LIST]
opts.append(Option('-d', '--daemonize', action='store_true',
                   help="Oh god it's a daemon."))


class celeryd(Command):
    option_list = opts

    def run(self, **opts):
        if opts['daemonize']:
            for opt in ('-d', '--daemonize'):
                if opt in sys.argv:
                    sys.argv.remove(opt)
            with daemon.DaemonContext():
                self.run_celery()
        self.run_celery()

    def run_celery(self):
        # Use celeryd's optparser.
        options = parse_options(sys.argv[2:])
        run_worker(**vars(options))
