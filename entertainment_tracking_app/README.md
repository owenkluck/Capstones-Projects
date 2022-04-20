# Cornhusker Entertainment Tracker (CET)
The CET uses SQLAlchemy and a Kivy-based GUI to construct and edit a 
SQL database that can be used to create cities, venues, and weather-dependent 
operating conditions for said venues, as well as edit the data of the venues and 
their operating conditions post-creation.

Project status: **Project complete, no known bugs**

Author: **Kierin Andrews <kandrews4@huskers.unl.edu>**

## Dependencies

The CET mainly relies upon SQLAlchemy and Kivy, both of which come 
preinstalled on PyCharm Edu (the Python IDE used to create this application).

## Running

The main application can be found in the folder `milestone_1` under the name 
`main.py`, while the database installer can be found in the same folder under the 
name `entertainment_installer.py`

Before the application can be run, there first must be a database for the app to 
interact with. To do this, open the Terminal. (The Terminal can be found in the 
Ubuntu applications list or in PyCharm at the bottom of the screen.)
After finding the terminal, type/copy-paste the following code snippet into the 
command-line interface to begin using MySQL:

`mysql --protocol=TCP --user=root -p`

The CLI will then ask for a password. Type in your MySQL password and press enter 
again. If the process was done correctly, the terminal should look like this:

`MariaDB [(none)]>`

Next, type `create database entertainment;` and press enter. If you are given an 
error that says there is already a database with that name, then type 
`drop database entertainment;` before recreating the database under the same name.

You are now ready to run the installer. Find the file called 
`entertainment_installer.py` and run the file by either right-clicking in the file 
and hitting Run or by pressing the green triangle at the top of the file.

If the file has run successfully, then the words `Tables created.` and `Records 
created.` will appear near the bottom of the screen.

You can now run the main application by right-clicking on `main.py` and 
clicking "Run main".
