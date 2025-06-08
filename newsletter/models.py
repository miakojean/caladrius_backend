from django.db import models

# Create your models here.

class NewsletterSubscribers(models.Model):
    name = models.CharField(max_length=255)
    email =models.EmailField(unique=False) #False just for the test
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'souscription de {self.name} réalisée avec l\'email {self.email}'
    
    class Meta:
        verbose_name = "Abonné à la newsletter"
        verbose_name_plural = "Abonnés à la newsletter"