# Getting the app to run
## Locally
1. Clone this git repository.
2. When inside repository folder, install Venv to allow you to run the application in virtual environment.
3. Activate Venv by calling `source /venv/bin/activate` when in repository root directory
4. To make sure your pip is up to date, call `pip install -r requirements.txt`
5. Install project dependencies by calling `pip install -r requirements.txt`
6. To start the application in virtual environment, call `python3 run.py` . You should now get indication that the application is running. The default address and port are 127.0.0.1:5000
7. Admin account needs to be manually inserted to the database, this can be done by opening recipes.db file in the application directory, and calling `INSERT INTO account(username, password, role) VALUES ("*your admin name*, *your admin pw*, "admin")`

## On Heroku
Following instructions assume that you have Heroku account and Heroku command line interface installed:
1. Clone this git repository.
2. Call `heroku create *your name for the app*` . Heroku CLI will create location for the application, and give you the url for that, as well as the .git version management address.
3. connect heroku to git by calling `git remote add heroku *git address heroku provided* `
4. Push application to herku by doing git add, git commit and then calling `git push heroku master` . Heroku should install dependencies and deploy the application.
5. Add postgreSQL-database for the application by calling `heroku addons:add heroku-postgresql:hobby-dev`
6. Now you can add admin account by connecting to the database calling `heroku pg:psql` and once the connection has been established, creating the account with command `INSERT INTO account(username, password, role) VALUES ("*your admin name*, *your admin pw*, "admin")`
