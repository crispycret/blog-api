# flask-user-auth: Flask Based User Authentication Template.

## Introduction
A simple user authentication template.

#### Features:
* User -> Registration | Login | Logout
* Authenticated Sessions using Tokens

Upon registering, user credintials and a newly generated authentication token are stored to the database and the token is returned.
Upon login, an authentication token is generated and is saved to the database (replaces previous token if existing).
Upon logout, the authentication token is erased from the database making it invalid if used in a request.

A decorator is provied, `@authenticated_session`, that returns a user connected to the database if a valid authentication token is given. This simplifies handling requests that may require a user to be authenticated (logged in).


## Setup

### Generate a SECRET_KEY for the Flask Application
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

### Setup and configure the database


#


## Start

#

## Deploy

