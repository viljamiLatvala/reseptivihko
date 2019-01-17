## Installing
### Running locally
1. Clone this git repository, and access its root directory.
   `git clone https://github.com/viljamiLatvala/reseptivihko.git`  
   `cd reseptivihko`  
2. When inside repository folder, create an virtual environment to allow you to run the application in locally.
   `python3 -m venv venv`  
3. Activate Venv 
   `source venv/bin/activate`  
4. Make sure your pip is up to date 
   `pip install --upgrade pip`  
5. Install project dependencies
   `pip install -r requirements.txt`  
6. Start the application in virtual environment
   `python3 run.py`  
   You should now get indication that the application is running. The default address and port are 127.0.0.1:5000
7. Admin account needs to be manually inserted to the database
   First open the application on a browser, and create an account to the site
   Then you can elevate user role from the database
   `sqlite3 application/recipes.db`  
   `UPDATE account SET role='admin' WHERE username='*your username*';`  

### Deploying to Heroku
Following instructions assume that you have Heroku account and Heroku command line interface installed:
1. Clone this git repository, and access its root directory.
   `git clone https://github.com/viljamiLatvala/reseptivihko.git`  
   `cd reseptivihko`  
2. Create location and version management address for your application.
   `heroku create *your name for the app*`  
   Heroku CLI will create location for the application, and give you the URLs for that, and the .git address.
4. Push application to Heroku
   `git push heroku master`  
   Heroku should install dependencies and deploy the application.
5. Add environmental variable to signal that the application is on Heroku
   `heroku config:set HEROKU=1`  
6. Add postgreSQL-database for the application
   `heroku addons:add heroku-postgresql:hobby-dev`  
6. Now you can add an admin account

   First open the application on a browser, and create an account to the site..
   Then you can elevate user role from the database
   `heroku pg:psql`  
   `UPDATE account SET role='admin' WHERE username='*your username*';`  