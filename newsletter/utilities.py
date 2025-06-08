# test_email.py
import os
import django
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

# Configurez les paramètres Django si vous exécutez ce script seul
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
django.setup()

def test_send_simple_email():
    """Teste l'envoi d'un email simple"""
    subject = "Test d'envoi d'email Django"
    message = "Ceci est un message de test envoyé depuis Django."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['destinataire@example.com']
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    print("Email simple envoyé avec succès!")

def test_send_html_email():
    """Teste l'envoi d'un email HTML"""
    subject = "Test d'envoi d'email HTML Django"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['destinataire@example.com']
    
    # Version texte et HTML du message
    text_content = "Ceci est un message texte simple."
    html_content = """
    <html>
        <body>
            <h1>Ceci est un test HTML</h1>
            <p>Ceci est un <strong>message HTML</strong> envoyé depuis Django.</p>
        </body>
    </html>
    """
    
    email = EmailMessage(
        subject,
        html_content,
        from_email,
        recipient_list,
    )
    email.content_subtype = "html"  # Définit le contenu comme HTML
    email.send()
    print("Email HTML envoyé avec succès!")

def test_send_email_with_attachment():
    """Teste l'envoi d'un email avec pièce jointe"""
    subject = "Test d'envoi avec pièce jointe"
    message = "Veuillez trouver ci-joint un fichier de test."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['destinataire@example.com']
    
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )
    
    # Ajout d'une pièce jointe (créez un fichier test.txt dans le même répertoire)
    file_path = os.path.join(os.path.dirname(__file__), 'test.txt')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            email.attach('test.txt', file.read(), 'text/plain')
    
    email.send()
    print("Email avec pièce jointe envoyé avec succès!")

if __name__ == "__main__":
    print("Début des tests d'envoi d'emails...")
    test_send_simple_email()
    test_send_html_email()
    test_send_email_with_attachment()
    print("Tous les tests ont été exécutés!")