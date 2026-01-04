from django.apps import AppConfig
import os
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        User = get_user_model()

        try:
            username = os.environ.get("CEO_USERNAME")
            email = os.environ.get("CEO_EMAIL")
            password = os.environ.get("CEO_PASSWORD")

            if not all([username, email, password]):
                return

            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )

            if created:
                user.set_password(password)

            # 🔥 FORCE CEO POWERS EVERY TIME
            user.role = "CEO"
            user.status = "Approved"
            user.is_staff = True
            user.is_superuser = True
            user.save()

        except OperationalError:
            pass
