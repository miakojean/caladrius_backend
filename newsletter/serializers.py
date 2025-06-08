from .models import NewsletterSubscribers
from rest_framework import serializers

class NewsletterSubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscribers
        fields = ['id', 'name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        print("Données validées:", validated_data)
        
        # Création standard (utilise tout le validated_data)
        return NewsletterSubscribers.objects.create(**validated_data)
    
    #def deactivate_subscriber(self):
    #    """Méthode pour désactiver un abonné"""
    #    instance = self.instance  # Récupère l'instance du modèle associée
    #    if instance:
    #        instance.is_active = False
    #        instance.save()
    #        return True
    #    return False



