cryptoparty.in
==============

Web overview of cryptoparties all around the world

Deployment
----------
clone the code:
  git clone git@github.com:waaaaargh/cryptoparty.in.git
  
as root:
  apt-get install libpq-dev
  apt-get install postgresql
  apt-get install virtualenvwrappr
  
this should install the following packages:

postgresql postgresql-server-dev-9.1 postgresql-9.1-postgis libpq-dev postgresql postgresql-9.1 postgresql-common postgresql postgresql-client-9.1 postgresql-client-common postgresql-server-dev-9.1 libgeos-dev libgeos-c1 libgeos-3.3.3 postgresql-9.1-postgis postgis libproj0 postgresql-9.1-postgis proj-data

  mkvirtualenv cryptoparty
  pip install -r requirements.txt
  as per http://flask.pocoo.org/docs/patterns/packages/
  for testing, create a new file called runserver.py in cryptoparty.in root folder with contents

  from cryptoparty import app
  app.run(debug=True)
  python runserver.py
  
  then connect on http://127.0.0.1:5000 from a browser on the local machine.
