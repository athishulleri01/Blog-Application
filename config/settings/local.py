from os import getenv, path

from dotenv import load_dotenv

from .base import * #noqa

from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# Here I keep the Security key only for the development purpose
SECRET_KEY =  getenv("DJNAGO_SECRET_KEY","django-insecure-^q0!1gps*!cwnci-5o6$a^096b0+*^pnk^qgk0(*o%38iq4#1i")


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

ADMIN_URL = getenv("ADMIN_URL")

#Only for production purpose
DOMAIN = getenv("DOMAIN")

#----------------------Logging purpose-------------------
# 1. DEBUG   : Low level system information
# 2. INFO    : General level system information
# 3. WARING  : Minor problem occures
# 4. ERROR   : Major problem occures
# 5. CRITICAL: Critical problem occures
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}