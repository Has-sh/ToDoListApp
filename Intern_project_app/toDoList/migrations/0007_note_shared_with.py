# Generated by Django 4.2.3 on 2023-08-07 09:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('toDoList', '0006_note_due_date_note_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
