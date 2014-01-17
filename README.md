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

shutting down the development instance
--------------------------------------
If you want to shut down the running machine Vagrant is managing first exit from the vagrant ssh session and return to your nomal shell, where you should still be in the cryptoparty.in directory then

        vagrant halt
        
destroying the development instance
-----------------------------------
and if you want to stop the running machine Vagrant is managing and destroy all resources that were created during the machine creation process:

        vagrant destroy
