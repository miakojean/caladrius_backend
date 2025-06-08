from .models import Contact, ContactService
from rest_framework import serializers

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        print("Données validées:", validated_data)
        
        # Création standard (utilise tout le validated_data)
        return Contact.objects.create(**validated_data)
        
class ContactServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactService
        fields = ['id', 'name', 'email', "message", 'services', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create (self, validated_data):
        print("Données validées:", validated_data)

        return ContactService.objects.create(**validated_data)