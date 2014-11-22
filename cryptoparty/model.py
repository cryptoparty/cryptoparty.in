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

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Unicode

from cryptoparty.database import Base
from cryptoparty.util import random_string
from geoalchemy2 import Geography


class Party(Base):
    __tablename__ = 'Parties'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    time = Column(DateTime)
    additional_info = Column(String)
    street_address = Column(Unicode)
    organizer_email = Column(String)
    organizer_avatar_url = Column(String)
    position = Column(Geography('POINT', srid=4326))
    confirmed = Column(Boolean)
    confirmation_token = Column(String)

    def __init__(self, name, time, additional_info, street_address,
                 organizer_email, lat, lon):
        self.name = name
        self.time = time
        self.additional_info = additional_info
        self.street_address = street_address
        self.organizer_email = organizer_email
        self.organizer_avatar_url = '/static/generic_avatar.png'
        wkt_pos = "POINT(%f %f)" % (lon, lat)
        self.position = wkt_pos
        self.confirmed = False
        self.confirmation_token = random_string(length=42)

    def confirm(self, token):
        if self.confirmed:
            raise ValueError('Party already confirmed')
        if self.confirmation_token == token:
            self.confirmed = True


class Subscription(Base):
    __tablename__ = 'Subscriptions'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    position = Column(Geography('POINT', srid=4326))
    confirmed = Column(Boolean)
    confirmation_token = Column(String)

    def __init__(self, email, lat, lon):
        self.email = email
        self.confirmed = False
        wkt_pos = "POINT(%f %f)" % (lon, lat)
        self.position = wkt_pos
        self.confirmation_token = random_string(length=43)

    def confirm(self, token):
        if self.confirmed:
            raise ValueError('Party already confirmed')
        if self.confirmation_token == token:
            self.confirmed = True


Party.__table__.c.position.type.management = True
Subscription.__table__.c.position.type.management = True
