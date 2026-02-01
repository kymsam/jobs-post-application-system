from fastapi import FastAPI,APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..Database import get_db
from ..import models
from sqlalchemy import func
from io import BytesIO
from fastapi.responses import StreamingResponse
from ..service.chart import generate_dashboard_chart

router = APIRouter()

@router.get("/dashboard/chart") 
def dashboard_chart(db: Session = Depends(get_db)): 
    results = ( db.query( models.Job.id, 
                         models.Job.Job_position, 
                         models.Job.views, 
                         func.count(models.Application.id).label("applications") )
                           .outerjoin(models.Application, models.Job.id == models.Application.job_id) 
                           .group_by(models.Job.id, models.Job.Job_position, models.Job.views) 
                           .all() 
                           )
    
    if not results: 
        raise HTTPException(status_code=404, 
                            detail="No jobs found for chart") 
    
    data = [{"title": title,"views": views,"applications": applications} 
        for job_id, title, views, applications in results ] 
    buf: BytesIO = generate_dashboard_chart(data) 
    return StreamingResponse(buf, media_type="image/png")