"""WSGI config for riesgosgenerales project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riesgosgenerales.settings")

application = get_wsgi_application()
