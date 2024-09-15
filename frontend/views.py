from django.shortcuts import render, redirect
from .models import Packages, agent  

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            agent_instance = agent.objects.get(username=username)
            
            if password == agent_instance.password:
                return redirect('home') 
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except agent.DoesNotExist:
            return render(request, 'login.html', {'error': 'No such agent'})
    else:
        return render(request, 'login.html')


# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if agent.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        new_agent = agent(username=username, password=password)
        new_agent.save()
        return redirect('login') 
    else:
        return render(request, 'signup.html')


# Home view
def home(request):
    packages = Packages.objects.all()
    packages_list = list(packages.values())
    data = {
        'packages': packages_list
    }
    return render(request, 'home.html', data)


# Package detail view
def package(request, package):
    package = Packages.objects.filter(name=package).first()  # Get the first match

    if package:
        data = {
            'package': package
        }
        return render(request, 'package.html', data)
    else:
        return render(request, '404.html', {'error': 'Package not found'})
