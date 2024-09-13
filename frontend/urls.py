from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('package/<str:package>/', views.package, name='package')
]