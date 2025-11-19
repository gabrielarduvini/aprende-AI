from django.urls import path
from . import views

urlpatterns = [
    path('stt/', views.stt_view, name='stt'),
    path('tts/', views.tts_view, name='tts'),
    path('nova-palavra/', views.nova_palavra, name='nova_palavra'),
    path('resetar-palavras/', views.resetar_palavras, name='resetar_palavras'),
]
