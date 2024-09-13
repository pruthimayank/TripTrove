from django.shortcuts import render
from .models import Packages

# Create your views here.
def home(request):
    packages = Packages.objects.all()
    packages_list = list(packages.values())
    data = {
        'packages': packages_list
    }
    # print(data)
    return render(request, 'home.html', data)

def package(request, package):
    package = Packages.objects.filter(name=package)
    packages_list = list(package.values())
    data = {
        'package': packages_list[0]
    }
    print(data, "package")
    return render(request, 'package.html', data)