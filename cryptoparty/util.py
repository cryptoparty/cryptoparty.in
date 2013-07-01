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

import string
import random
import urllib2
import json


def random_string(length):
    """
    returns a random string of the length <length> composed of ASCII letters
    and digits.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in range(length))


def geocode(address):
    """
    takes an address string and returns a (lat, lng) tuple
    """
    url_encoded_address = urllib2.quote(address.encode('utf-8'))
    geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % url_encoded_address

    req = urllib2.urlopen(geocode_url)
    res = json.loads(req.read())
    location = res['results'][0]['geometry']['location']
    return (location['lat'], location['lng'])
