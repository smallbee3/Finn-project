"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import json
import numbers
import os

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')
SECRETS_LOCAL = os.path.join(SECRETS_DIR, 'local.json')
SECRETS_DEV = os.path.join(SECRETS_DIR, 'dev.json')
SECRETS_PRODUCTION = os.path.join(SECRETS_DIR, 'production.json')

secrets = json.loads(open(SECRETS_BASE, 'rt').read())

# Static
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]


def set_config(obj, module_name=None, root=False):
    def eval_obj(obj):
        if isinstance(obj, numbers.Number) or (isinstance(obj, str) and obj.isdigit()):
            return obj

        try:
            return eval(obj)
        except NameError:
            return obj
        except Exception as e:
            return obj

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                set_config(value)
            else:
                obj[key] = eval_obj(value)

            if root:
                setattr(sys.modules[module_name], key, value)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            obj[index] = eval_obj(value)


set_config(secrets, __name__, root=True)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
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

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True
