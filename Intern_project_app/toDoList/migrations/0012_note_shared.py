# Generated by Django 4.2.3 on 2023-08-07 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDoList', '0011_delete_usersharednote'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]
