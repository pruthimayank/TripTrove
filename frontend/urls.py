from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('package/<str:package>/', views.package, name='package'),
    path('bookings/', views.bookings, name='bookings'),
    path('about/', views.about, name='about'),
]