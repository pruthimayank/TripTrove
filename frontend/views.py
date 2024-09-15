from django.shortcuts import render, redirect
from .models import Packages, agent 

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        try:
            agent_instance = agent.objects.get(username=username)
            
            if password == agent_instance.password:
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'password'})
        except agent.DoesNotExist:
            return render(request, 'login.html', {'error': 'no such agent'})
    else:
        return render(request, 'login.html')

def home(request):
    packages = Packages.objects.all()
    packages_list = list(packages.values())
    data = {
        'packages': packages_list
    }
    return render(request, 'home.html', data)


def package(request, package):
    package = Packages.objects.filter(name=package).first()  # Use .first() to get the first match

    if package:
        data = {
            'package': package
        }
        return render(request, 'package.html', data)
    else:
        return render(request, '404.html', {'error': 'Package not found'})
