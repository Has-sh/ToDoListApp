from django.apps import AppConfig


class TodolistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'toDoList'
    
    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()