always create a virtual env for a project. Command to create:
py -3 -m venv <name>

for this new python virtual env, we need to set the python path
go to View->command pallette->python select interpreter
enter the path of python.exe in the virtual env : .\project1\Scripts\python.exe

 now the terminal also should point to the virtual env. run this command in terminal
 project1\Scripts\activate

 to install the fastapi libraries run this:
 pip install fastapi[all]

create the first py file and make changes to it

start the app server command:
uvicorn <file name of the entry point>:app --reload
eg : uvicorn main:app --reload

After developing API, fastapi will generate API  documentation easily
just access : localhost:8000/docs
or          : localhost:8000/redoc

creation of package(folders) in python:
1. create a folder with any name.
2. inside each folder create a dummy empty file : __init__.py
3. then run the command to start the main.py : uvicorn <folder>.<main.py file>:app --reload

to know all the libraries installed run this:
pip freeze

To install the postgres libraries
command : pip install psycopg2

install sql alchemy orm
command: pip install sqlalchemy

configure the db connection as sqlalchemy cannot interact wthout it

install the password hashing library using the below command.
pip install passlib[bcrypt]

To generate token and signature install this libraries
pip install python-jose[cryptography]

To handle env variables, do this:
1. create a class (config.py) that will extend BaseSettings
2. create variables into it.
3. Set these variables with values from .env file
Dont upload this to git so add the .env file to .gitignore

What is CORS : By default API for a site will be accessible only from that site only.
IF API is running on a different site then CORS policy should be set up to access it from another
site.
the CORS middleware will run before any request is executed. It handles the pre flight request.

run this command : pip freeze > requirements.txt
all the packages will be printed in the file
to install all these packages in a different machine to run our app run the below
pip install -r <file>.txt

Alembic : A python library to alter table after its created. 
USing SQL Alchemy, table will be created only once and its not possible to alter table.
Alembic is a tool to do DDL and is used for DB migrations
command : pip install alembic
to initialize it : alembic init <some dir name>
1. its a general idea to install and start the DB related changes in alembic mode.
2. create the first Alembic change:
run the command : alembic revision -m "<add some comments>"
3. This will create a versions folder and will have a .py file inside it
4. in that file there will be one method for upgrade and another for downgrade.
5. in upgrade method, create, alter table to add new things
6. in downgrade method, write a roll back for #5
7. run the command : alembic upgrade "<version>"  to execute the upgrade method of the revision.
8. run the command : alembic downgrade "<version>" or alembic downgrade -<number> to undo change
9. command : alembic upgrade head  - to run the latest version upgrade method.
command : alembic heads - to get latest file
command : alembic revision autogenerate -m "<comments>"  - This will auto generate DDL for tables
          based on the models we have defined. Once generated, run the alembic upgrade head to execute it

HEROKU : A salesforce based dev ops app where env can be set, code can be built and deployed.
create heroku account and install heroku CLI in local machine
1. heroku --version
2. login :  heroku login
3. create an app command : heroku create <name> . This will create a new app
This will create an app and will also have a git repo created for heroku.
4. run : git remote . This will give 2 remotes. One for git another for heroku git
if remote is not set, run this: git add "main" git@github.com:srikanth-ven-geet/fast-api.git
5. cmd to push our code from git : git push heroku main 
enter your user name (email) and the API key as password (heroku auth:token).
6. Create a file with name : Procfile in the main directory of the project.
This file will have app restart command


Ubuntu cloud deployment:
Try digital ocean or Amazon ECS with Ubuntu
1. sudo apt update && sudo apt upgrade -y : -y is used to answer all questions with "y"
2. check if python is installed : python3 --version
3. If not installed install py: sudo apt install python-<version #>
4. install pip : sudo apt install python3-pip
5. install py virtual env : sudo pip3 install virtualenv
6. install postgres: sudo apt install postgresql postgresql-contrib -y
7. to access postgres via CLI check : psql --version
8. connect to postgres : psql -U <username>
9. to see the list of users in the linux : sudo cat /etc/passwd
10 : To switch user : su -postgres  : To switch user to login to postgres
11. To create a new password for the postgres user : \password <username>
12 : To quit postgres cli : \q
13. go to root and : cd /etc/postgresql/<version>/main  and do: ls-lrt
14. sudo vi postgresql.conf : make sure the postgres is accessible from outside the cloud by changing the listen port to *
15. sudo vi pg_hba.conf : to make conf changes to list of accessible IP
16. restart postgres : systemctl restart postgresql
17. Create a linux user : adduser <username>  .do not work with root user. switch user : su -<username>
18: provide root level accessto this user from root : usermod -aG sudo <username>.
19. to log on as the user : ssh <username>@<public IP>
20. to finish root level access to the user : sudo apt upgrade
21. now create a virtual env : virtualenv venv
22. mkdir src . cd src . git clone <https://.....> . to clone the code into src
23. get into venv : source venv/bin/activate  .to get out of venv run : deactivate
24. run : pip install -r requirements.txt
25. if any library fails run this : deactivate . sudo apt install <library name>
26. always run the serverin venv mode : uvicorn app.main:app
27. cd ~ . vi .env . In this file add all the env variables like DB user , pwd, etc
28. run : set -o allexport; source /home/user/.env; set +o allexport. This will set the env values
29. env vars will be deleted when system is rebooted. add #28 to .profile file to get around 
30. uvicorn --host 0.0.0.0 app.main:app.
31. now run the app in local browser: <public cloud ip>:8000
32. pip install gunicorn
33. gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
gunicorn will spawn mutiple threads and will handle loads
34. /etc/systemd/system : Here is where automating script to start server after reboot can be done
create a .service file and update it

For SSL or HTTPS:
1. visit site certbot.eff.org site it will have instruction to install step by step
2. firewall:
sudo ufw status, sudo ufw allow <port or protocol>, sudo ufw enable

Docker:
1. hub.docker.com : search for python and select the official python image
2. refer to Dockerfile for the config
3. build the docker image  command from command line : docker build -t fastapi
4. create a docker-compose.yml

Unit test:
pip install pytest - to install pytest framework
create "tests" directory outside the app dir
create test py file with this format <>_test.py or test_<>.py
The methods also should have test in its name
run: pytest  to execute these files
sample command :  pytest -v -s --disable-warnings .\tests\test_users.py

CI/CD:
1. Github actions, jenkins can be used
2. CI CD just provides a runner
3. Pipelines are triggered thru some actions like git push
4. check the gitbuh actions reference package (events that trigger workflows)
5. 

