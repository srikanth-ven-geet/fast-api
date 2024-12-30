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