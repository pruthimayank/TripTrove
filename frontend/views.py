from django.shortcuts import render
from .models import Packages

# Create your views here.
def home(request):
    packages = Packages.objects.all()
    packages_list = list(packages.values())
    data = {
        'packages': packages_list
    }

    return render(request, 'home.html', data)