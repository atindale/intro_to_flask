# Intro to Flash

## Overview

This application started out from the Introduction to Flask tutorial on Tuts+. It has been developed further from trying out techiques and technologies. Eventually this will morph into a simple one-man-band professional services business management application.

## Grabbing this application

Just execute the follwing command to grab the application.

```bash
$ git clone https://github.com/atindale/intro_to_flask.git
```

## Creating the database

This application currently needs these tables:

* client
* project
* project_statuss
* vehicle
* mileage
* users

Create the tables with:

```bash
$ . venv/bin/activate
$ export FLASK_APP=intro_to_flask.py
$ flask shell
>>> from app import db
>>> db.create_all()
```

Obviously create your own database and database user beforehand

```SQL
$ mysql
mysql> create database mydatabase
mysql> create user 'newuser'@'localhost' identified by 'password';
mysql> grant all privileges on *.* to 'newuser'@'localhost';
````

## Configuring your database connection

Simply create a config.py file from config.py.example and update the parameters therein.

## Running this application

You can run this application by:

```bash
$ . venv/bin/activate
$ export FLASK_APP=intro_to_flask.py
$ flask run
```

## What's to do next

1. Add CRUD to a page
2. Look into using Datables for rich display of data
3. Rename or clone the app and give it a project management name
4. Add a dashboard type main page.
