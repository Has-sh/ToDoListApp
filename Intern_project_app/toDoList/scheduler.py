from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from apscheduler.jobstores.base import JobLookupError
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Note
import logging
import uuid

logger = logging.getLogger(__name__)

def send_due_date_reminders_for_tomorrow():
    try:
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        notes_due_tomorrow = Note.objects.filter(due_date=tomorrow, is_reminder_sent=False)

        for note in notes_due_tomorrow:
            if not note.is_reminder_sent:
                send_due_date_reminder_email(note)
                note.is_reminder_sent = True
                note.save()
                
    except Exception as e:
        logger.exception("An error occurred: %s", str(e))

def send_due_date_reminder_email(note):
    user_email = note.userId.email
    note_title = note.title
    note_user = note.userId.username

    subject = 'Reminder: Note Due Tomorrow'
    html_message = render_to_string("due_date.html", {'note_title': note_title, 'note_user': note_user})
    email = EmailMessage(subject, html_message, to=[user_email])
    
    if email.send():
        logger.info('Mail sent to %s', note_user)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    try:
        scheduler.remove_all_jobs()
    except Exception as e:
        logger.exception("An error occurred while clearing jobs: %s", str(e))
    
    unique_job_id = str(uuid.uuid4())

    try:
        scheduler.remove_job(unique_job_id)
    except JobLookupError:
        pass

    scheduler.add_job(
        send_due_date_reminders_for_tomorrow,
        trigger=IntervalTrigger(hours=1), 
        next_run_time=timezone.now(),  
        id=unique_job_id  
    )
    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started...")
