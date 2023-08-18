# Generated by Django 4.2.3 on 2023-08-02 17:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('toDoList', '0002_member_firstname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='password1',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='member',
            name='password2',
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=10000)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toDoList.member')),
            ],
        ),
    ]