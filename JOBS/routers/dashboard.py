from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..Database import get_db
from ..import models
from sqlalchemy import func
from fastapi.responses import StreamingResponse
from JOBS.service.chart import generate_dashboard_chart

router = APIRouter()


@router.get("/dashboard/jobs")
async def job_dashboard(db:Session=Depends(get_db)):
    results = (
        db.query(models.Job.id,
                 models.Job.Job_position,
                 models.Job.views,
                 func.count(models.Application.id).label("applications")
                 )
                 .outerjoin(models.Application,models.Job.id==models.Application.job_id)
                 .group_by(models.Job.id,models.Job.Job_position,models.Job.views)
                 .all()
    )

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No job found for dashboard")
    dash_board = []
    for job_id,title,views,applications in results:
        conversion_rate = (applications/views* 100 ) if views > 0 else 0
        dash_board.append({
            "job_id":job_id,
            "title":title,
            "applications":applications,
            "views":views,
            "conversion_rate":round(conversion_rate,2)
        })
    return dash_board