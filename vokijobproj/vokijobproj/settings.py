from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = str(os.getenv('ENVIRONMENT', 'development'))

if ENVIRONMENT in ['development', 'staging']:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

# Common settings for all environments
COMMON_SETTINGS = {
    'SECRET_KEY': str(os.environ.get('SECRET_KEY')),
    'ALLOWED_HOSTS': [],
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'apps.aistream',
        'apps.reactconnect',
        'apps.fileintake',

        'storages',
        'apps.useraccount.apps.UseraccountConfig',],
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        "whitenoise.middleware.WhiteNoiseMiddleware",
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    'ROOT_URLCONF': 'vokijobproj.urls',
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    'WSGI_APPLICATION': 'vokijobproj.wsgi.application',
    'AUTH_PASSWORD_VALIDATORS': [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
    ],
    'LANGUAGE_CODE': 'en-us',
    'TIME_ZONE': 'UTC',
    'USE_I18N': True,
    'USE_TZ': True,
    'STATIC_URL': 'static/',
    'DEFAULT_AUTO_FIELD': 'django.db.models.BigAutoField',
    'FILE_TYPE_CHOICES': [('RS', 'Resume'), ('CL', 'Cover Letter'),],
}



AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))
AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))
AWS_STORAGE_BUCKET_NAME = str(os.getenv('AWS_STORAGE_BUCKET_NAME'))
AWS_S3_SIGNATURE_NAME = str(os.getenv("AWS_S3_SIGNATURE_NAME"))
AWS_S3_REGION_NAME = str(os.getenv("AWS_S3_REGION_NAME"))
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
MEDIAFILES_LOCATION = 'media'


# Development-specific settings
DEVELOPMENT_SETTINGS = {
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    },
}

# Staging-specific settings
STAGING_SETTINGS = {
    'DEBUG': False,
    'ALLOWED_HOSTS': ['staging.yourdomain.com'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    },
}

# Production-specific settings
PRODUCTION_SETTINGS = {
    'DEBUG': False,
    'ALLOWED_HOSTS': ['yourdomain.com'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    },
    'SECURE_SSL_REDIRECT': True,
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
}

# Determine which environment we're in
ENV = os.environ.get('DJANGO_ENV', 'development')

# Start with common settings
settings = COMMON_SETTINGS.copy()

# Update with environment-specific settings
if ENV == 'development':
    settings.update(DEVELOPMENT_SETTINGS)
elif ENV == 'staging':
    settings.update(STAGING_SETTINGS)
elif ENV == 'production':
    settings.update(PRODUCTION_SETTINGS)
else:
    raise ValueError(f"Unknown environment: {ENV}")


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Now set the Django settings from our settings dictionary
globals().update(settings)