# Generated by Django 3.1.7 on 2021-03-16 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courier',
            old_name='working_time',
            new_name='working_hours',
        ),
    ]
