# core/context_processors.py
from django.conf import settings
from django.contrib.auth.models import User


def global_context(request):
    return {
        "project_name": getattr(settings, "PROJECT_NAME", "hcot"),
        # add more as needed
    }
