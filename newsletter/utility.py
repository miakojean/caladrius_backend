import pandas as pd
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import NewsletterSubscribers

class NewsletterManager:
    def __init__(self):
        self.subscribers_df = pd.DataFrame()
        self.active_emails = set()
        # Ne chargez pas les données immédiatement
    
    def refresh_data(self):
        """Met à jour les données des abonnés (à appeler explicitement)"""
        self._update_subscribers_data()
    
    def _update_subscribers_data(self):
        """Met à jour le DataFrame des abonnés"""
        try:
            queryset = NewsletterSubscribers.objects.all()
            self.subscribers_df = pd.DataFrame.from_records(queryset.values())
            self.active_emails = set(self.subscribers_df['email']) if not self.subscribers_df.empty else set()
        except Exception as e:
            # Gestion d'erreur si la table n'existe pas encore
            self.subscribers_df = pd.DataFrame()
            self.active_emails = set()
    
    @transaction.atomic
    def add_subscriber(self, name, email):
        """Ajoute un nouvel abonné de manière thread-safe"""
        if email in self.active_emails:
            return False
            
        subscriber, created = NewsletterSubscribers.objects.get_or_create(
            email=email,
            defaults={'name': name, 'is_active': True}
        )
        
        if created:
            self._send_welcome_email(subscriber)
            self._update_subscribers_data()
        
        return created
    
    def send_newsletter(self, subject, message, html_message=None):
        """Envoie la newsletter à tous les abonnés"""
        if self.subscribers_df.empty:
            return 0
            
        recipients = self.subscribers_df['email'].tolist()
        
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return len(recipients)
    
    def _send_welcome_email(self, subscriber):
        """Email de bienvenue"""
        send_mail(
            subject="Bienvenue à notre newsletter",
            message=f"Merci {subscriber.name} pour votre inscription !",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.email],
            fail_silently=False,
        )
    
    def get_stats(self):
        """Retourne des statistiques sur les abonnés"""
        if self.subscribers_df.empty:
            return None
            
        return {
            'total': len(self.subscribers_df),
            'last_subscription': self.subscribers_df['created_at'].max(),
            'name_stats': self.subscribers_df['name'].describe()
        }