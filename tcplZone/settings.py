

import os
from pathlib import Path
#for file upload
import boto3
# from storages.backends.s3boto3 import S3Boto3Storage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Add this to use Registration model for the login
# AUTHENTICATION_BACKENDS = ['TCPLapp.authentication_backends.RegistrationBackend']

# AUTH_USER_MODEL = 'TCPLapp.Registration'  # Replace 'your_app' with the actual app name



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1)+*i^d#fc1-!_4(-e6)&2weaf6r@7c=sujkby!&7$p2)#_2!$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "TCPLapp",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tcplZone.urls"

CSRF_COOKIE_SECURE = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tcplZone.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     # 'ENGINE': 'django.db.backends.postgresql',
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
        
    #     'NAME': 'tcplauth4',
    #     'USER': 'postgres', 
    #     'PASSWORD': '1234',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
       
   
    # 'default': {
    #     # 'ENGINE': 'django.db.backends.postgresql',
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
        
    #     'NAME': 'tcpl_postgres',
    #     'USER': 'postgres', 
    #     'PASSWORD': 'postgres123',
    #     'HOST': 'tcplauth4.c3unf3q1zfkv.ap-south-1.rds.amazonaws.com',
    #     'PORT': '5432',
       
    # }
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        
        'NAME': 'database1',
        'USER': 'postgres', 
        'PASSWORD': '12345678',
        'HOST': 'data.c3unf3q1zfkv.ap-south-1.rds.amazonaws.com',
        'PORT': '5432',
       
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

AUTH_KEY = 'your_actual_api_key_value'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'

#This is to save images in media folder
MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR / "media"

#This is to redirect in profile url
LOGIN_REDIRECT_URL='/profile/'

# Add these new lines
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



SESSION_EMGINE="django.contrib.sessions.backends.db"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"





#This is to redirect in profile url
# LOGIN_REDIRECT_URL='/profile/'

# GDAL_LIBRARY_PATH = 'C:/Users/tract/Desktop/zoneproject/.venv/Lib/site-packages/osgeo/gdal304.dll' 

GDAL_LIBRARY_PATH = 'C:/Users/TCPL2/Desktop/pune_zone/.venv/Lib/site-packages/osgeo/gdal304.dll' 
GEOS_LIBRARY_PATH = 'C:/Users/TCPL2/Desktop/pune_zone/.venv/Lib/site-packages/osgeo/geos_c.dll'

#email_auth
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'


AWS_ACCESS_KEY_ID = 'AKIA4VYMO2FKZCLUCFHT '
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tcplpostgres'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




#file upload


# Configure the default file storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Set your AWS S3 bucket name and access credentials
# AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket-name'
# AWS_ACCESS_KEY_ID = 'your-access-key-id'
# AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
# AWS_S3_REGION_NAME = 'your-s3-region'  # e.g., 'us-east-1'

# Additional settings for AWS S3, if needed
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_QUERYSTRING_AUTH = False  # Optional, for querystring authentication

# Other settings
# MEDIA_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN  