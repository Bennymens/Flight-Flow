from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def flights(request):
    return render(request, 'core/flights.html')

def about_us(request):
    return render(request, 'core/about_us.html')

def contact_us(request):
    return render(request, 'core/contact_us.html')

def login_view(request):
    return render(request, 'core/login.html')
