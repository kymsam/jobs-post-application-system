from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from ..import models,schemas
from sqlalchemy.orm import Session
from ..Database import get_db
from ..oauth2 import role_required
from sqlalchemy import func



router = APIRouter()

@router.post("/job/{job_id}/rule",status_code =status.HTTP_201_CREATED)
async def create_scoring_rule(job_id:int,rule:schemas.Rule,db:Session=Depends(get_db),current_user:models.User=Depends(role_required(["Recruiter","Admin"]))):
    
    existing = db.query(models.JobScoringRule).filter(models.JobScoringRule.job_id==job_id,func.lower(models.JobScoringRule.criteria)==rule.criteria.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"The rule {rule} exists")
    

    rule = models.JobScoringRule(**rule.dict(),job_id=job_id)
    
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/job/{rule_id}/rule")
async def get_rule(rule_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(role_required(['Recruiter','Admin']))):
    rule = db.query(models.JobScoringRule).filter(models.JobScoringRule.id==rule_id).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Jobs with id: {rule_id} was not found")
    return rule

@router.get("/job/rule")
async def get_rule(db:Session=Depends(get_db),current_user:models.User=Depends(role_required(['Recruiter','Admin']))):
    rules = db.query(models.JobScoringRule).all()

    return rules


@router.patch("/job/{rule_id}/rule")
async def update_rule(rule_id:int,rule_update:schemas.RuleUpdate,db:Session=Depends(get_db),current_user:models.User=Depends(role_required(['Recruiter','Admin']))):
    rule_query = db.query(models.JobScoringRule).filter(models.JobScoringRule.id==rule_id)
    rule = rule_query.first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rule with id:{rule_id} was not found")
    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Can not execute command")
    
    rule_query.update(rule_update.dict(),synchronize_session=False)
    db.commit()
    return rule_query.first()

@router.delete("/job/{rule_id}/rule",status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(rule_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(role_required(["Recruiter","Admin"]))):
    rule_query = db.query(models.JobScoringRule).filter(models.JobScoringRule.id==rule_id)
    rule = rule_query.first()

    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rule with id:{rule_id} was not found")
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unable to process your request")
    
    rule_query.delete(synchronize_session=False)
    db.commit()
    return rule_query.first()