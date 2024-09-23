from django.shortcuts import render, redirect
from .models import Packages, agent, BlogPost  # Assuming 'agent' is the correct model for agents
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Login view
def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if agent.objects.filter(phone=phone).exists():
            try:
                agent_instance = agent.objects.get(phone=phone)
                if password == agent_instance.password:
                    agent_data = agent.objects.filter(phone=phone)
                    request.session['user_data'] = list(agent_data.values())[0]
                    request.session['login'] = "loggedin"
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'error': 'Invalid password'})
            except agent.DoesNotExist:
                return render(request, 'login.html', {'error': 'No such agent'})
        else:
            return render(request, 'login.html', {'error': 'Phone number does not exist'})
    
    return render(request, 'login.html')

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if agent.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})
        
        if agent.objects.filter(phone=phone).exists():
            return render(request, 'signup.html', {'error': 'Phone number already taken'})

        new_agent = agent(username=username, email=email, phone=phone, password=password)
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
        data = {
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

    if login == 'loggedin' and user:
        agent_instance = agent.objects.get(id=user['id'])
        booking_history = agent_instance.bookinghistory if agent_instance.bookinghistory else []
        current_date = datetime.now().date()

        for booking in booking_history:
            booking['slot_start'] = datetime.strptime(booking['slot_start'], '%Y-%m-%d').date()
            booking['slot_end'] = datetime.strptime(booking['slot_end'], '%Y-%m-%d').date()

        return render(request, 'bookings.html', {
            'user': user,
            'login': login,
            'current_date': current_date,
            'booking_history': booking_history
        })
    else:
        return redirect('login')

def about(request):
    user = request.session.get('user_data')
    login = request.session.get('login')
    
    if login == 'loggedin':
        data = {
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

def policies(request):
    user = request.session.get('user_data')
    login = request.session.get('login')
    
    if login == 'loggedin':
        data = {
            'user': request.session.get('user_data'),
            'login': 'loggedin'
        }
        return render(request, 'policies.html', data)
    else:
        data = {
            'user': request.session.get('user_data'),
            'login': 'notloggedin'
        }
        return render(request, 'policies.html', data)

def terms(request):
    user = request.session.get('user_data')
    login = request.session.get('login')
    
    if login == 'loggedin':
        data = {
            'user': request.session.get('user_data'),
            'login': 'loggedin'
        }
        return render(request, 'terms.html', data)
    else:
        data = {
            'user': request.session.get('user_data'),
            'login': 'notloggedin'
        }
        return render(request, 'terms.html', data)

def logout(request):
    request.session.flush()
    return redirect('login')

# Handle booking - REST API view
@csrf_exempt
def handle_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            slot_start = data.get('slot_start')
            slot_end = data.get('slot_end')
            total_amount = data.get('total_amount')

            # Ensure all fields are present
            if not (first_name and last_name and slot_start and slot_end and total_amount):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            # Convert slot_start and slot_end to date objects
            try:
                slot_start_date = datetime.strptime(slot_start, '%Y-%m-%d').date()
                slot_end_date = datetime.strptime(slot_end, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid date format'}, status=400)

            # Ensure the user is logged in
            user_data = request.session.get('user_data')
            if not user_data:
                return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=400)

            # Retrieve the agent instance
            agent_instance = agent.objects.get(id=user_data['id'])

            # Get the existing booking history (if available)
            booking_history = agent_instance.bookinghistory if agent_instance.bookinghistory else []

            # Add the new booking
            new_booking = {
                'first_name': first_name,
                'last_name': last_name,
                'slot_start': slot_start_date.isoformat(),
                'slot_end': slot_end_date.isoformat(),
                'total_amount': total_amount
            }

            booking_history.append(new_booking)

            # Save updated booking history
            agent_instance.bookinghistory = booking_history
            agent_instance.save()

            return JsonResponse({'status': 'success', 'message': 'Booking confirmed'})

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'blog_list.html', context)
