import pytest
from JOBS.main import app
from fastapi.testclient import TestClient
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from JOBS import models
from passlib.hash import bcrypt,argon2
from JOBS.Database import sessionlocal


@pytest.fixture
def client():
    return TestClient(app)


def test_create_job_unauthorized(client):
    res = client.post(

        '/jobs/',json={
            "Job_position":'cook',
            "Job_description":'dedicated cook',
            "Skills_required":'certified and approved cook',
            "location":'Nakuru',
            "Job_salary":70000,
            "Required_experience":4,
            "Education_background":'collage'
            }
    )
    print(res.json())
    assert res.status_code== 401
    #assert res.json().get('Job_position') == "cook"



@pytest.fixture
def seed_admin_user():
    db = sessionlocal()
    user = models.User(
        email = "testuser@gmail.com",
        password  = argon2.hash("testpassword"),
        location = 'Lamu',
        role = 'Admin'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield(user)
    db.delete(user)
    db.commit()
    db.close()


def test_create_job_authorized(client,seed_admin_user):

    login_res = client.post(
        "/login",
        data = {"username":seed_admin_user.email,"password":"testpassword"},
        
    )
    assert login_res.status_code==200
    token = login_res.json()["access_token"]
    headers = {"Authorization":f"Bearer {token}"}

    res = client.post(
        '/jobs/',json={
            "Job_position":'cook',
            "Job_description":'dedicated cook',
            "Skills_required":'certified and approved cook',
            "location":'Nakuru',
            "Job_salary":70000,
            "Required_experience":4,
            "Education_background":'collage'
            },
            headers = headers
    )
    print(res.json())

    assert res.status_code== 201   #non Admin or Recruiter can not post job
    assert res.json()['Job_position'] == "cook"



