from fastapi.testclient import TestClient
from basic_app.main_sqlalchemy import app
from basic_app import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote
from basic_app.database import get_db
from basic_app.database import Base
from basic_app import models
import pytest


engine = create_engine('postgresql://postgres:%s@localhost:5432/fastapi'%quote("Geetha@1955"))
testing_app_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def unitest_get_db():
    db=testing_app_Session()
    try:
        yield db
    finally:
        db.close()




@pytest.fixture
def client():
    yield TestClient(app) # yield is return statement but anything after yield will execute
    print("tests successful and if required drop tables here")

def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == 'hello world SQL Alchemy tutorial'
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users", json = {"email":"test@test.com", "password":"password123"})
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert response.json().get('email') == "test@test.com"