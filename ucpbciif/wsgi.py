"""
WSGI config for ucpbciif project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
# import django
# from django.core.handlers.wsgi import WSGIHandler

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ucpbciif.settings')

application = get_wsgi_application() 
