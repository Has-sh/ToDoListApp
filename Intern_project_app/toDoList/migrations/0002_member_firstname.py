# Generated by Django 4.2.3 on 2023-08-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDoList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='firstName',
            field=models.CharField(default='default_name', max_length=255),
        ),
    ]
