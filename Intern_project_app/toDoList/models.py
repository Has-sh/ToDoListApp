from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    
    data = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Hello')
    due_date = models.DateField(default=timezone.now)
    shared = models.BooleanField(default=False)
    is_reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        
        return self.title
    
class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        
        return f"{self.note.title} - Token: {self.token} - Created At: {self.created_at}"
