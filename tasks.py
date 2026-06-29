# tasks.py
from celery import current_task
from flask_mail import Message
from celery import shared_task
from app import mail

@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, recipients, html_body):
    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            html=html_body)
        mail.send(msg)
        return {"status": "success", "message": f"Email sent to {recipients}"}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise self.retry(exc=e, countdown=30)