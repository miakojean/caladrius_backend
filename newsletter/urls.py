from django.urls import path
from .views import *  # Import explicite

urlpatterns = [  # Correction de l'orthographe
    path('', index, name='index'),
    path('subscribers/', NewsletterSubscriberView.as_view(), name='newsletter_subscribers'),  # Correction de l'orthographe
]