from sqlalchemy import Integer,Boolean,String,TIMESTAMP,Column,ForeignKey,func,Float
from typing import Text
from .Database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer,nullable=False,primary_key=True)
    Job_position = Column(String,nullable=False)
    Job_description = Column(String,nullable=False)
    Skills_required = Column(String,nullable=False) 
    location = Column(String,nullable=False)
    Job_salary = Column(Integer,nullable=False)
    Required_experience = Column(Integer,nullable=False)
    Education_background = Column(String,nullable=False)
    views = Column(Integer,nullable=False,default=0)
    Created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=Text("now()"))




class User(Base):
    __tablename__ = "users"
    id = Column(Integer,nullable=False,primary_key=True)
    first_name = Column(String,nullable=False)
    second_name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    applications = relationship("Application",back_populates="user")
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    location = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=Text("now()"))
    role = Column(String,nullable=False,default="User")



class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer,nullable=False,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer,ForeignKey("jobs.id",ondelete="CASCADE"),nullable=False)
    resume_id = Column(Integer,ForeignKey("resume.id",ondelete="CASCADE"),nullable=False)
    user = relationship("User",back_populates="applications")
    cover_letter = Column(String,nullable=False)
    status = Column(String,nullable=False,default="submitted") 
    submitted_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=Text("now()"))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=Text("now()"))
    __table_args__ = (UniqueConstraint("job_id","user_id",name="uq_job_user"),)

class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer,nullable=False,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    skills = Column(String,nullable=False)
    experience = Column(Integer,nullable=False)
    education_level = Column(String,nullable=False)
    expected_salary = Column(Integer,nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True),server_default=Text("now()"),nullable=False)
    

class JobScoringRule(Base):
    __tablename__ = "rule"
    id = Column(Integer,nullable=False,primary_key=True)
    job_id = Column(Integer,ForeignKey("jobs.id",ondelete="CASCADE"),nullable=False)
    criteria = Column(String,nullable=False)
    weight = Column(Float,nullable=False)
    threshold = Column(Float,nullable=False)
    __table_args__ = (UniqueConstraint("job_id","criteria",name="unique_job_rule"),)

class JobView(Base):
    __tablename__ = "job_views"
    id = Column(Integer,nullable=False,primary_key=True)
    job_id = Column(Integer,ForeignKey("jobs.id",ondelete="CASCADE"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    viewed_at  = Column(TIMESTAMP(timezone=True),server_default=Text("now()"),nullable=False)
    __table_args__ = ( UniqueConstraint("job_id", "user_id", name="uq_job_user_view"),)