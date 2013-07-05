cryptoparty.in
==============
Web overview of cryptoparties all around the world overlayed on a map.

Updates
-------
* now using the OSM Tileserver
* started porting to leaflet.js
* added some demo functionailty to the map like an example map pin

Screenshot
----------
![](screenshot.png?raw=true)

To Do
-----
 * heavy editing of main.js in accordance to change from google maps API to leaflet.js API as per http://leafletjs.com/reference.html
 * remove <iframe>

Creating a development instance
-------------------------------

**WARNING!** This method is not suited for production.

This requires virtualbox and vagrant.

        git clone git@github.com:cryptoparty/cryptoparty.in.git

cd into the cryptoparty.in folder and just

        vagrant up
        
Now, you can head for a coffee, this will take a while. After vagrant is done, you're nearly there. All you have to do is

        vagrant ssh
        cd /vagrant
        pip install -r requirements.txt
        python manage.py initdb
        python manage.py runserver
        
That's it. Fire up your browser and point it to http://localhost:5001 and you're there!

Deployment
----------

        git clone git@github.com:cryptoparty/cryptoparty.in.git
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
* proj-data

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

then run with: 

        python manage.py runserver
 
then fire up your favourite browser and connect to http://127.0.0.1:5000
