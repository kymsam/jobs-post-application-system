from fastapi.testclient import TestClient
import pytest
from JOBS.main import app
from JOBS.schemas import CreateUser
from pydantic import ValidationError
from fastapi import HTTPException


@pytest.fixture
def client():
    TestClient(app)



def test_valid_create_user(client):
    user = CreateUser(
        email = "email@gmail.com",
        password="Email.peter1",
        location = "Kilifi"
    )
    assert user.email == "email@gmail.com"
    assert user.location == 'Kilifi'
    assert user.role == 'User'




def test_invalid_email(client):
    with pytest.raises(ValidationError):
        CreateUser(
            email = "home@com",
            password="StrongPass1!",
            lacation = 'rongai'
        )

def test_invalid_password_too_short(client):
    with pytest.raises(HTTPException):
        CreateUser(
            email = 'oscar@gmial.com',
            password = 'Ocar!3',
            location = 'kiserian'
        )

def test_invalid_password_no_number(client):
    with pytest.raises(HTTPException):
        CreateUser(
            email = 'kigan@gmail.com',
            password = "kigan%not",
            location = "rwanda"
        )
    
def test_invalid_password_no_uppercase_letter(client):
    with pytest.raises(HTTPException):
        CreateUser(
            email='lookman@gmail.com',
            password="look#man1",
            location='Ngong'
        )

def test_invalid_password_no_special_character(client):
    with pytest.raises(HTTPException):
        CreateUser(
            email="kadong@gmial.com",
            password='kaDong7kigan',
            location='rironi'
        )





