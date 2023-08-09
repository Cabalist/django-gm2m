DEBUG = True
SECRET_KEY = "secret"

DATABASES = {
    "default": {
        "NAME": "gm2m",
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "gm2m",
)

ROOT_URLCONF = "tests.urls"

USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
