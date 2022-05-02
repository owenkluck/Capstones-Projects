# Capstone SOFT 161


## Authors

Connor Weyers <cweyers3@unl.edu>
Owen Kluck <okluck2@unl.edu>
Isaac Kenney <ikenney3@unl.edu>
Kierin Andrews <kandrews4@unl.edu>


## Airport Tracking App

The app that tracks the airports is the folder named airport_tracking_app.
This app tracks airports input into it's system and relays forecasts at those airports. It also allows you 
to create cities to be serviced by these airports.

### Completeness:
The Airport Tracking App is missing one piece of the specifications. That is that the user is asked whether 
they want to add a city or airport if no city or airport is nearby. The user is simply given the option to 
create a city for that airport in the first place regardless of whether there are no other airports or cities 
to service the place.

### Issues:
1. The app will not return the user to the airport or city screen to select an airport or city if the user had selected the create city or create airport button from the success screen after creating a city or airport.
2. 
### Dependencies for Running:
- Repository exists on <git.unl.edu>.
- The repository has been cloned on the local file system.
- The local copy of the repository is up-to-date with the remote repository.
- The tester has access to the repository and has an SSH public key associated
  with their account on <git.unl.edu>.
- You have applied openweather connector to your project build path
- The installer has been run.
- No changes to the database have been made.
### Building and Running:
1. Open a terminal window and run the command 'mysql -h cse.unl.edu -u kandrews -p' and press enter.
2. You will be asked to submit a password, type 'qUc:6M' and press enter.
3. from here run the command 'create database kandrews', if an error is given saying one then leave it.
4. Leave the Terminal and run the python file database_installer.py.
5. Run the main.py file in the airport_tracking_app project folder.
6. To Create an Airport, Press the Create Airport Button and input the necessary data.
7. To Create a City, Press the Create City Button and input the necessary data.
8. To check the forecast on a give day at your airport, press the Check Forecast button and input the necessary data.
9. To Review Itinerary for past or upcoming days press the Review Itinerary Button.


## Entertainment Tracking App

The app that tracks the entertainment options is the folder named entertainment_tracking_app. This app tracks venues,
allowing the user to create venues, reviews and cities for the database. 

### Completeness:
The Entertainment Tracking App is complete in its functionality.
### Issues:
1. At this time there are no known issues with this app.
### Dependencies for Running:
- Repository exists on <git.unl.edu>.
- The repository has been cloned on the local file system.
- The local copy of the repository is up-to-date with the remote repository.
- The tester has access to the repository and has an SSH public key associated
  with their account on <git.unl.edu>.
- You have applied openweather connector to your project build path
- The installer has been run.
- No changes to the database have been made.
### Building and Running:
1. Open a terminal window and run the command 'mysql -h cse.unl.edu -u kandrews -p' and press enter.
2. You will be asked to submit a password, type 'qUc:6M' and press enter.
3. from here run the command 'create database kandrews', if an error is given saying one then leave it.
4. Leave the Terminal and run the python file database_installer.py.
5. Run the main.py file in the entertainment_tracking_app project folder.
6. To create a city press the Create City button.
7. To add a venue press the Add Venue button.
8. To add a review press the Add Review Button.
9. To review past or future travel itineraries press the Review Itinerary button

## Installer

The installer is the folder named installer.

### Completeness:
The installer is complete in its functionality.
### Issues:
The installer has no known issues at this time.
### Dependencies for Running:
- Repository exists on <git.unl.edu>.
- The repository has been cloned on the local file system.
- The local copy of the repository is up-to-date with the remote repository.
- The tester has access to the repository and has an SSH public key associated
  with their account on <git.unl.edu>.
- You have applied openweather connector to your project build path
- The installer has been run.
- No changes to the database have been made.
### Building and Running:
1. Open a terminal window and run the command 'mysql -h cse.unl.edu -u kandrews -p' and press enter.
2. You will be asked to submit a password, type 'qUc:6M' and press enter.
3. from here run the command 'create database kandrews', if an error is given saying one then leave it.
4. Leave the Terminal and run the python file database_installer.py.

## Travel Planner App

The app that plans future travel is the folder named travel_planner_app.

### Completeness:
The Travel Planner App is mostly complete in its functionality. There are some small bugs.
### Issues:
1. The algorithm to determine the next place to travel, will sometimes loop back and forth between airports.
### Dependencies for Running:
- Repository exists on <git.unl.edu>.
- The repository has been cloned on the local file system.
- The local copy of the repository is up-to-date with the remote repository.
- The tester has access to the repository and has an SSH public key associated
  with their account on <git.unl.edu>.
- You have applied openweather connector to your project build path
- The installer has been run.
- No changes to the database have been made.
### Building and Running:
1. Open a terminal window and run the command 'mysql -h cse.unl.edu -u kandrews -p' and press enter.
2. You will be asked to submit a password, type 'qUc:6M' and press enter.
3. from here run the command 'create database kandrews', if an error is given saying one then leave it and skip the next step.
4. Leave the Terminal and run the python file database_installer.py.
5. Run the main.py file in the entertainment_tracking_app project folder.
6. The app will start by giving you a credentials screen. Input the necessary information.
7. Then you will be given the main menu screen where you may choose to validate locations, update reviews, or prepare itineraries.




