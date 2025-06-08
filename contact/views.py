from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.db import transaction
from .models import Contact, ContactService
from .serializers import ContactSerializer, ContactServicesSerializer
from newsletter.utility import NewsletterManager
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import logging
from django.shortcuts import render

# Initialisation du manager newsletter
newsletter_mgr = NewsletterManager()

logger = logging.getLogger(__name__)

def voir(request):
    return render(request, 'contact/contact.html')

class ContactView(APIView):
    """
    Vue pour gérer les messages de contact et les inscriptions newsletter
    Permissions :
    - GET : réservé aux admins
    - POST : accessible à tous (avec throttling)
    """
    #permission_classes = [IsAdminUser]  # Seuls les admins peuvent lister les contacts
    throttle_classes = [AnonRateThrottle]  # Protection contre le spam

    def get(self, request):  # Correction: ajout du paramètre request manquant
        """
        Liste tous les contacts (réservé aux administrateurs)
        """
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    @transaction.atomic  # Garantit l'intégrité des données
    def post(self, request):
        """
        Crée un nouveau contact et gère l'inscription newsletter
        """
        serializer = ContactSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Sauvegarde du contact
            contact = serializer.save()
            
            # Abonnement newsletter seulement si l'email est valide et présent
            email = request.data.get('email')
            if email:
                newsletter_mgr.add_subscriber(
                    name=request.data.get('name', ''),  # Valeur par défaut vide
                    email=email
                )
            
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:  # Gestion des erreurs inattendues
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ServicesView(APIView):
    """
    Vue pour gérer les demandes de services :
    - GET : réservé aux admins
    - POST : accessible à tous (avec throttling)
    """
    # permission_classes = [IsAdminUser]  # Seuls les admins peuvent lister les contacts
    throttle_classes = [AnonRateThrottle]  # Protection contre le spam

    def get(self, request):
        """
        Liste tous les contacts (réservé aux administrateurs)
        """
        services = ContactService.objects.all()
        serializer = ContactServicesSerializer(services, many=True)
        return Response(serializer.data)
    
    @transaction.atomic
    def post(self, request):
        """
        Crée un nouveau contact et gère l'inscription newsletter
        """
        serializer = ContactServicesSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Sauvegarde du contact
            service = serializer.save()

            # Préparation du contenu de l'email
            subject = "Demande de service reçue"
            html_content = render_to_string(
                'contact/contact.html',
                {
                    'service_name': service.services,
                    'company_name': settings.COMPANY_NAME,
                    'subscriber_name': service.name if service.name else 'abonné',
                    'created_at': service.created_at,
                    'contact_phone': settings.CONTACT_PHONE,
                    'contact_email': settings.EMAIL_HOST_USER,
                }
            )
            text_content = strip_tags(html_content)

            # Envoi de l'email
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [service.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            # Abonnement newsletter
            email = request.data.get('email')
            if email:
                try:
                    newsletter_mgr.add_subscriber(
                        name=request.data.get('name', ''),
                        email=email
                    )
                except Exception as e:
                    logger.error(f"Échec de l'abonnement à la newsletter: {str(e)}")
            
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du service: {str(e)}")
            return Response(
                {"error": "Une erreur est survenue lors du traitement de votre demande"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )