/import os/a\
import hashlib\
#STATIC_URL = '/static/'\
#STATIC_ROOT = '/srv/static/'

/^ALLOWED_HOSTS/c\
ALLOWED_HOSTS = ['*']\
URL_FIELD_NAME = 'record_url'

/^INSTALLED_APPS/a\
    'django.contrib.staticfiles',\
    'rest_framework',\
    'rest_framework.authtoken',\
    'django_filters',\
    'django.contrib.postgres',

# This does not seem to work properly, switching to the simpler PageNumberPagination style
#'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',\
# Perhaps there is some conflict with the dynamic filtering system
/^MIDDLEWARE/i\
REST_FRAMEWORK = {\
    'DEFAULT_AUTHENTICATION_CLASSES': [\
        'rest_framework.authentication.TokenAuthentication',\
        'rest_framework.authentication.SessionAuthentication'\
        ],\
    'DEFAULT_FILTER_BACKENDS': [\
                                'rest_framework_filters.backends.DjangoFilterBackend'],\
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\
    'PAGE_SIZE':20\
    }\

/^        'DIRS':/c\
        'DIRS': ['/srv/website/templates/'],

/^DATABASES/i\
# Allow connections to persist (default is 0 seconds)\
CONN_MAX_AGE = 60\
with open(os.environ['POSTGRES_PASSWORD_FILE'],'r') as password_file:\
    postgres_password = password_file.readline()\
postgres_password_hasher = hashlib.md5()\
postgres_password_hasher.update(postgres_password.encode())\
hashed_postgres_password = postgres_password_hasher.hexdigest()\

/^        'ENGINE'/c\
        'ENGINE': 'django.db.backends.postgresql',

/^        'NAME': os/c\
        'NAME': 'postgres',\
        'USER': 'postgres',\
        'PASSWORD': postgres_password,\
        'HOST': 'db',\
        'PORT': '5432'
    
