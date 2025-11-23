from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('gluideai/', include('gluideai.urls')),
]
