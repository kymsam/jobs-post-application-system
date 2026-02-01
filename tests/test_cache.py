from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from fastapi import Depends
from JOBS.main import app
from JOBS.Database import get_db

@pytest.fixture
def client():
    return TestClient(app)


#def test_job_cache(db:Session=Depends(get_db)): 
def test_job_cache(client):
    # First request → hits DB 
    response1 = client.get("/jobs/14") 
    assert response1.status_code == 200 
    data1 = response1.json() 
    
    # Second request → should return cached result 
    response2 = client.get("/jobs/14") 
    assert response2.status_code == 200 
    data2 = response2.json() 
    assert data1 == data2

