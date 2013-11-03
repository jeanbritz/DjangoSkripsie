import os

# Django settings for skripsie project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('jibritz', 'britz.jean@gmail.com'),
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['ml.sun.ac.za']


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/jibritz/devel/skripsie/skripsie.db'
    }
}

DATABASE_ENGINE = 'django.db.backends.sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/home/jibritz/devel/skripsie/skripsie.db'           # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

FIXTURE_DIRS = (
   os.path.join(os.path.dirname(__file__), 'accounts/fixtures'),
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "static"),
    '/var/www/static/',
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p6irv0)_g^n!6rl^qxp%sv@k^_2alnuoadq2_qqerhqi+#+jjd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
   
   'django.template.loaders.filesystem.Loader',
   'django.template.loaders.app_directories.Loader',
   
)

TEMPLATE_CONTEXT_PROCESSORS = (
	
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
	'django.contrib.auth.context_processors.auth',
	
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	'oauth2_provider.middleware.OAuth2TokenMiddleware',
	
)

ROOT_URLCONF = 'skripsie.urls'

#AUTH_PROFILE_MODULE = 'paySystem.UserProfile'
AUTH_USER_MODEL = 'paySystem.User'

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.staticfiles',
	'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.sites',
    'registration',
	'paySystem',
	'rest_framework',
	'rest_framework_swagger',
	'crispy_forms',
	'django_openid_auth',
	#'inspector_panel',
	'south',
	'oauth2_provider',
	'oauthlib',
	'braces',
	
	
)

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '1.0',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '123', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}

DEBUG_TOOLBAR_PANELS = (
    #'debug_toolbar.panels.version.VersionDebugPanel',
    #'debug_toolbar.panels.timer.TimerDebugPanel',
    #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    #'debug_toolbar.panels.headers.HeaderDebugPanel',
    #'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    #'debug_toolbar.panels.template.TemplateDebugPanel',
    #'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.signals.SignalDebugPanel',
    #'debug_toolbar.panels.logger.LoggingPanel',
	#'inspector_panel.panels.inspector.InspectorPanel',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'auth.GoogleBackend',
	'oauth2_provider.backends.OAuth2Backend',
	
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

OAUTH2_PROVIDER = {
    'CLIENT_ID_GENERATOR_CLASS':
        'oauth2_provider.generators.ClientIdGenerator',
    'CLIENT_SECRET_GENERATOR_CLASS':
        'oauth2_provider.generators.ClientSecretGenerator',
		# this is the list of available scopes
    #'SCOPES': {'read' , 'write', 'groups'}
}


REST_FRAMEWORK = {
	
	'DEFAULT_AUTHENTICATION_CLASSES' : (
		'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
		#'oauth2_provider.ext.rest_framework.OAuth2Authentication',
	),
	'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
	
}


CRISPY_TEMPLATE_PACK = 'bootstrap'

REGISTRATION_DEFAULT_GROUP_NAME='Consumer'
ACCOUNT_ACTIVATION_DAYS = 7

