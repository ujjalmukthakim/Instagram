from django.apps import AppConfig
import os
from django.contrib.auth import get_user_model

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.db.utils import OperationalError
        User = get_user_model()
        try:
            username = os.environ.get("CEO_USERNAME")
            email = os.environ.get("CEO_EMAIL")
            password = os.environ.get("CEO_PASSWORD")

            if username and email and password:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                        role="CEO"  # make sure your User model has a 'role' field
                    )
        except OperationalError:
            # Happens if DB isn’t ready yet (migrations not run)
            pass
