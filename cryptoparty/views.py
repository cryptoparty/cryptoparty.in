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

import re
import json

from cryptoparty import app
from cryptoparty.model import Party, Subscription
from cryptoparty import mail

from flask import render_template, g, request
from wtforms import Form, TextField, FileField, validators
from flask.ext.mail import Message

EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")


@app.route('/')
@app.route('/<location>')
def hello(location=None):
    return render_template("index.html", location=location)


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


@app.route('/json/subscription/add', methods=['POST'])
def json_subscription_add():
    # load and unpack form data
    try:
        formdata = request.form['data']
        form_dict = json.loads(formdata)
    except Exception, e:
        return 'Error! ' + str(e)
    if form_dict['lat'] == "" or form_dict['lon'] == "":
        return 'Error! No location selected.'

    # convert geodata to floats
    try:
        lon = float(form_dict['lon'])
        lat = float(form_dict['lat'])
    except KeyError, e:
        return 'Error! ' + str(e)
    except ValueError, e:
        return 'Error! ' + str(e)

    # check email address
    try:
        if not EMAIL_REGEX.match(form_dict['email']):
            return 'Error: invalid Email address'
    except KeyError, e:
        return 'Error! ' + str(e)

    # create and store Subscription Object
    s = Subscription(email=form_dict['email'], lat=lat, lon=lon)
    g.db.add(s)
    g.db.commit()

    # send confirmation mail
    msg = Message(
        subject="cryptoparty.in email address confirmation",
        body=("Hi! \n" +
              "You just registered for norifications from cryptoparty.in. \n" +
              "To confirm that this email address really belongs to you \n" +
              "please point yout favorite browser to: \n\n" +
              "    http://cryptoparty.in/subscription/confirm/%s \n\n" %
              (s.confirmation_token) +
              "Thanks!"),
        sender="noreply@cryptoparty.in",
        recipients=[s.email])
    mail.send(msg)

    return 'OK'


@app.route('/subscription/confirm/<token>')
def web_subscription_confirm(token):
    s = g.db.query(Subscription).filter(Subscription.confirmation_token ==
                                        token).all()
    if len(s) > 0:
        try:
            s[0].confirm(token)
        except ValueError:
            return render_template("confirm.html", success=False,
                                   errormsg="Subscription already confirmed")
        g.db.commit()
        return render_template("confirm.html", success=True)
    else:
        return render_template("confirm.html", success=False,
                               errormsg="No Subscription to confirm.")


@app.route('/party/add', methods=['POST', 'GET'])
def web_party_add():
    class AddPartyForm(Form):
        name = TextField('Event name', [validators.required()])
        date = TextField('Time and date', [validators.required()])
        additional_info = TextField('Additional Info', [validators.required()])
        street_address = TextField('Street address', [validators.required()])
        organizer_email = TextField('Your email address',
                                    [validators.required()])
        organizer_pubkey = FileField('Your GPG Public key')

    if request.method == 'GET':
        form = AddPartyForm()
        return render_template("add_party.html", form=form)

    ## check input
    form = AddPartyForm(request.form)
    if not form.validate():
        return render_template("add_party.html", form=form)

    ## get and check gpg key

    ## encrypt mail

    ## send

    ## add party

    return 'OK'
