from django.urls import path
from .views import scanner_view, api_dados_tempo_real

urlpatterns = [
    path('', scanner_view, name='scanner'),
    path('api/dados/', api_dados_tempo_real, name='api_dados'),
]