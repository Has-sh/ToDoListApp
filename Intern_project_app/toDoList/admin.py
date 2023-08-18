from django.contrib import admin
from .models import Note, SharedNote

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
   
    list_display = ("id", "title", "userId", "due_date", "shared", "is_reminder_sent")

# Create an admin class for the SharedNote model
class SharedNoteAdmin(admin.ModelAdmin):
    
    list_display = ("id", "note", "token", "created_at")

# Register the models with the custom admin classes
admin.site.register(Note, NoteAdmin)
admin.site.register(SharedNote, SharedNoteAdmin)