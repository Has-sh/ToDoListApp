from django.apps import AppConfig
import sys


class TodolistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'toDoList'
    
    def ready(self):
        if 'runserver' in sys.argv or 'uwsgi' in sys.argv:
            from .scheduler import start_scheduler
            start_scheduler()
