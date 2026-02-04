

Job Application Backend System

A scalable backend system for managing job postings and applications, enhanced with an automated applicant evaluation model. The system allows recruiters and administrators to post jobs, applicants to apply and upload resumes, and intelligently determines whether applicants are qualified or not qualified based on job requirements.

This project demonstrates strong backend engineering principles, secure authentication, relational database design, and practical application of automated decision logic.


🚀 Key Highlights (Recruiter View)

Secure, production-ready backend architecture

Role-based access control (Admin / Recruiter / Applicant)

JWT authentication with password hashing

PostgreSQL + SQLAlchemy with Alembic migrations

Automated applicant scoring logic

Clean API design suitable for frontend or mobile integration


Features
Authentication & Authorization

    1.User registration and login

    2.Password hashing for security

    3.JWT token-based authentication

    4.Role-based permissions

Job Management

    Admins and recruiters can:

        1.Create job postings

        2.Specify required skills, salary range, and experience

        3.Manage job listings

Job Applications

    Applicants can:

        1.Apply for jobs

        2.Upload resumes

    Each application is automatically evaluated


Applicant Scoring Model

Applicants are evaluated based on:

    1.Skill match

    2.Salary expectations

    3.Years of experience

The system classifies applicants as:

    Qualified

    Not Qualified

Qualified applicants are automatically informed of their status.



🔔 Notification System Overview
This project implements an asynchronous notification system using Celery and SendGrid:

FastAPI handles incoming requests (e.g., user registration, password reset).

When an email needs to be sent, the app queues a task using Celery.

Redis acts as the broker, storing tasks until workers pick them up.

Celery workers process tasks in the background, ensuring the API stays responsive.

The worker calls the EmailService, which wraps the SendGrid API client.

SendGrid delivers the email reliably to the recipient.






📊 Job Dashboard Feature
The Job Dashboard provides recruiters with real‑time insights into how each job posting is performing. It compares candidate views against applications submitted, and calculates a conversion rate (%) to measure effectiveness.

    Features:
    
    Views Counter → Tracks how many unique candidates viewed each job.

    Applications Counter → Shows how many candidates applied for each job.

    Conversion Rate (%) → Applications ÷ Views × 100, giving recruiters a clear measure of job attractiveness.

    Visualization → Grouped bar chart (Views vs Applications) with a line overlay for Conversion Rate.


    Visualization:
        The dashboard chart compares Views vs Applications with a Conversion Rate line overlay:

        Blue bars → Views

        Orange bars → Applications

        Green line → Conversion Rate (%)

    API Endpoints
        GET /dashboard/jobs → Returns JSON data with views, applications, and conversion rate.

        GET /dashboard/chart → Returns a PNG chart comparing views vs applications with conversion rate overlay.

🛠️🛠️Tech Stack
        Layer	T                   Technology
        Backend Framework	        FastAPI
        Database	                PostgreSQL
        ORM	                        SQLAlchemy
        Migrations	                Alembic
        Authentication	            JWT
        Security	                Password hashing
        ML Logic	                Rule-based / scoring model



Author
Kimani Njonge
Backend Developer | Machine Learning for Finance Enthusiast