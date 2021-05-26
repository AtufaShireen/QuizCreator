from pathlib import Path
from decouple import config
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ADMINS = (
    ('Atufa', 'anonymouslookingirl@gmail.com'),
)
SECRET_KEY = config('SECRET_KEY')
cloudinary.config( 
  cloud_name = "dzzpfmpgm", #"CLOUD_NAME", 
  api_key = "696813483658762", #, #"CLOUD_API_KEY", 
  api_secret = "AW1QvsfDRFWt2dYXaz-05twrI2M" #"CLOUD_API_SECRET" 
)

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1','localhost','.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'quiz.apps.QuizConfig',
    'users.apps.UsersConfig',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'django_cleanup',
    'widget_tweaks',
    'cloudinary',
    # 'cloudinary_storage',
]

MIDDLEWARE = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quizzmaster.urls'

TEMPLATES = [
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
]

WSGI_APPLICATION = 'quizzmaster.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {

     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = '' #str(BASE_DIR/ 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = ''#str(BASE_DIR/ 'media')  # create folder
MEDIA_URL = ''#'/media/'
TAGGIT_CASE_INSENSITIVE = True
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'quiz:quizzes'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#  Add configuration for static files storage using whitenoise
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}