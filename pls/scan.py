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
import os
import re
import subprocess

from pls.verbose import VerbosePrint


def ScanPort(database, nomos, portspath, origin):
    VerbosePrint('  Processing port {}'.format(origin))

    cursor = database.cursor()
    cursor.execute('SELECT COUNT(*) FROM ports WHERE origin=?', (origin,))
    if cursor.fetchone()[0] == 1:
        VerbosePrint('    Already processed, skipping')
        return

    portpath = os.path.join(portspath, origin)
    VerbosePrint('    Getting port information')
    varslist = subprocess.run(['make', '-C', portpath, '-V', 'LICENSE', '-V', 'WRKDIR'], check=True, encoding='utf-8', stdout=subprocess.PIPE)

    license, wrkdir = varslist.stdout.split('\n')[:2]
    port_licenses = license.split()
    file_licenses = {}

    try:
        VerbosePrint('    Extracting port')
        subprocess.run(['make', '-C', portpath, 'clean', 'extract'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except KeyboardInterrupt:
        raise
    except:
        VerbosePrint('      Failed to extract, skipping')
        return

    VerbosePrint('    Running nomos')
    nomosoutput = subprocess.run([nomos, '-l', '-d', wrkdir], check=True, encoding='utf-8', stdout=subprocess.PIPE)
    lines = nomosoutput.stdout.split('\n')
    for line in lines:
        if not line:
            continue

        match = re.match('File (.*) contains license\(s\) (.*)$', line)
        if match:
            nomos_file = match.group(1)
            if wrkdir not in nomos_file:
                VerbosePrint('      Unexpected path outside wrkdir: {}'.format(nomos_file))
                continue

            nomos_file = nomos_file[len(wrkdir) + 1:]
            nomos_licenses = match.group(2).split()

            if nomos_licenses == ['No_license_found']:
                continue

            for license in nomos_licenses:
                file_licenses.setdefault(license, []).append(nomos_file)

        else:
            VerbosePrint('      Unexpected output from nomos: {}'.format(line))

    VerbosePrint('    Cleaning up')
    subprocess.run(['make', '-C', portpath, 'clean'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    VerbosePrint('    Saving to database')

    database.cursor().execute('INSERT INTO ports (origin, port_licenses, file_licenses) VALUES(?, ?, ?)', (origin, json.dumps(port_licenses), json.dumps(file_licenses)))

    database.commit()

    VerbosePrint('    Done')


def ScanPorts(database, nomos, portspath, origins=None):
    if origins:
        for origin in origins:
            ScanPort(database=database, nomos=nomos, portspath=portspath, origin=origin)
        return

    VerbosePrint('Getting list of categories')
    catlist = subprocess.run(['make', '-C', portspath, '-V', 'SUBDIR'], check=True, encoding='utf-8', stdout=subprocess.PIPE)

    for category in catlist.stdout.split():
        VerbosePrint('Processing category {}'.format(category))

        portlist = subprocess.run(['make', '-C', os.path.join(portspath, category), '-V', 'SUBDIR'], check=True, encoding='utf-8', stdout=subprocess.PIPE)

        for port in portlist.stdout.split():
            ScanPort(database, nomos, portspath, os.path.join(category, port))
