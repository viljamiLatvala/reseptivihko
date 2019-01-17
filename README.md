# Reseptivihko - RecipeApp
## Table of Contents
1. [Description](#description)
2. [Instructions for use](#instructions-for-use)
3. [Installing](#installing)
4. [User stories](#user-stories)
5. [Database diagram and schema](#database-diagram-and-schema)
6. [Developement points and problems](#developement-points-and-problems)
7. [My experiences](#my-experiences)
## Description
This is a web application created as course work for the course Tietokantojen harjoitustyö (Database excercise project).

The basic idea of the application is for users to be able to add and browse recipes.

Application users are able to register user accounts that they can log in with, add and edit their own recipes. Users with admin rights are able to edit any recipe or tag.

Recipes contain information such as name, preparation time, ingredient description and instructions. Users are also able to mark their recipes with tags of their choosing, and browse recipes by tags.

### Application on Heroku
Application is running on Heroku at: https://reseptivihko.herokuapp.com

For testing purposes, feel free to use following admin-credentials:

__username:__  admin
__password:__ password

For basic user functionality, you can create your own user-account. Please note that at this time, passwords are stored in the application database as plain text.

## Instructions for use
### Front page and navigation
Upon accessing the front page of the site, you are greeted with a welcome, short description and some site statistics. The navigation bar is located at the top of the site, and provides links to add a recipe, to view a list of all recipes and to browse tags associated with recipes. If user is not logged in, a possibility for doing so, or creating a new account is visible in the right corner of the navigation bar. If user is logged in, username and logout link is shown.

Without logging in, visitors can browse recipes added by others, and tags associated with recipes. If user wants to create their own recipe, login is required.

### User creation and logging in
Creating user is done by clicking the link "Create an accunt!" shown on the right corner of the navigation bar, when user is not signed in. This takes user to the account creation form, where user can choose their own username and password. Account credentials must follow these rules:

* Username must be unique
* Username must between 3 and 16 characters long
* Password must be between 8 and 144 characters long
* Password must contain both letters and numers
* Password must contain both uppercase and lowercase letters
* Password must match the password re-written in the "Re-type password"-field

If the credentials submitted by user do not meet these rules, the form is not accepted, and displays error messages to explain what rule is not met. After choosing suitable credentials, user-account is created, signed in and redirected to the front page of the site. From there, user can start accessing functionality that requires being logged in, I.E. adding and editing recipes.

If user already has an account they can log in by clicking the "Log in" link in the navigation bar that leads them to a log in form.

Once logged in, the right corner links of the navigation bar are replaced with the username of the logged in account, and a link to sign them out.

### Recipe list and individual recipe view
The "Recipe list"-link in the navbar leads users to (surprisingly) a list of recipes added into the application database. The list shows the name of the recipe, and the preparation time for that recipe. By clicking a name of a recipe, the user is led to a view of the recipe. This view contains all the information about the recipe: its name, creator, preparation time, ingredients that are needed, instructions for making the dish and lastly identifier tags that have been associated with the recipe. By clicking one of these tags, users can see other recipes associated with the tag. If the recipe that is viewed is created by the same user that has logged in, or logged in user is admin, a possibility to edit the recipe is shown.

### Creating and editing a recipe
Adding a recipe is done by clicking "Add a recipe" from the navigation bar. This opens a form that takes in all of the recipe information. Recipe information must meet following requirements:

* Name of the recipe must be unique
* Name of the recipe must be between 3 and 64 characters long
* Preparation time must be entered, and must be a number
* Each line of ingredients must be between 3 and 140 characters long
* Instructions must be between 10 and 6000 characters long
* Each tag must be between 3 and 18 characters long

If these requirements are not met, the form will show according error messages.

Users can separate different ingredients with linebreaks. This way ingredients are shown in a list form. Similarly adding multiple tags is possible by separating different tags with a comma.

Users can submit the recipe by pressing "Add recipe". On adding the recipe, different pieces of recipe information are ensured to have some spesific form. These include:

* Leading and trailing whitespace is removed from all fields
* Recipe name is forced to begin with a capital letter
* Ingredient lines are forced to begin with a capital letter
* Tags are forced to begin with a capital letter, and be otherwise lowercase

To edit a recipe, user must be the creator of said recipe, or be an admin. Editing form is opened from the individual recipe view. The editing form contains all of the same fields that the recipe creation form, but is preloaded with the values of the recipe being edited. Editing form also contains the possibility to remove the recipe. Edited recipe must pass same validations as a new recipe.

### Tag list and individual tag view
A list of tags is found under the "Browse tags" link on the navbar. This view contains a list of tags that have been added, and the amount of recipes belonging to each tag. This list is shown in descending order.

By clicking a tag name on the list, user is directed to a site containging a list of all the recipes that the tag is associated with. From there, user can navigate to view these recipes. Tags can also have descriptions added by administrators, to further describe recipes belonging to the tag. From this view, administrators are able to detach any recipes they deem unfit from the tag.

By default, users are not able to create tags in other ways than adding a previously unused tag to a recipe. However admins are capable of creating tags without any recipes. This functionality could be used for example to format the tag list with pre-meditated tag-names and descriptions to inspire and help users use tag functionality.

## Installing
### Running locally
1. Clone this git repository, and access its root directory.
...`git clone https://github.com/viljamiLatvala/reseptivihko.git`
...`cd reseptivihko`
2. When inside repository folder, create an virtual environment to allow you to run the application in locally.
...`python3 -m venv venv`
3. Activate Venv 
...`source venv/bin/activate`
4. Make sure your pip is up to date 
...`pip install --upgrade pip`
5. Install project dependencies
...`pip install -r requirements.txt`
6. Start the application in virtual environment
...`python3 run.py` 
...You should now get indication that the application is running. The default address and port are 127.0.0.1:5000
7. Admin account needs to be manually inserted to the database
...First open the application on a browser, and create an account to the site
...Then you can elevate user role from the database
...`sqlite3 application/recipes.db`
...`UPDATE account SET role='admin' WHERE username='*your username*';`

### Deploying to Heroku
Following instructions assume that you have Heroku account and Heroku command line interface installed:
1. Clone this git repository, and access its root directory.
...`git clone https://github.com/viljamiLatvala/reseptivihko.git`
...`cd reseptivihko`
2. Create location and version management address for your application.
...`heroku create *your name for the app*` 
...Heroku CLI will create location for the application, and give you the URLs for that, and the .git address.
4. Push application to Heroku
...`git push heroku master` 
...Heroku should install dependencies and deploy the application.
5. Add environmental variable to signal that the application is on Heroku
...`heroku config:set HEROKU=1`
6. Add postgreSQL-database for the application
...`heroku addons:add heroku-postgresql:hobby-dev`
6. Now you can add an admin account
...First open the application on a browser, and create an account to the site
...Then you can elevate user role from the database
...`heroku pg:psql`
...`UPDATE account SET role='admin' WHERE username='*your username*';`

## User stories

|As a/an | I want to... | so that...| related SQL-query | 
|--------|--------------|-----------|-------------------|
| user | be able to add recipes with ingredient lists and instructions | other people can enjoy the recipes that I come up with | 
| user | be able to edit my recipe instructions, |I can correct any mistakes |
| user | be able to edit my recipe ingredients, |I can adjust the amounts after coming up with better ones | 
| user | be able to anticipate how long it takes to make a dish by following a spesific recipe | I can manage my time better | 
| user | search recipes by category | I can find recipes to suit my mood and taste | 
| user | be able to delete a recipe | I don't have to share anything I dont want to online | 
| admin | Be able to edit any recipe on the platform | I can remove any explicit language | 
| admin | Be able to remove any recipe | I can weed out possible spam | 
| admin | Manage which recipes belong to which tag | Make sure tags contain only recipes that belog to it | 
| admin | add descriptive information for tags | I can describe what sorts of recipes a tag should contain | 

## Database diagram and schema
### Diagram
A database diagram drawn with [yuml.me](https://yuml.me). The diagram represents the relations of different database entities.

![database diagram](https://github.com/viljamiLatvala/reseptivihko/blob/master/documentation/database_diagram.png?raw=true "database diagram")

### Schema
```sql
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	username VARCHAR(64) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	role VARCHAR(64), 
	PRIMARY KEY (id)
);
CREATE TABLE tag (
	id INTEGER NOT NULL, 
	name VARCHAR(144) NOT NULL, 
	description VARCHAR(144), 
	PRIMARY KEY (id)
);
CREATE TABLE recipe (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	instruction VARCHAR(6000), 
	preptime INTEGER, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE ingredient (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	line VARCHAR(500) NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (id)
);
CREATE TABLE tags (
	tag_id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	PRIMARY KEY (tag_id, recipe_id), 
	FOREIGN KEY(tag_id) REFERENCES tag (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (id)
);

```
## Developement points and problems
* Making CRUD-functionality for users
* Hashing passwords, passwords are now stored in plaintext.
* User roles done with a separate table instead of as column of account table
* Setting different userroles in some other way than directly setting them directly to the database
* Better authorization for defining usergroups
* Editing recipes tags and instrucions are currently done by first removing all recipes and tags of a recipe, and then adding everything in the editform in. More sophisticated way could be done.
* Some database interaction is still done outside models directories.

## My experiences
This project uses SQLAlchemy, and while I had previosly stumbled upon the consept of ORMs, it was a fist time using one for me. Using SQLAlchemy was fairly straight forward and intuitive, and it certainly made alot of stuff easier. Things I found a bit harder to grasp at first was creating different kinds of relations between database models and separating database objects and their usage into their own directories and files to form an undestandable filestructure for the project. However towards the end of the course I managed restructure my database models and code into a more clean and suitable form.

This course was also my first time using Python for any web-development. My experiences were, that Flask is a very flexible framework and it was very easy to get started with it. I feel like having to use multiple different extensions to achieve some functionality such as ORM, validation and authentication led to a better understanding of the sturcture, inner workings and expandability of Flask projects.

I found the peer-to-peer reviews done in this course very valuable, both to read and write. Detailed and well structured criticism, experiences and opinions from others was good material for steering the project into a right direction. I especially liked that the reviewing forced me to pay attention to the readability and style of the code I wrote, something I easily overlook in code I know is for "my eyes only". I also liked the course schedule, since it provided some good weekly waypoints and thus helped to keep the project on track.