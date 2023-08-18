# Generated by Django 4.2.3 on 2023-08-03 18:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('toDoList', '0005_alter_note_userid_delete_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='note',
            name='title',
            field=models.CharField(default='Hello', max_length=200),
        ),
    ]
