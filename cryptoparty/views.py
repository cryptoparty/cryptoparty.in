#!/usr/bin/env python
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

import json

from cryptoparty import app
from cryptoparty.model import Party

from flask import render_template, g


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/json/party')
def get_all_parties_as_json():
    parties = g.db.query(Party).all()
    parties_serialized = []
    for p in parties:
        party_dict = {
            'name': p.name,
            'time': p.time.strftime("%c"),
            'additional_info': p.additional_info,
            'street_address': p.street_address,
            'organizer_email': p.organizer_email,
            'lat': p.lat,
            'lon': p.lon
        }
        parties_serialized.append(party_dict)
    return json.dumps(parties_serialized)


@app.route('/json/party/<float:lat>/<float:len>')
def get_events_as_json(lat, lon):
    pass


@app.route('/add', methods=['POST'])
def add_parties():
    pass
