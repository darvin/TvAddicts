def setup_legacy_django_compatibility():
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
