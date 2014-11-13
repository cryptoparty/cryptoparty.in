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
from cryptoparty.util import random_string, geocode, Pagination

from flask import render_template, g, request
from wtforms import Form, TextField, FileField, DateTimeField, validators
from flask.ext.mail import Message
from werkzeug.contrib.atom import AtomFeed


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
            'time': p.time.strftime("%a %b %d %Y %H:%I"), #Fri Aug 9 2013 14:37".
            'additional_info': p.additional_info,
            'street_address': p.street_address,
            'organizer_email': p.organizer_email,
            'organizer_avatar_url': p.organizer_avatar_url,
            'position': json.loads(g.db.scalar(p.position.ST_AsGeoJSON()))
        }
        parties_serialized.append(party_dict)
    return json.dumps(parties_serialized)


@app.route('/feeds/atom')
def feed():
    feed = AtomFeed('Upcoming Cryptoparties',
                    feed_url=request.url, url=request.url_root)
    parties = g.db.query(Party).filter(Party.time > datetime.now()).\
        filter(Party.confirmed).all()
    for party in parties:
        text_content = '<h4>' + party.name + '</h4></p>' + '<p><b>Street Address: </b>' + party.street_address + '</p>' + '<p><b>Date: </b>' + party.time.strftime("%a %b %d %Y %H:%I") + '</p>' + '<p><b>Additional Info: </b><a href="' + party.additional_info + '">[link]</a></p>' + '<p><b>Event Organizer: </b>' + party.organizer_email + '</p>'
        feed.add(
            party.name, text_content,
            url=party.additional_info,
            updated = party.time, # this should be the datetime the event was added, but we don't store that
            )
    return feed.get_response()

@app.route('/json/subscription/add', methods=['POST'])
def json_subscription_add():
    # load and unpack form data
    try:
        formdata = request.form['data']
        form_dict = json.loads(formdata)
    except Exception as e:
        return 'Error! ' + str(e)
    if form_dict['lat'] == "" or form_dict['lon'] == "":
        return 'Error! No location selected.'

    # convert geodata to floats
    try:
        lon = float(form_dict['lon'])
        lat = float(form_dict['lat'])
    except KeyError as e:
        return 'Error! ' + str(e)
    except ValueError as e:
        return 'Error! ' + str(e)

    # check email address
    try:
        if not EMAIL_REGEX.match(form_dict['email']):
            return 'Error: invalid Email address'
    except KeyError as e:
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
    except Exception as e:
        return 'error sending mail'

    return 'OK'



#    name = TextField('Name', [Required()])
def validate_name(form, field):
    if len(field.data) > 50:
        raise ValidationError('Name must be less than 50 characters')

@app.route('/subscription/confirm/<token>')
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

    if request.method == 'GET':
        form = AddPartyForm()
        return render_template("add_party_new.html", form=form)

    ## check input
    form = AddPartyForm(request.form)
    if not form.validate():
        return render_template("add_party_new.html", form=form)

    ## create and save party object

    party_location = geocode(form.street_address.data)

    p = Party(name=form.name.data, time=form.date.data,
              additional_info=form.additional_info.data,
              street_address=form.street_address.data,
              organizer_email=form.organizer_email.data,
              lat=party_location[0], lon=party_location[1])
    g.db.add(p)
    g.db.commit()

    msg_body = render_template("mail/confirm_party.txt",
                               token=p.confirmation_token)

    # send
    #todo uncomment these lines which have been commented for development to allow parties to be added without a mail server being setup see READMEDevelopers.md for more information
#    msg = Message(subject="cryptoparty.in email address confirmation",
#                  body=str(msg_body),
#                  sender="noreply@cryptoparty.in",
#                  recipients=[p.organizer_email])
#
#    mail.send(msg)

    return render_template("add_party_new.html", success=True, form=form)


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

        party_coords = json.loads(g.db.scalar(p[0].position.ST_AsGeoJSON()))['coordinates']

        return render_template("confirm.html", success=True,
                               msg="Your e-mail address is now " +
                               "confirmed. Thanks!")
    else:
        return render_template("confirm.html", success=False,
                               msg="No Party to confirm.")


@app.route('/party/archive')
@app.route('/party/archive/page/<int:page>')
def party_archive(page=1):
    parties_query = g.db.query(Party).\
            filter(Party.time < datetime.now()).\
            filter(Party.confirmed)

    return render_template("archive.html", parties=Pagination(
        query=parties_query, objects_per_page=30, page_number=page))


@app.route('/party/upcoming')
@app.route('/party/upcoming/page/<int:page>')
def party_upcoming(page=1):
    parties_query = g.db.query(Party).\
            filter(Party.time >= datetime.now()).\
            filter(Party.confirmed)

    return render_template("upcoming.html", parties=Pagination(
        query=parties_query, objects_per_page=30, page_number=page))
