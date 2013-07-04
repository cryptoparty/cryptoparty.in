cryptoparty.in
==============
Web overview of cryptoparties all around the world overlayed on a map.

 * plns to use the OSM Tileserver
 * plans to port from google maps to leaflet.js

Deployment
----------

        git clone git@github.com:waaaaargh/cryptoparty.in.git
        cd cryptoparty.in
  
as root:

        apt-get install libpq-dev
        apt-get install postgresql
        apt-get install virtualenvwrappr

as a result, these should be installed, correct if not so:

* libpq-dev
* postgresql
* postgresql-9.1
* postgresql-common
* postgresql-client-9.1
* postgresql-client-common
* postgresql-server-dev-9.1
* postgresql-9.1-postgis
* libgeos-dev
* libgeos-c1
* libgeos-3.3.3
* postgis
* libproj0
*proj-data

Make a new virtualenv:

        mkvirtualenv cryptoparty

Install from requirements file:

        pip install -r requirements.txt

Add a new system user:

        adduser test
        passwd test
        su - test

Create a new database test with owner as test:

        createdb test -O test
        
Initialise the database by running this script:

        cd scripts
        chmod a+x create_testuser_and_database.sh
        ./create_testuser_and_database.sh

In order to test the flask app create a new file called runserver.py in cryptoparty.in root folder with file contents as:

        from cryptoparty import app
        app.run(debug=True)

then run with: 

        python runserver.py

then fire up your favourite browser and connect to http://127.0.0.1:5000
