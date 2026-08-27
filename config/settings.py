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
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

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
# JAZZMIN ADMIN THEME
# ==========================================
JAZZMIN_SETTINGS = {
    'site_title': 'Azoria Admin',
    'site_header': 'Azoria',
    'site_brand': 'Azoria',
    'welcome_sign': 'Bienvenue dans le centre de commandement Azoria',
    'copyright': 'Azoria Technologies',
    'search_model': ['shop.Shop', 'accounts.User'],
    'topmenu_links': [
        {'name': 'Accueil',  'url': 'admin:index', 'permissions': ['auth.view_user']},
        {'name': 'Voir le site', 'url': '/', 'new_window': True},
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'hide_models': [],
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'accounts.User': 'fas fa-user-circle',
        'shop.Shop': 'fas fa-store',
        'shop.ShopProduct': 'fas fa-box-open',
        'shop.Order': 'fas fa-shopping-cart',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'related_modal_active': True,
    'custom_css': None,
    'custom_js': None,
    'show_ui_builder': False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar': 'navbar-dark',
    'theme': 'flatly',
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'theme_color': 'default',
    'accent': 'accent-primary',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success'
    }
}

