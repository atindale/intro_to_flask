# Intro to Flash

## Overview

This application started out from the Introduction to Flask tutorial on Tuts+. It has been developed further.

## Grabbing this application

Just execute the follwing command to grab the application

```bash
$ git clone https://github.com/atindale/intro_to_flask.git
```

## Creating the database

This application currently need a vehicle, mileage and users table. Create them in MySQL with the following DDL 

```SQL
CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_short_name` varchar(55) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

CREATE TABLE `mileage` (
  `mileage_id` int(11) NOT NULL AUTO_INCREMENT,
  `journey_date` date NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `start_km` int(11) DEFAULT NULL,
  `end_km` int(11) DEFAULT NULL,
  `journey` varchar(100) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `purpose` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`mileage_id`),
  KEY `fk_mileage_vehicle1_idx` (`vehicle_id`),
  KEY `fk_mileage_project1_idx` (`project_id`),
  CONSTRAINT `fk_mileage_project1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_mileage_vehicle1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `pwdhash` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
```

Obviously create your own database and database user beforehand!

## Configuring your database connection

Simple create a config.py file from config.py.example and update the parameters therein 

## Running this application

You can run this application by:

```bash
$ cd app
$ python runserver.py
```

