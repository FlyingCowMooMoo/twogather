Welcome to Twogather!
===================

This is the codebase for the project

It uses Python (2.7+) and Flask for the Back end
The front end is using bootstrap, jQuery UI

If you want to contribute, make a **fork** of the project make your changes and then make a **pull request**. If everyone starts merging to the *master* it will be a complete mess :D


Installing on your local machine.
---------------------------------

Ensure you have Python 2.7.X installed, mac and linux usually come with it preinstalled I think.

Windows users will also need the following runtime: https://www.microsoft.com/en-au/download/details.aspx?id=44266

Once you have python installed, you will need to install some packages

Open a command prompt/terminal and install the following depenencies

    pip install Flask
    pip install Flask-Security
    pip install peewee
    pip install flask-peewee

Then you can download the zip file here and unzip it anywhere: https://github.com/PeteShag/twogather/archive/master.zip

Or if your are familiar with git, just clone the repository to your machine

Then open a command prompt/terminal, navigate to there the project is
and run the following command

    python twogather.py
  
  This will start the server. By default you should be able to connect to it on localhost:5000. For now, it's populating a lot of dummy data so it will take a while for the page to load. This is just something I have done so there is data to work with and will be addressed soon.
