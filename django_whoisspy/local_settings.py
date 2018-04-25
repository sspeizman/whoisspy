# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(rrz-^00m6nklzzc(47s^)(jkzz@+nj)bzx1-gbt5b6y136bf#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.whoisspy.club'
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

SITE_ID = 1

# For production version
TEMPLATEDIRS = ['/home/acounsel/webapps/django_whoispy/django_whoisspy/whoisspy/templates']

# For production version
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'whoisspy',
        'USER': 'whoisspy',
        'PASSWORD': '22vZQu6KmHSG',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ADMINS = (
    ('Samer', 'samer@accountabilitycounsel.org'),
    ('Marisa', 'marisa@accountabilitycounsel.org')
)


STATICFILES_DIRS = (
    '/home/acounsel/webapps/django_whoispy/django_whoisspy/static/',
)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = '/home/acounsel/webapps/whoisspy_static/'



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL =  '/home/acounsel/webapps/whoisspy_static'
