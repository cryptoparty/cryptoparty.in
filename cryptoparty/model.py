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

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean

from cryptoparty.database import Base
from cryptoparty.util import random_string


class Party(Base):
    __tablename__ = 'Parties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(DateTime)
    additional_info = Column(String)
    street_address = Column(String)
    organizer_email = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    confirmed = Column(Boolean)
    confirmation_token = Column(String)

    def __init__(self, name, time, additional_info, street_address,
                 organizer_email, lat, lon):
        self.name = name
        self.time = time
        self.additional_info = additional_info
        self.street_address = street_address
        self.organizer_email = organizer_email
        self.lat = lat
        self.lon = lon
        self.confirmed = False
        self.confirmation_token = random_string(length=42)

    def confirm(self, token):
        if self.confirmed:
            raise ValueError('Party already confirmed')
        if self.confirmation_token == token:
            self.confirmed = True
