from django.shortcuts import render
import requests

def get_country_from_ip(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        return data.get('country_code', 'GHA')  # Default to Ghana if not found
    except Exception:
        return 'GHA'

def home(request):
    ip = request.META.get('REMOTE_ADDR', None)
    country_code = get_country_from_ip(ip)
    return render(request, 'core/home.html', {'country_code': country_code})

def flights(request):
    return render(request, 'core/flights.html')

def about_us(request):
    return render(request, 'core/about_us.html')

def contact_us(request):
    return render(request, 'core/contact_us.html')

def login_view(request):
    return render(request, 'core/login.html')
