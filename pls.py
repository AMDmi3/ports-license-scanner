#!/usr/bin/env python3
#
# Copyright (c) 2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import os

from pls.database import Database
from pls.path import GetDatabasePath, GetWrkdirprefixPath
from pls.scan import ScanAllPorts, ScanOrigins
from pls.show import ShowAllPorts, ShowOrigins
from pls.verbose import EnableVerbose, VerbosePrint


def Main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose operation')
    parser.set_defaults(mode=None)

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands')

    parser_reset = subparsers.add_parser('reset', help='reset the database')
    parser_reset.set_defaults(mode='reset')

    parser_scan = subparsers.add_parser('scan', help='scan portstree for license information')
    parser_scan.add_argument('-n', '--nomos', default='nomossa', help='path to fossology nomos license scanner')
    parser_scan.add_argument('-p', '--portspath', default='/usr/ports', help='path to FreeBSD ports tree')
    parser_scan.add_argument('-t', '--timeout', type=int, default=600, help='nomos scan timeout in seconds')
    parser_scan.add_argument('origins', metavar='origin', nargs='*', help='port origins to process')
    parser_scan.set_defaults(mode='scan')

    parser_show = subparsers.add_parser('show', help='show license information')
    parser_show.add_argument('origins', metavar='origin', nargs='*', help='port origins to process')
    parser_show.set_defaults(mode='show')

    options = parser.parse_args()

    if not options.mode:
        parser.parse_args(['--help'])
        return 1

    EnableVerbose(options.verbose)

    VerbosePrint('Opening database')

    database = Database(GetDatabasePath())
    os.environ['WRKDIRPREFIX'] = GetWrkdirprefixPath()
    os.environ['BATCH'] = '1'

    if options.mode == 'reset':
        VerbosePrint('Clearing database')
        database.clear()
    elif options.mode == 'scan':
        VerbosePrint('Running scan')
        if options.origins:
            ScanOrigins(database=database, nomos=options.nomos, portspath=options.portspath, timeout=options.timeout, origins=options.origins)
        else:
            ScanAllPorts(database=database, nomos=options.nomos, portspath=options.portspath, timeout=options.timeout)
    elif options.mode == 'show':
        VerbosePrint('Showing results')
        if options.origins:
            ShowOrigins(database=database, origins=options.origins)
        else:
            ShowAllPorts(database=database)

    VerbosePrint('Closing database')

    database.close()

    return 0


if __name__ == '__main__':
    os.sys.exit(Main())
