"""
Test script to verify URL configuration.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_test')
django.setup()

from django.urls import resolve, reverse
from django.test import RequestFactory

print("\n" + "=" * 60)
print(" URL Configuration Test")
print("=" * 60)

# Test 1: Health endpoint
try:
    url = '/api/health'
    match = resolve(url)
    print(f"\n[OK] Health endpoint: {url}")
    print(f"     View: {match.func.__name__}")
    print(f"     URL name: {match.url_name}")
except Exception as e:
    print(f"\n[ERROR] Health endpoint failed: {e}")

# Test 2: Parse transcript endpoint
try:
    url = '/api/v1/gluideai/parse-transcript/'
    match = resolve(url)
    print(f"\n[OK] Parse transcript endpoint: {url}")
    print(f"     View: {match.func.__name__}")
    print(f"     URL name: {match.url_name}")
    print(f"     Namespace: {match.namespace}")
except Exception as e:
    print(f"\n[ERROR] Parse transcript endpoint failed: {e}")

# Test 3: Reverse URL lookups
try:
    health_url = reverse('health')
    print(f"\n[OK] Reverse lookup 'health': {health_url}")
except Exception as e:
    print(f"\n[ERROR] Reverse lookup 'health' failed: {e}")

try:
    parse_url = reverse('v1:gluideai:parse-transcript')
    print(f"[OK] Reverse lookup 'v1:gluideai:parse-transcript': {parse_url}")
except Exception as e:
    print(f"[ERROR] Reverse lookup 'v1:gluideai:parse-transcript' failed: {e}")

# Test 4: Test actual health endpoint
print("\n" + "=" * 60)
print(" Testing Health Endpoint")
print("=" * 60)

from gluideai.views import HealthCheck
factory = RequestFactory()
request = factory.get('/api/health')
view = HealthCheck.as_view()
response = view(request)

print(f"\n[OK] Health check status code: {response.status_code}")
print(f"[OK] Health check response: {response.data}")

print("\n" + "=" * 60)
print(" All URL tests completed!")
print("=" * 60 + "\n")
