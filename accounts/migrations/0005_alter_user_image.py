# Generated by Django 4.2.7 on 2024-03-10 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_profile_image_user_image_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='profile_pic/default.jpg', upload_to='profile_pics'),
        ),
    ]
