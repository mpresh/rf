# Django settings for demo project.
import os

ROOT_PATH = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

BITLY_API="R_ea72b3fc1102ce7c8285e11b6bd2b11c"
EVENTBRITE_API="ZmQ3NWQ4YjE3OTQ5"

AUTHENTICATION_BACKENDS = (
    #'backends.twitteroauth.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = "twitterauth.UserProfile"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'static')
ADMIN_MEDIA_ROOT = os.path.join(ROOT_PATH, 'static/admin/media')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nw(a_i9yd!r(czkk-x7!_i74k&d@yq6+7gt4y_iia--om-t#pi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.domains.SubdomainMiddleware',
    #'middleware.login.SiteLogin',
)

ROOT_URLCONF = 'rf.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates/core'),
    os.path.join(ROOT_PATH, 'templates/entities'),
    os.path.join(ROOT_PATH, 'templates/fauth'),
    os.path.join(ROOT_PATH, 'templates/tauth'),
    os.path.join(ROOT_PATH, 'templates/frontpage'),
    os.path.join(ROOT_PATH, 'templates/analytics'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sites',
    'core.events',
    'core.entities',
    'core.fauth',       
    'core.tauth',
    'frontpage',
    'analytics',
    'core.campaign',
    'django_extensions',
    'south',
    'core.pos',
    'core.pos.brite',
)


LOGIN_URL = "/admin"
