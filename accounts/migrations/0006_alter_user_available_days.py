# Generated by Django 4.2.7 on 2024-04-05 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_available_days_user_end_time_user_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='available_days',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Available Days'),
        ),
    ]