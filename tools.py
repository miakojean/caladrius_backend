from django.http import JsonResponse
from .newsletter.utility import NewsletterManager

newsletter_mgr = NewsletterManager()

def subscribe_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if newsletter_mgr.add_subscriber(name, email):
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'exists'}, status=400)

def send_newsletter_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        count = newsletter_mgr.send_newsletter(subject, message)
        return JsonResponse({'status': 'sent', 'recipients': count})