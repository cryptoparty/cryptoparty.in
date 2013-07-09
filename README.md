cryptoparty.in
==============
Web overview of cryptoparties all around the world overlayed on a map.

screenshot
----------
![](screenshot.png?raw=true)

creating a development instance
-------------------------------

**WARNING!** This method is not suited for production.

This requires virtualbox and vagrant.

        git clone git@github.com:cryptoparty/cryptoparty.in.git

cd into the cryptoparty.in folder and just

        vagrant up

Now, you can head for a coffee, this will take a while. After vagrant is done, you're nearly there. All you have to do is

        vagrant ssh
        cd /vagrant

and edit the file ```/vagrant/cryptoparty/config.py``` according to your needs.
        
        python manage.py initdb
        python manage.py runserver
        
That's it. Fire up your browser and point it to http://localhost:5001 and you're there!
