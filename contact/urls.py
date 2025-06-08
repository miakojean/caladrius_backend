from django.urls import path
from .views import ContactView, ServicesView, voir  # Import explicite

urlpatterns = [
    path('',ContactView.as_view(), name='contact'),  # Correction de l'orthographe
    path('service/', ServicesView.as_view(), name='contact_service'),  # Ajout pour les services
    path('index/', view=voir, name='contact_index'),  # Correction de l'orthographe
]