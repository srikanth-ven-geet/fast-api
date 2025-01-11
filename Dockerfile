FROM python:3.9.7
#set up a working dir where everything will happen
WORKDIR /usr/src/app
#copy the requirement file for pip packages
COPY requirements.txt /usr/src/app/
#run the packages
RUN pip install --no-cache-dir -r requirements.txt
#now copy the code base to the working dir
COPY . /usr/src/app
#now start the server
CMD ["uvicorn","app.main_sqlalchemy:app", "--host","0.0.0.0","--port","8000"]