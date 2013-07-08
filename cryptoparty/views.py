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
from datetime import datetime

from cryptoparty import app
from cryptoparty.model import Party, Subscription
from cryptoparty import mail
from cryptoparty.util import random_string, geocode

from flask import render_template, g, request
from wtforms import Form, TextField, FileField, DateTimeField, validators
from flask.ext.mail import Message
import gnupg

EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")


@app.route('/')
@app.route('/<location>')
def hello(location=None):
    return render_template("index.html", location=location)


@app.route('/json/party')
def get_all_parties_as_json():
    parties = g.db.query(Party).filter(Party.time > datetime.now()).\
        filter(Party.confirmed).all()
    parties_serialized = []
    for p in parties:
        party_dict = {
            'name': p.name,
            'time': p.time.strftime("%c"),
            'additional_info': p.additional_info,
            'street_address': p.street_address,
            'organizer_email': p.organizer_email,
            'organizer_twitter_handle': p.organizer_twitter_handle,
            'position': json.loads(g.db.scalar(p.position.ST_AsGeoJSON()))
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
        body=render_template("mail/confirm_subscription.txt",
                             token=s.confirmation_token),
        sender="noreply@cryptoparty.in",
        recipients=[s.email])
    try:
        mail.send(msg)
    except Exception, e:
        return 'error sending mail'

    return 'OK'


@app.route('/subscription/confirm/<token>')

#    name = TextField('Name', [Required()])

def validate_name(form, field):
    if len(field.data) > 50:
        raise ValidationError('Name must be less than 50 characters')

def web_subscription_confirm(token):
    s = g.db.query(Subscription).filter(Subscription.confirmation_token ==
                                        token).all()
    if len(s) > 0:
        try:
            s[0].confirm(token)
        except ValueError:
            return render_template("confirm.html", success=False,
                                   msg="Subscription already confirmed")
        g.db.commit()
        return render_template("confirm.html", success=True,
                                msg="Your subscription has been confirmed.")
    else:
        return render_template("confirm.html", success=False,
                               msg="No Subscription to confirm.")


@app.route('/party/add', methods=['POST', 'GET'])
def web_party_add():
    class AddPartyForm(Form):
        name = TextField('Event name', [validators.required()])
        date = DateTimeField('Time and date', [validators.required()],
                             format='%d-%m-%Y %H:%M')
        additional_info = TextField('Additional Info', [validators.required(),
                                    validators.URL()])
        street_address = TextField('Street address', [validators.required()])

        organizer_email = TextField('Your email address',
                                    [validators.required(), validators.Email()])

        organizer_twitter_handle = TextField('Twitter handle for your city\'s Cryptoparty',
                                    [validators.required(), validators.Regexp('/^[A-Za-z0-9_]{1,15}$/', flags=0, message=u'Invalid Twitter handle, did you forget the @?.')
        organizer_pubkey = FileField('Your GPG Public key')

    if request.method == 'GET':
        form = AddPartyForm()
        return render_template("add_party.html", form=form)

    ## check input
    form = AddPartyForm(request.form)
    if not form.validate():
        return render_template("add_party.html", form=form)

    ## get and check gpg key
    temp_keyring_file = '/tmp/' + random_string(length=8) + '.asc'
    gpg = gnupg.GPG(keyring=temp_keyring_file)

    result = gpg.import_keys(request.files['organizer_pubkey'].read())

    if len(result.fingerprints) != 1:
        form.errors['organizer_pubkey'] = ["Your publickey could not be imported"]
        return render_template("add_party.html", form=form)

    organizer_fingerprint = result.fingerprints[0]

    ## create and save party object

    party_location = geocode(form.street_address.data)

    p = Party(name=form.name.data, time=form.date.data,
              additional_info=form.additional_info.data,
              street_address=form.street_address.data,
              organizer_email=form.organizer_email.data,
              lat=party_location[0], lon=party_location[1])
    g.db.add(p)
    g.db.commit()

    ## encrypt mail
    msg_body = render_template("mail/confirm_party.txt",
                               token=p.confirmation_token)

    encrypted_mail = gpg.encrypt(msg_body, [organizer_fingerprint],
                                 always_trust=True)
    ## send
    msg = Message(subject="cryptoparty.in email address confirmation",
                  body=str(encrypted_mail),
                  sender="noreply@cryptoparty.in",
                  recipients=[p.organizer_email])

    mail.send(msg)
    # TODO delete file in /tmp

    return render_template("add_party.html", success=True, form=form)


@app.route('/party/confirm/<token>')
def web_party_confirm(token):
    p = g.db.query(Party).filter(Party.confirmation_token ==
                                 token).all()
    if len(p) > 0:
        try:
            p[0].confirm(token)
        except ValueError:
            return render_template("confirm.html", success=False,
                                   msg="Party already confirmed")
        g.db.commit()

        ## send mail to subscribers

        # query subscriptions
        subscriptions = g.db.query(Subscription).\
            filter(Subscription.position.
                   ST_DWithin(p[0].position, 100000)).\
            filter(Subscription.confirmed).\
            all()

        mails = []

        # construct mails

        for s in subscriptions:
            msg_body = render_template("mail/notify.txt", party=p[0])
            msg = Message(
                subject="Someone announced a cryptoparty in your area!",
                body=msg_body,
                sender="noreply@cryptoparty.in",
                recipients=[s.email])
            mails.append(msg)

        # actually send mails
        with mail.connect() as conn:
            for m in mails:
                conn.send(m)

        return render_template("confirm.html", success=True,
                               msg="Your e-mail address is now " +
                               "confirmed. Thanks!")
    else:
        return render_template("confirm.html", success=False,
                               msg="No Party to confirm.")
