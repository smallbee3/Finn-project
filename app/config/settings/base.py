"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import importlib
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

STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    STATIC_DIR,
]

# IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'config.settings.imagekit-strategy.FixJustInTime'


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


setattr(sys.modules[__name__], 'raven', importlib.import_module('raven'))
set_config(secrets, __name__, root=True)

AUTH_USER_MODEL = 'members.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.APIFacebookBackend',
]

CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'localhost:3000',
    'localhost:4200',
    'rxd119.dothome.co.kr',
    'fc-finn-front.s3-website.ap-northeast-2.amazonaws.com',
    'ec2-52-78-196-254.ap-northeast-2.compute.amazonaws.com',
    'finn.dlighter.com',
)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    'members',
    'house',
    'reservation',
    'imagekit',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Elastic Beanstalk의 Django 애플리케이션에서 발생하는 ELB Health check 4xx에러 해결
# https://lhy.kr/elb-healthcheck-for-django
def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None
