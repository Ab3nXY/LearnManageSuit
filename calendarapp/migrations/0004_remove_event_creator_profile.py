# Generated by Django 4.2.7 on 2024-03-30 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_alter_event_creator_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='creator_profile',
        ),
    ]
