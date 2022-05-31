# Student manager

Basic functions to manage score, class, student for 3 roles: admin, student, teacher
- Admin: create, update, delete, authorize users
- Teacher: create, update, delete classes, scores, subjects
- Student: view and download score
- Login and logout function


## Requirements:

Install  requirements.txt

```bash
pandas==1.4.2
flask==2.1.2
Flask-MySQL==1.5.2
requests
Flask-Login==0.6.1
passlib==1.7.4
WTForms==3.0.1
```
Install [Postman](https://www.postman.com/downloads/) to test

Install Mysql and Adminer image for initial data:
```bash 
#mysql:8
docker run -itd --restart always --name mysql --hostname mysql \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=my-secret-pw \
-e MYSQL_DATABASE=hieutest \
-e MYSQL_USER=hieu \
-e MYSQL_PASSWORD=hieu123456 \

#adminer
docker run -itd --restart always --name adminer --hostname adminer \
-p 8080:8080 \
```
Import data.sql in adminer (http://192.168.234.192:8080/)*

*: change address, server based on your docker address

*: change app.config['MYSQL_DATABASE_HOST'] in config.py based on your docker address

## Usage

Import project.postman_collection.json in Postman to test project's functions