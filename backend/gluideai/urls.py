from django.urls import path
from .views import TranscriptParseViewSet

app_name = 'gluideai'

urlpatterns = [
    path(
        'parse-transcript/',
        TranscriptParseViewSet.as_view({'post': 'create'}),
        name='parse-transcript'
    ),
]
