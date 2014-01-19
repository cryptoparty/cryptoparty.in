Adding a party to the map without an email server setup:
--------------------------------------------------------

**WARNING!** This method is not suited for production.

This requires virtualbox and vagrant.

        git clone git@github.com:cryptoparty/cryptoparty.in.git

cd into the cryptoparty.in folder and just

        vagrant up

Now, you can head for a coffee, this will take a while. After vagrant is done, you're nearly there. All you have to do is

        vagrant ssh
        cd /vagrant

and edit the file ```/vagrant/cryptoparty/config.py``` according to your needs.
        
        python3 manage.py initdb
        python3 manage.py runserver

fill out the form at: http://localhost:5001/party/add for each successful form submission, an entry will be added to "Parties" in the 'test' table in the database

we need to read out the confirmation token that was generated for that event (normally emailed to the user who created the event but since we don't have an email server setup...)

now you need to do a psql login. From a new terminal session (i.e. not the one the flask app is currently running in):

        vagrant ssh
        cd /vagrant

        psql -h localhost -d test -U test
        password: test
        SELECT confirmation_token from "Parties";

if you have added any parties using the webfrom then you will see something like this:

<pre>
test=> SELECT confirmation_token from "Parties";
             confirmation_token             
--------------------------------------------
 k4l2ZRfWnE1l9YUzpCJHEcRTTgBNa6lUbvbxx410YC
 7XIQYzK51bBjI4cGSWwWj8LlZoKojRCokaXnI4Bhvr
(2 rows)
</pre>
 now we need to manually trigger 'add party email confirmation' mechanism by supplying the token to the correct URL endpoint, let's build a custom confirmation url using the output of the database query and the endpoint http://localhost:5001/party/confirm/<token>

        http://localhost:5001/party/confirm/k4l2ZRfWnE1l9YUzpCJHEcRTTgBNa6lUbvbxx410YC

Now finally we can see the Parties that we have added actually on the map!

Note: to help with this workaround the following code in views.py was temporarily commented out (todo: this might be better as a debug flag):
<pre>
#    msg = Message(subject="cryptoparty.in email address confirmation",
#                  body=str(msg_body),
#                  sender="noreply@cryptoparty.in",
#                  recipients=[p.organizer_email])
#
#    mail.send(msg)
</pre>
extra notes on psql
-------------------

psql list all tables:
test=> \l

list tables in connected database:
test=> \dt

dump all values under Parties:
test=> SELECT * from "Parties";

dump all confirmation_token values under Parties:
test=> SELECT confirmation_token from "Parties";

full cheatsheet: http://blog.jasonmeridth.com/2012/10/02/postgresql-command-line-cheat-sheet.html
