#!/usr/bin/env python3
# encoding: utf-8
# (c) Johannes Fürmann <johannes@weltraumpflege.org>
# http://weltraumpflege.org/~johannes
# This file is part of cryptoparty.in.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse

def initdb():
    """
    initializes the database at cryptoparty.db
    """
    from cryptoparty.database import init_db
    init_db()


def runserver():
    """
    runs a local development server on port 5000
    """
    from cryptoparty import app
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="cryptoparty.in management tool")
    p.add_argument("command")
    a = p.parse_args()
    if a.command is None:
        p.print_help()
    else:
        if a.command == 'runserver':
            runserver()
        elif a.command == 'initdb':
            initdb()
        else:
            print("Unknown command specified, kthxbai.")
