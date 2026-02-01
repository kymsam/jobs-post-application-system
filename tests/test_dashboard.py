import pytest
from fastapi.testclient import TestClient
from JOBS.main import app
client = TestClient(app)

def test_dashboard_jobs_empty(monkeypatch): 
     # Mock DB query to return empty list 
    def fake_query(*args, **kwargs): return [] 
    # Patch the dependency 
    monkeypatch.setattr("job.routers.dashboard.db.query", fake_query) 
    response = client.get("/dashboard/jobs") 
    assert response.status_code == 404 
    assert response.json()["detail"] == "No job found for dashboard"


    def test_dashboard_jobs_success(monkeypatch): 

    # Fake DB results 
        fake_results = [(6, "Backend Engineer", 200, 50)] 
        def fake_query(*args, **kwargs): 
            class FakeQuery: 
                def outerjoin(self, *a, **kw): return self 
                def group_by(self, *a, **kw): return self 
                def all(self): return fake_results 
            return FakeQuery() 
        
        monkeypatch.setattr("job.routers.dashboard.db.query", fake_query)
        response = client.get("/dashboard/jobs") 
        assert response.status_code == 200 
        data = response.json() 
        assert data[0]["title"] == "Backend Engineer" 
        assert data[0]["conversion_rate"] == 25.0 
    
def test_dashboard_chart(monkeypatch): 

    # Fake DB results 
    fake_results = [(6, "Backend Engineer", 200, 50)]
    def fake_query(*args, **kwargs): 
        class FakeQuery: 
            def outerjoin(self, *a, **kw): return self 
            def group_by(self, *a, **kw): return self 
            def all(self): return fake_results 
        return FakeQuery() 
    monkeypatch.setattr("job.routers.dashboard.db.query", fake_query) 
    response = client.get("/dashboard/chart") 
    assert response.status_code == 200 
    assert response.headers["content-type"] == "image/png"