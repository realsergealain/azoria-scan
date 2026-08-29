"""
Django settings for Azoria project.
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps folder to Python path for convenient imports
sys.path.insert(0, str(BASE_DIR / 'apps'))

# ─────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────

# Read SECRET_KEY from environment (never commit a real key to version control).
# Fallback is only acceptable in local development — always set the env var in production!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-djk3c-83jpuhf@u3)^hwongpp3401ahx_=%2)x)0a_2#$sz6f%'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')


# ─────────────────────────────────────────────────────────────
# APPLICATION DEFINITION
# ─────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'import_export',
    'imagekit',

    # Custom Apps
    'apps.accounts',
    'apps.core',
    'apps.shop',
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
        # Only include the top-level templates/ directory here.
        # App templates are discovered automatically via APP_DIRS=True.
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# ─────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ─────────────────────────────────────────────────────────────
# CUSTOM USER MODEL
# ─────────────────────────────────────────────────────────────

AUTH_USER_MODEL = 'accounts.User'


# ─────────────────────────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────────────────────────

# Where to redirect unauthenticated users
LOGIN_URL = '/accounts/login/'

# Where to redirect after a successful login
LOGIN_REDIRECT_URL = '/'

# Where to redirect after logout
LOGOUT_REDIRECT_URL = '/'

# Session cookie age: 2 weeks (in seconds)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14


# ─────────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ─────────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────────────────────

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Abidjan'
USE_I18N      = True
USE_TZ        = True


# ─────────────────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ─────────────────────────────────────────────────────────────

STATIC_URL  = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'


# ─────────────────────────────────────────────────────────────
# CACHE CONFIGURATION & PERFORMANCE
# ─────────────────────────────────────────────────────────────

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'azoria-cache',
        'TIMEOUT': 300,  # 5 minutes par défaut
        'OPTIONS': {
            'MAX_ENTRIES': 2000
        }
    }
}

# Cache-Control pour les assets statiques (1 an)
WHITENOISE_MAX_AGE = 31536000



# ─────────────────────────────────────────────────────────────
# MESSAGES FRAMEWORK
# ─────────────────────────────────────────────────────────────

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG:   'debug',
    message_constants.INFO:    'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR:   'error',
}


# ─────────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY FIELD TYPE
# ─────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# UNFOLD ADMIN THEME
# ==========================================
from django.templatetags.static import static

UNFOLD = {
    'SITE_TITLE': 'Azoria Admin',
    'SITE_HEADER': 'Azoria',
    'SITE_URL': '/',
    'SITE_ICON': {
        'light': lambda request: static('logo.svg'),
        'dark': lambda request: static('logo.svg'),
    },
    'COLORS': {
        'primary': {
            '50': '#F5F3FF', '100': '#EDE9FE', '200': '#DDD6FE', '300': '#C4B5FD',
            '400': '#A78BFA', '500': '#8B5CF6', '600': '#7C3AED', '700': '#6D28D9',
            '800': '#5B21B6', '900': '#4C1D95', '950': '#2E1065',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': True,
        'navigation': [
            {
                'title': 'Boutiques',
                'separator': True,
                'items': [
                    {
                        'title': 'Tableau de bord',
                        'icon': 'dashboard',
                        'link': '/admin/',
                    },
                    {
                        'title': 'Boutiques',
                        'icon': 'store',
                        'link': '/admin/shop/shop/',
                    },
                    {
                        'title': 'Produits',
                        'icon': 'inventory_2',
                        'link': '/admin/shop/shopproduct/',
                    },
                    {
                        'title': 'Identités Visuelles',
                        'icon': 'palette',
                        'link': '/admin/shop/shopbranding/',
                    },
                ]
            },
            {
                'title': 'Utilisateurs',
                'separator': True,
                'items': [
                    {
                        'title': 'Utilisateurs',
                        'icon': 'group',
                        'link': '/admin/accounts/user/',
                    },
                    {
                        'title': 'Groupes',
                        'icon': 'security',
                        'link': '/admin/auth/group/',
                    },
                ]
            },
        ],
    },
}

