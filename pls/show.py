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

import json


def FormatLicenses(licenses):
    if not licenses:
        return 'NONE'

    return '"{}"'.format(' '.join(sorted(list(set(licenses)))))


def ShowPort(origin, port_licenses, file_licenses):
    portlic = FormatLicenses(port_licenses)
    srclic = FormatLicenses(file_licenses.keys())

    print('{}: port: {}, sources: {}'.format(origin, portlic, srclic))

    if portlic != srclic:
        for license, files in sorted(file_licenses.items()):
            print('  {}'.format(license))
            for file_ in sorted(files):
                print('    {}'.format(file_))


def ShowOrigins(database, origins):
    for origin in origins:
        row = database.cursor().execute('SELECT origin, port_licenses, file_licenses FROM ports WHERE origin=?', (origin,)).fetchone()
        ShowPort(row[0], json.loads(row[1]), json.loads(row[2]))


def ShowAllPorts(database):
    for row in database.cursor().execute('SELECT origin, port_licenses, file_licenses FROM ports'):
        ShowPort(row[0], json.loads(row[1]), json.loads(row[2]))
