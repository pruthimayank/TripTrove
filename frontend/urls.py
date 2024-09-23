from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('package/<str:package>/', views.package, name='package'),
    path('packages/', views.packages, name='packages'),
    path('bookings/', views.bookings, name='bookings'),
    path('about/', views.about, name='about'),
    path('policies/', views.policies, name='policies'),
    path('terms/', views.terms, name='terms'),
    path('blog/', views.blog_list, name='blog'),
    
    #rest
    path('booking/', views.handle_booking, name='handle_booking')
]