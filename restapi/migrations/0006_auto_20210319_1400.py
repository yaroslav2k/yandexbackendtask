# Generated by Django 3.1.7 on 2021-03-19 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0005_auto_20210319_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ASSIGNED', 'Assigned'), ('COMPLETED', 'Complted')], default='PENDING', max_length=25, null=True),
        ),
    ]