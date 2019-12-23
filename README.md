# movieshub-backend
[![Build Status](https://travis-ci.org/ocranbillions/movieshub-backend.svg?branch=develop)](https://travis-ci.org/ocranbillions/movieshub-backend)


[Heroku Link](https://movieshub-api.herokuapp.com/)

My capstone project for Udacity's Fullstack Nanodegree program.
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Installation & DB setup

Clone this repo and create your local test and development databases with the following names.

    movies_hub      
    movies_hub_test

    If you choose to name the databases differently...
    be sure to reflect the changes in the environment variables in 'setup.sh'


    On a bash terminal, create a python virtual environment:- virtualenv env

    Activate your virtual env:- source env/Scripts/activate

    Install project dependencies:- pip install -r requirements.txt

    Load environment variables:- . setup.sh

    Generate database tables:- python manage.py db upgrade
    
    Seed tables with some initial data:- python manage.py seed

    Run the application:- flask run

    The app is served on port 5000


## Accessing the routes
[localhost-login](https://ocran.auth0.com/authorize?audience=movies&response_type=token&client_id=cliVni40Jsk2gPmMkw43vXhY8c65Uyql&redirect_uri=http://localhost:5000/login-results) |
[logout](https://ocran.auth0.com/v2/logout?client_id=cliVni40Jsk2gPmMkw43vXhY8c65Uyql&returnTo=http://localhost:5000/logout)

[heroku-login](https://ocran.auth0.com/authorize?audience=movies&response_type=token&client_id=cliVni40Jsk2gPmMkw43vXhY8c65Uyql&redirect_uri=http://localhost:5000/login-results) |
[logout](https://ocran.auth0.com/v2/logout?client_id=cliVni40Jsk2gPmMkw43vXhY8c65Uyql&returnTo=http://localhost:5000/logout)

    To access the endpoints in the next section, you'll need to be logged-in.
    The app uses a third-party service (Auth0) for authentication.
    Three roles (user-types) have been created on Auth0. To login as any of these, use the following login details

    Executive Producer      ocranbillions@yahoo.com Password: Xyy673mU
    Casting Director        sammiestt@gmail.com Password: 723M12ai
    Casting Assistant       mike@gmail.com Password: U6263952a

    Ignore the resource-not-found response and get the access_token from your browser's url bar
    set the token in postman's Bearer-Authorization to access the routes below.
    OR if you choose to set the token manually in the header...
    be sure to prepend 'Bearer' before the token. 'Bearer TOKEN'




## Endpoints

NOTE: ALL endpoints require a jwt access_token containing permissions gotten for each user-type upon logging in. (See the login steps above) 

| REQUEST TYPE | ROUTE | ACCESS PERMISSION | DESCrptn | USER | BODY |
| ------------- | ----- | ------------- | ------------- |------------- | ------------- |
| POST | /movies | post:movies | Adds a movie | Exec Prod ONLY | { title:"String", release_date:"YYYY-MM-DD" } |
| PATCH | /movies/id | patch:movies | Updates a movie |Casting Dir & Exec Prod ONLY | { title:"String", release_date:"YYYY-MM-DD" } |
| GET | /movies | get:movies | Gets list of movies | ALL USERS | N/A |
| GET | /movies/id | get:movies | Get a movie | ALL USERS | N/A |
| DELETE | /movies/id | delete:movies | Delete a movie | Exec Prod ONLY | N/A |
| POST | /actors | post:actors | Add an actor | Casting Dir & Exec Prod ONLY | { name:"String", age:"Number", gender:"String" } |
| PATCH | /actors/id | patch:actors | Updates an actor | Casting Dir & Exec Prod ONLY | { name:"optional String", age:"optional Number" gender:"optional String" } |
| GET | /actors | get:actors | Gets list of actors| ALL USERS | N/A |
| GET | /actors/id | get:actors | Get an actor | ALL USERS | N/A |
| DELETE | /actors/id | delete:actors | delete an actor | Casting Dir & Exec Prod ONLY | N/A |



## Running test
    ```
    * Once the test database is created.
    * Stop the server if still running.
    * On a separate terminal, activate the virtual env and run `. test_runner.sh`. 
        This shell file contains the commands to drop any existing tables,
        re-create them, seed the tables and run all unit tests.
    * NOTE: If you get a 401 unauthorized error, replace all tokens in the test files.
        You will have to run the server & login with the users above to get these tokens
    ```


## Technologies

    - Python/Flask
    - Auth0
    - SQLAlchemy
    - Flask-Migrate
    - Flask-Cors
    - Flask-Script


## Pre-requirements for using a different Auth0 Account
- The steps above are enough to get the app running on your local environment. However, you if you choose to have access to Auth0 where you can assign roles to new users as they sign up, then you will have to create your own [Auth0](https://auth0.com/) account. You then create a new application, create the above permissions (e.g 'post:movies' 'get:movies'), create new roles as described above and assign them to users as they sign up.
You will also need to change the below credentials in auth.py to reflect your account
- AUTH0_DOMAIN = ''
- ALGORITHMS = []
- API_AUDIENCE = ''






