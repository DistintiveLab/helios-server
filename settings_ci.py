# CI-specific settings that override database configuration for GitHub Actions
from settings import *

# Override database settings for CI environment
# This is needed because the main settings.py ignores environment variables during testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'helios',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'CONN_MAX_AGE': 600,
    },
}

# plain users can create elections in tests (fork prod restricts this to
# institution admins, which the upstream test fixtures know nothing about)
HELIOS_ADMIN_ONLY = False

# the CSRF smoke test exercises the feature-election toggle
FEATURE_ELECTION = True
