from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from .Database import get_db,engine
from sqlalchemy.orm import Session
from .import models,schemas,utils
from .routers import auth,jobs, metric,users,application,resume,scoring_rule,dashboard,dashboard_chart
from starlette.responses import Response
from prometheus_client  import Counter,generate_latest
from prometheus_fastapi_instrumentator import Instrumentator 
from .middleware import PasswordValidationMiddleware






models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
async def read_root():
    return {"Message":"Hello user"}

app.include_router(jobs.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(application.router)
app.include_router(resume.router)
app.include_router(scoring_rule.router)
app.include_router(metric.router)
app.include_router(dashboard_chart.router)
app.include_router(dashboard.router)

app.add_middleware(PasswordValidationMiddleware)
