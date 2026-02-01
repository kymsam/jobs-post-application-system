from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import requests
from .config import settings



celery_app = Celery( "notifications", 
                    broker=f"redis://{settings.redis_hostname}:{settings.redis_port}/0", 
                    backend=f"redis://{settings.redis_hostname}:{settings.redis_port}/0" )


celery_app.conf.update( task_serializer="json", accept_content=["json"], result_serializer="json", timezone="UTC", enable_utc=True )
celery_app.autodiscover_tasks(['JOBS'])



@celery_app.task(name='send_email')

def send_email(to_email,subject,body):
    print("Registered tasks:", celery_app.tasks.keys())

    MAILGUN_API_KEY  = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')

    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        raise RuntimeError("Mailgun credentials missing")
    
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "Jobs Portal <mail@yourdomain.com>",
            "to": [to_email],
            "subject": subject,
            "text": body
        }
    )

    print("to_email",to_email)
    print('subject',subject)
    print("body",body)


    if response.status_code != 200:
        raise RuntimeError(f"Mailgun failed: {response.text}")

    return response.status_code

app = celery_app



