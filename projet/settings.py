"""
Django settings for projet project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+@d34a*%izej&!5qp#w-cd*967v(-cj0p#3udweszpnp(&r#oq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1', 'localhost','192.168.8.109']  # Remplacez par votre IP
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
  # Définissez une URL personnalisée


ALLOWED_HOSTS = ['127.0.0.1', 'localhost','192.168.8.109']  # Remplacez par votre IP

LOGIN_URL = '/login/'  # URL pour rediriger si l'utilisateur n'est pas connecté
 # Optionnel : redirige vers l'index après déconnexion




CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # L'URL de ton frontend React
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DHT',
    'rest_framework',
    'twilio',
    'corsheaders',
    'sensor',  # Ajoutez ceci pour votre application sensor
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',



]


ROOT_URLCONF = 'projet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'DHT' / 'template',
            BASE_DIR / 'template',# Ajoute ici le chemin vers ton dossier templates
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


WSGI_APPLICATION = 'projet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import os
STATIC_URL='static/'
STATICFILES_DIRS=[
os.path.join(BASE_DIR,'static')

]
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # remplacer avec l'adresse SMTP de votrefournisseur de messagerie
EMAIL_PORT = 587 # remplacer avec le port SMTP de votre fournisseur demessagerie
EMAIL_USE_TLS = True # ou False, selon la configuration de votrefournisseur de messagerie
EMAIL_HOST_USER = 'farajrayhan@gmail.com' # remplacer avec votre adresse email
EMAIL_HOST_PASSWORD = 'keeu tncl tcjy wxis'

EMAIL_HOST_PASSWORD = 'keeu tncl tcjy wxis'

