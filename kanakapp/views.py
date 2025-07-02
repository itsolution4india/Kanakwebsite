import random
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import User

def generate_otp():
    return str(random.randint(100000, 999999))

def send_sms(mobile, otp):
    try:
        url = "http://www.smsdealnow.com/api/pushsms"
        params = {
            'user': 'harishit',
            'authkey': '92yFICCNaH0A',
            'sender': 'ITSTON',
            'mobile': mobile,
            'text': f'Dear Customer, your IT app Login one time password is {otp} thanks ITsol',
            'rpt': '1',
            'output': 'json',
            'entityid': '1701160576859005802',
            'templateid': '1007990679727833850'
        }
        response = requests.get(url, params=params)
        return response.status_code == 200
    except:
        return False

def landing_page(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        location = request.POST.get('location')
        subscribe_sms = request.POST.get('subscribe_sms') == 'on'
        subscribe_email = request.POST.get('subscribe_email') == 'on'
        subscribe_voice = request.POST.get('subscribe_voice') == 'on'
        
        # Check if user already exists
        if User.objects.filter(number=number).exists():
            messages.error(request, 'User with this number already exists!')
            return render(request, 'register.html')
        
        # Generate OTP
        otp = generate_otp()
        
        # Create user
        user = User.objects.create(
            name=name,
            number=number,
            location=location,
            subscribe_sms=subscribe_sms,
            subscribe_email=subscribe_email,
            subscribe_voice=subscribe_voice,
            otp=otp
        )
        
        # Send OTP
        if send_sms(number, otp):
            request.session['user_id'] = user.id
            request.session['registration'] = True
            messages.success(request, 'OTP sent successfully!')
            return redirect('verify_otp')
        else:
            messages.error(request, 'Failed to send OTP. Please try again.')
            user.delete()
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        
        try:
            user = User.objects.get(number=number)
            if not user.is_verified:
                messages.error(request, 'Please complete registration first.')
                return render(request, 'login.html')
            
            # Generate new OTP for login
            otp = generate_otp()
            user.otp = otp
            user.save()
            
            # Send OTP
            if send_sms(number, otp):
                request.session['user_id'] = user.id
                request.session['registration'] = False
                messages.success(request, 'OTP sent successfully!')
                return redirect('verify_otp')
            else:
                messages.error(request, 'Failed to send OTP. Please try again.')
        
        except User.DoesNotExist:
            messages.error(request, 'User not found. Please register first.')
    
    return render(request, 'login.html')

def verify_otp(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('user_id')
        is_registration = request.session.get('registration', False)
        
        try:
            user = User.objects.get(id=user_id)
            if user.otp == entered_otp:
                if is_registration:
                    user.is_verified = True
                    user.save()
                    messages.success(request, 'Registration completed successfully!')
                else:
                    messages.success(request, 'Login successful!')
                
                request.session['logged_in_user'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')
    
    return render(request, 'verify_otp.html')

def dashboard(request):
    if 'logged_in_user' not in request.session:
        return redirect('login')
    
    user = User.objects.get(id=request.session['logged_in_user'])
    return render(request, 'dashboard.html', {'user': user})

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('landing_page')