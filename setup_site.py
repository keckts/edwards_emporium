#!/usr/bin/env python
"""
Setup script for configuring the Django Site object for allauth.
Run this after migrations: python setup_site.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hcot.settings')
django.setup()

from django.contrib.sites.models import Site

def setup_site():
    """Configure the Site object for localhost development."""
    try:
        site = Site.objects.get(id=1)
        site.domain = 'localhost:8000'
        site.name = 'HCOT'
        site.save()
        print("✅ Site configured successfully!")
        print(f"   Domain: {site.domain}")
        print(f"   Name: {site.name}")
        print("\n🚀 You're all set! Run 'python manage.py runserver' to start.")
    except Site.DoesNotExist:
        site = Site.objects.create(id=1, domain='localhost:8000', name='HCOT')
        print("✅ Site created successfully!")
        print(f"   Domain: {site.domain}")
        print(f"   Name: {site.name}")
        print("\n🚀 You're all set! Run 'python manage.py runserver' to start.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Tip: Make sure you've run migrations first:")
        print("   python manage.py migrate")

if __name__ == '__main__':
    setup_site()
