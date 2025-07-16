from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.mail import send_mail
from django.http import JsonResponse
import random

# Ensure that a Profile instance exists for each User
for user in User.objects.all():
    Profile.objects.get_or_create(user=user)

def home(request):
    return render(request, 'core/home.html')

def flights(request):
    return render(request, 'core/flights.html')

def about_us(request):
    return render(request, 'core/about_us.html')

def contact_us(request):
    return render(request, 'core/contact_us.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == "POST":
        step = request.POST.get('step')
        # Step 3: Send verification code to email
        if step == "3":
            email = request.POST.get('email')
            code = str(random.randint(100000, 999999))
            request.session['verification_code'] = code
            request.session['email'] = email
            send_mail(
                'Your Flight-Flow Verification Code',
                f'Your code is: {code}',
                'benymento4@gmail.com',  # Must match EMAIL_HOST_USER in settings.py
                [email],
                fail_silently=False,
            )
            return render(request, 'core/registration.html', {'step': 4, 'email': email})
        # Step 4: Check code
        elif step == "4":
            # Combine the 6 boxes into one code string
            code_input = ''.join([
                request.POST.get(f'code{i}', '') for i in range(1, 7)
            ])
            if code_input == request.session.get('verification_code'):
                return render(request, 'core/registration.html', {'step': 5})
            else:
                messages.error(request, "Invalid verification code.")
                return render(request, 'core/registration.html', {'step': 4, 'email': request.session.get('email')})
        # Step 5: Create user
        elif step == "5":
            first_name = request.POST.get("first_name", "")
            last_name = request.POST.get("last_name", "")
            email = request.session.get("email", "")
            username = email
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                login(request, user)
                return redirect('home')
    # Initial step
    return render(request, 'core/registration.html', {'step': 1})

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
        # Handle other POST actions (like username change) here
        # ...
        return redirect('profile')
    return render(request, 'core/profile.html')

@login_required
def edit_profile_view(request):
    # Add your edit logic here (for now, just render a template)
    return render(request, 'core/edit_profile.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def resend_code_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'No email provided.'})
        code = str(random.randint(100000, 999999))
        request.session['verification_code'] = code
        send_mail(
            'Your Flight-Flow Verification Code',
            f'Your code is: {code}',
            'benymento4@gmail.com',  # Should match EMAIL_HOST_USER in settings.py
            [email],
            fail_silently=False,
        )
        return JsonResponse({'success': True, 'message': 'Verification code resent.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
