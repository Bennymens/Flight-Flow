from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('visas/', views.visas, name='visas'),
    path('flights/', views.flights, name='flights'),
    path('travel-planner/', views.travel_planner, name='Travel_planner'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('resend-code/', views.resend_code_view, name='resend_code'),
    path('visa-application/', views.visa_application, name='visa_application'),
]