# core/apps.py
from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import AppRegistryNotReady
from django.contrib.auth import get_user_model   # ← use this

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Create a default super‑user (admin / admin@123) once,
        **even when a custom user model is in use.**
        """
        try:
            User = get_user_model()                   # ← custom or default
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin@123'
                )
                print("Default admin created: admin / admin@123")
        # first run migrations, or tables not ready
        except (OperationalError, ProgrammingError, AppRegistryNotReady):
            pass
