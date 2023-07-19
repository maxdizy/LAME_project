"""
Django settings for LAME project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import psycopg2
import boto3
import json
from django.core.files.storage import default_storage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
AWS_ACCESS_KEY_ID = 'AKIA4KQG7XH5OVEP7WOR'
AWS_SECRET_ACCESS_KEY = '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'

s3 = boto3.resource('s3',
aws_access_key_id=AWS_ACCESS_KEY_ID,
aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
verify=False)

def get_file(file_path):
    return s3.Bucket('lame-bucket').Object(file_path).get()['Body']

def push_file(file_path, contents):
    return s3.Bucket('lame-bucket').Object(file_path).put(Body=contents)

def push_json(file_path, contents):
    return s3.Bucket('lame-bucket').Object(file_path).put(Body=(bytes(json.dumps(contents).encode('UTF-8'))))

SECRET_KEY = get_file('data/key.txt').read().decode()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False

#ALLOWED_HOSTS = ['https://lame-b9e2e1e6b25e.herokuapp.com']
ALLOWED_HOSTS = ['*']

# server {
#     listen 80 default_server;
#     return 444;
# }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MADI.apps.MadiConfig',
    'HOME.apps.HomeConfig',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LAME.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
]

WSGI_APPLICATION = 'LAME.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dfd779b7nskdrk',
            'USER': 'zearswbhpbqnmv',
            'PASSWORD': '93aa0c65115d6a1d61a0b284c541a3a970b4e1f965e8e9544b95129b504262bf',
            'HOST': 'ec2-52-205-45-222.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/MADI/static/'

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'HOME-home'
LOGIN_URL = 'HOME-login'

AWS_STORAGE_BUCKET_NAME = 'lame-bucket'
AWS_ACCESS_KEY_ID = 'AKIA4KQG7XH5OVEP7WOR'
AWS_SECRET_ACCESS_KEY = '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'

AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'