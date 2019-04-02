# TicketingService
This is a ticketing service using tornado framework.

Tornado version : 5.1.1

Torndb version : 0.3

Author : Mohammad Ali Poorafsahi

# PreRequirements
- python
- mysql

# Debian distribution command to install python and mysql:
`$ apt install python mysql`

# installation
## step 0:cloning the repository

`
$ git clone https://github.com/MohammadAliAfsahi/TicketingService.git
$ cd ticketing_project 
`
## step 1: Mysql

check if mysql service is running using following command:
`$ service mysql status`

if mysql is running you're free to skip, if not use following command in order to start mysql service:
`$ service mysql start`

run following command as a user that has root privillege or a user that can create database(you can change root to 
desired user):

`$ mysql -u root`

`mysql> CREATE DATABASE ticket;`

Allow the "ticket" user to connect with the password "ticket":

`mysql> GRANT ALL PRIVILEGES ON ticket.* TO 'ticket'@'localhost' IDENTIFIED BY 'ticket';`
 
 # step 2: create table

`mysql> use ticket;`

`mysql> CREATE TABLE user ( id smallint unsigned not null auto_increment, username varchar(20) not null, password varchar(20) not null,firstname varchar(20),lastname varchar(20),apitoken varchar(100), admin BOOLEAN NOT NULL,constraint pk_example primary key (id));`

`mysql> CREATE TABLE tickets ( id smallint unsigned not null auto_increment, subject varchar(50) not null,body varchar(500) NOT NULL, status VARCHAR(20) NOT NULL, userid INT NOT NULL, date DATETIME DEFAULT CURRENT_TIMESTAMP, response VARCHAR(500),constraint pk_example primary key (id) );`

# Run project
`
$ python server/server.py
`

# Usage
The main features are:
1. login
2. signup
3. logout
4. Sending ticket
5. Get tickets (user privilege)
6. Close ticket(user privilege)
7. Change status of ticket (admin privilege)
8. Response to ticket (admin privilege)
9. Get tickets (admin privilege)

This project supports both POST and GET methods.

# Client
In order to run client code you need request module which is pre-installed in python but if not use following command:
`
$ pip install requests
`

# Support:
- Telegram : [@MohammadAliAfsahi](https://t.me/MohammadAliAfsahi)
- gmail : MohammadAliAfsahi.ce@gmail.com


###### special thanks to :

[@limner](https://gitlab.com/limner)


