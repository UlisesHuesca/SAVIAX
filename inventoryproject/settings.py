"""
Django settings for inventoryproject project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import moneyed

MXN = moneyed.add_currency(
    code='MXN',
    numeric='068',
    name='Peso mexicano',
    countries=('MEXICO', )
)
CURRENCIES =('USD','MXN')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j%w1sp%wr1q1hpfx4nn)=y0(bl$0=$fuus@y^)p8*9mm(11-4t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard.apps.DashboardConfig',
    'solicitudes.apps.SolicitudesConfig',
    'requisiciones.apps.RequisicionesConfig',
    'compras.apps.ComprasConfig',
    'tesoreria.apps.TesoreriaConfig',
    'entradas.apps.EntradasConfig',
    'user.apps.UserConfig',
    'cobranza.apps.CobranzaConfig',
    'gastos.apps.GastosConfig',
    'viaticos.apps.ViaticosConfig',



# Extensions - installed with pip3 / requirements.txt
    'django_extensions',
    'crispy_forms',
    'djmoney',
    'widget_tweaks',
    'simple_history',
    'django.contrib.humanize'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'inventoryproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.contadores_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'inventoryproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'UlisesHuesca$default',
        'USER': 'UlisesHuesca',
        'PASSWORD': 'peruzzi25',
        'HOST': 'UlisesHuesca.mysql.pythonanywhere-services.com',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Esta etiqueta es necesaria para agregar crispy
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

#Manejo de imagenes
STATIC_URL = '/static/'

MEDIA_ROOT = (BASE_DIR/'static/images')

MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
    ]

STATIC_ROOT = (BASE_DIR/"assert/")

#Esta etiqueta es para redigir cuando te logeas desde settings
LOGIN_REDIRECT_URL ='dashboard-index'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = '587'
#EMAIL_HOST_USER = 'saviax.vordcab@gmail.com'
#EMAIL_HOST_PASSWORD = 'yzhzxcdkmmamxchq'
#EMAIL_USE_TLS = True
#EMAIL_USE_SSL = False

EMAIL_HOST = 'mail.vordtec.com'
EMAIL_PORT = '26'
EMAIL_HOST_USER = 'savia@vordtec.com'
EMAIL_HOST_PASSWORD = 'MjUaQ*46852'
EMAIL_USE_TLS = True

USE_THOUSAND_SEPARATOR = True