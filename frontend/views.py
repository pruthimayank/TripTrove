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
                agent_data = agent.objects.filter(username=username)
                request.session['user_data'] = list(agent_data.values())[0]
                request.session['login'] = "loggedin"
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
    # print(request.session.get('user_data'))
    login = request.session.get('login')

    packages = Packages.objects.all()
    packages_list = list(packages.values())
    if login == 'loggedin':
        data = {
            'login': 'loggedin',
            'packages': packages_list
        }
        return render(request, 'home.html', data)
    else:
        data = {
            'login': 'notloggedin',
            'packages': packages_list
        }
        return render(request, 'home.html', data)

# Package detail view
def package(request, package):
    login = request.session.get('login')

    package = Packages.objects.filter(name=package).first()
    if login == 'loggedin':
        if package:
            data = {
                'login': 'loggedin',
                'package': package
            }
            return render(request, 'package.html', data)
        else:
            return render(request, '404.html', {'error': 'Package not found'})
    else:
        if package:
            data = {
                'login': 'notloggedin',
                'package': package
            }
            return render(request, 'package.html', data)
        else:
            return render(request, '404.html', {'error': 'Package not found'})

def packages(request):
    login = request.session.get('login')
    
    packages = Packages.objects.all()
    packages_list = list(packages.values())
    if login == 'loggedin':
        data={
            'login': 'loggedin',
            'packages': packages_list
        }
        return render(request, 'packages.html', data)
    else:
        data = {
            'login': 'notloggedin',
            'packages': packages_list
        }
        return render(request, 'packages.html', data)
    
def bookings(request):
    login = request.session.get('login')
    
    if login == 'loggedin':
        data={
            'login': 'loggedin'
        }
        return render(request, 'bookings.html', data)
    else:
        data = {
            'login': 'notloggedin'
        }
        return render(request, 'bookings.html', data)

def about(request):
    login = request.session.get('login')
    
    if login == 'loggedin':
        data={
            'login': 'loggedin'
        }
        return render(request, 'about.html', data)
    else:
        data = {
            'login': 'notloggedin'
        }
        return render(request, 'about.html', data)
    
def logout(request):
    request.session.flush()
    return redirect('login')