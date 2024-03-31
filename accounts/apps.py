from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .signals import create_profile  # Import your signal handler
        from django.db.models.signals import post_save
        from .models import User  # Import the User model

        post_save.connect(create_profile, sender=User) 