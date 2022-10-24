# [Revision: 10/22/2022]

# Application Setup
## Create .env and generate application secret keys

To setup the application first create a `.env` file in the root directory.

Next generate the required `secret keys` for the application.

* SECRET_KEY
* ADMIN_SECRET_KEY

To generate a secret key open a pyhton terminal and run the following.

```
import secrets
secrets.token_hex(64)
```

Output 
``` ed1125209f460dbdbd998e0a4ceb1e4c62ac5f8b89501edd54a0e281f24c9ba4b0fba781b5928a02e4ca659e8c8ffb837206e965d682a501eda012f655c5b511
```

Generate unique secret keys for every required `.env` parameter.


#### Example .env
```
SECRET_KEY=ed1125209f460dbdbd998e0a4ceb1e4c62ac5f8b89501edd54a0e281f24c9ba4b0fba781b5928a02e4ca659e8c8ffb837206e965d682a501eda012f655c5b511

ADMIN_SECRET_KEY=7a8e60bc40ab70b67f4304048977610a595e670c50cb356c8c5e88c6d430fa930d3814a809f7c284cbc8a1d4f05f339ae1fb4049844b1058c89778e49085b580
``` 

## Next, setup database
The next thing to do is to generate the local database for the application (We are using SQLite for this project).

```
flask db init
flask db migrate
flask db upgrade
```

## Finally, Create Admin User.
Now that the application and database are ready lets create an admin account.

The application has an `ADMIN_SECRET_KEY` located in the `.env` file that is used to check the signature of a `create_admin` request. The requester must `encode` their request with this key so the application knows the requester has the authorization to create an admin account.

First: Create the request body that will be encoded. Just like a normal `create_user` request, a unqiue email should be provided along with a password.

```
data = {
    "email": "new_admin@email.com",
    "password": "admin's password"
}
```

Third: Encode the request body using the `ADMIN_SECRET_KEY` to create an authroization token.

```
import jwt
token = jwt.encode(data, ADMIN_SECRET_KEY, 'HS256')
print(token)
```

Output
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGVtYWlsLmNvbSIsInBhc3N3b3JkIjoibXlQYXNzd29yZCJ9.47eq50GWJvdwaOIS-CTUT2XSO0ZwpGX9Bo2N3kEV1bw
```

Fourth: The token should be stored as the value of the `Authorization` header of the request.


Fith: Send the request to the application.

Postman Example -> ...




# ###########################################################
# ###########################################################

# [Old Documentation]
# flask-user-auth: Flask Based User Authentication Template.

## Introduction
A simple user authentication template.

#### Features:
* * User -> Registration | Login | Logout
* * Authenticated Sessions using Tokens


* Upon registering, user credintials and a newly generated authentication token are stored to the database and the token is returned.
* Upon login, an authentication token is generated and is saved to the database (replaces previous token if existing).
* Upon logout, the authentication token is erased from the database making it invalid if used in a request.

A decorator is provied, `@authenticated_session`, that returns a user connected to the database if a valid authentication token is given. This simplifies handling requests that may require a user to be authenticated (logged in).


## Setup

### Clone
First clone and navigate inside the application.
```
git clone git@github.com:crispycret/flask-user-auth.git
# or
git clone https://github.com/crispycret/flask-user-auth.git

cd flask-user-auth
```

### Environment Setup
Create a virtual enviornment to run the application in and install the required libraries.
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```


#### Generate a SECRET_KEY for the Flask Application
In a python shell generate your flask applications secret token using python library `secrets`. 
```
import secrets
secrets.token_hex(64)
```

Paste the generated token in the `.env` file of the projects root directory. Create this file if nesseccary.
##### .env
```
SECRET_KEY=91b47920cca5d2fce10d4096f90c0e69eceae11e0c537a263e22ff11cbacdf34c00492deb6643cf676b68efd12a781ec174ae3abbe7f8f1d83b00a8fee234927
```

#### Setup and configure the database
Initialize, migrate and update the database.
```
flask db init
flask db migrate
flask db upgrade
```

#


## Start

```
flask run
```

#

# API Testing w/ Postman
Postman is an application that make interacting with an API easy and is great tool for API development.
A `postman collection` has been provided in this repo. 
Import the collection into the postman application and test the running Flask API

## Deploy

