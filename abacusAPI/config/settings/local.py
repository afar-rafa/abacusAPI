from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Local database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static files (for development)
STATIC_URL = "/static/"

# Add any local-specific apps
INSTALLED_APPS += [
    "django_extensions",  # Example: useful for debugging and development tools
]

# Local email settings (for example, using console backend)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
