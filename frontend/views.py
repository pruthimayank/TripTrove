from django.shortcuts import render, redirect
from .models import Packages, agent  

# Login view
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            agent_instance = agent.objects.get(email=email)
            
            if password == agent_instance.password:
                agent_data = agent.objects.filter(email=email)
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
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if agent.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        new_agent = agent(username=username, firstname=firstname, lastname=lastname, email=email, phone=phone, address=address ,password=password)
        new_agent.save()
        return redirect('login') 
    else:
        return render(request, 'signup.html')


# Home view
def home(request):
    user = request.session.get('user_data')
    login = request.session.get('login')

    packages = Packages.objects.all()
    packages_list = list(packages.values())
    if login == 'loggedin':
        data = {
            'user': request.session.get('user_data'),
            'login': 'loggedin',
            'packages': packages_list
        }
        return render(request, 'home.html', data)
    else:
        data = {
            'user': request.session.get('user_data'),
            'login': 'notloggedin',
            'packages': packages_list
        }
        return render(request, 'home.html', data)

# Package detail view
def package(request, package):
    user = request.session.get('user_data')
    login = request.session.get('login')

    package = Packages.objects.filter(name=package).first()
    if login == 'loggedin':
        if package:
            data = {
                'user': request.session.get('user_data'),
                'login': 'loggedin',
                'package': package
            }
            return render(request, 'package.html', data)
        else:
            return render(request, '404.html', {'error': 'Package not found'})
    else:
        if package:
            data = {
                'user': request.session.get('user_data'),
                'login': 'notloggedin',
                'package': package
            }
            return render(request, 'package.html', data)
        else:
            return render(request, '404.html', {'error': 'Package not found'})

def packages(request):
    user = request.session.get('user_data')
    login = request.session.get('login')
    
    packages = Packages.objects.all()
    packages_list = list(packages.values())
    if login == 'loggedin':
        data={
            'user': request.session.get('user_data'),
            'login': 'loggedin',
            'packages': packages_list
        }
        return render(request, 'packages.html', data)
    else:
        data = {
            'user': request.session.get('user_data'),
            'login': 'notloggedin',
            'packages': packages_list
        }
        return render(request, 'packages.html', data)
    
def bookings(request):
    user = request.session.get('user_data')
    login = request.session.get('login')
    
    if login == 'loggedin':
        data={
            'user': request.session.get('user_data'),
            'login': 'loggedin'
        }
        return render(request, 'bookings.html', data)
    else:
        data = {
            'user': request.session.get('user_data'),
            'login': 'notloggedin'
        }
        return render(request, 'bookings.html', data)

def about(request):
    user = request.session.get('user_data')
    login = request.session.get('login')
    
    if login == 'loggedin':
        data={
            'user': request.session.get('user_data'),
            'login': 'loggedin'
        }
        return render(request, 'about.html', data)
    else:
        data = {
            'user': request.session.get('user_data'),
            'login': 'notloggedin'
        }
        return render(request, 'about.html', data)
    
def logout(request):
    request.session.flush()
    return redirect('login')