# Generated by Django 4.2.7 on 2024-02-29 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
    ]
