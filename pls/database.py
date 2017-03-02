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

import os
import sqlite3


class Database:
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.database = sqlite3.connect(path)

        self.database.cursor().execute('''
            CREATE TABLE IF NOT EXISTS ports (
                origin text,
                port_licenses text,
                file_licenses text
            )
        ''')

        self.database.cursor().execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS ports_idx ON ports (origin)
        ''')

        self.database.commit()

    def clear(self):
        self.database.cursor().execute('''
            DELETE FROM ports
        ''')

        self.database.commit()

    def cursor(self):
        return self.database.cursor()

    def commit(self):
        self.database.commit()

    def close(self):
        self.database.commit()
        self.database.close()
