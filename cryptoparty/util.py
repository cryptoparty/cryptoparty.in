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
import urllib
import json
from math import ceil

from cryptoparty import app

from twython import Twython

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
    url_encoded_address = urllib.parse.quote(address)
    #url_encoded_address = urllib.parse.quote(address.encode('utf-8'))
    geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % url_encoded_address

    req = urllib.request.urlopen(geocode_url)
    res = json.loads(req.read().decode('utf-8'))
    location = res['results'][0]['geometry']['location']
    return (location['lat'], location['lng'])

class Pagination(object):
    def __init__(self, query, objects_per_page, page_number):
        self.objects_per_page = objects_per_page
        self.page_number = page_number
        self.total_count = query.count()
        self.objects = query.offset(objects_per_page * (page_number - 1)).\
                                    limit(objects_per_page).all()

    @property
    def first_page(self):
        if self.page_number < 2:
            return True
        else:
            return False

    @property
    def last_page(self):
        if self.page_number < self.total_pages:
            return False
        else:
            return True

    @property
    def total_pages(self):
        return ceil(self.total_count / self.objects_per_page)
