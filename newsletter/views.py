from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NewsletterSubscribers
from .serializers import NewsletterSubscribersSerializer
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the newsletter index.")

class NewsletterSubscriberView(APIView):
    """
    Vue pour gérer les abonnés à la newsletter
    """
    
    def get(self, request):
        subscribers = NewsletterSubscribers.objects.all()
        serializer = NewsletterSubscribersSerializer(subscribers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = NewsletterSubscribersSerializer(data=request.data)
        if serializer.is_valid():
            subscriber = serializer.save()
            
            # Préparation du contenu de l'email
            subject = "Bienvenue dans notre newsletter !"
            
            # Chargement du template HTML
            html_content = render_to_string(
                'newsletter/newsletter.html',
                {
                    'subscriber_name': subscriber.name if subscriber.name else 'abonné',
                    'company_name': settings.COMPANY_NAME,
                    #'unsubscribe_link': f"{settings.SITE_URL}/newsletter/unsubscribe/{subscriber.id}/"
                }
            )
            
            # Version texte brut du contenu
            text_content = strip_tags(html_content)
            
            # Envoi de l'email
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """Désactive un abonné"""
        try:
            subscriber = NewsletterSubscribers.objects.get(pk=pk)
            subscriber.is_active = False
            subscriber.save()
            serializer = NewsletterSubscribersSerializer(subscriber)
            return Response(serializer.data)
        except NewsletterSubscribers.DoesNotExist:
            return Response(
                {"error": "Abonné non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )

    # Ou pour une suppression définitive :
    def delete(self, request, pk):
        """Supprime un abonné (définitif)"""
        try:
            subscriber = NewsletterSubscribers.objects.get(pk=pk)
            subscriber.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NewsletterSubscribers.DoesNotExist:
            return Response(
                {"error": "Abonné non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )