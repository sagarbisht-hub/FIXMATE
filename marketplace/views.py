from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Worker, Job
import random
import string

def landing_page(request):
    return render(request, 'landing.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Find user by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'Email not found. Please sign up first.')
    
    return render(request, 'login.html')

def signup_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Validate name - only letters and spaces allowed
        if not all(c.isalpha() or c.isspace() for c in name):
            messages.error(request, 'Name should only contain letters and spaces, no numbers or special characters.')
            return render(request, 'signup.html')
        
        # Split name into first and last name
        name_parts = name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create username from first name (letters only)
        username = ''.join(c for c in first_name.lower() if c.isalpha())
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please login.')
            return redirect('login')
        
        # If username exists, add letters from last name or make it unique
        if User.objects.filter(username=username).exists():
            if last_name:
                username = username + ''.join(c for c in last_name.lower() if c.isalpha())[:3]
            if User.objects.filter(username=username).exists():
                # Add suffix with letters only
                import string
                suffix = ''.join(random.choices(string.ascii_lowercase, k=3))
                username = username + suffix
        
        # Create user with name
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Create worker if role is worker
        if role == 'WORKER':
            Worker.objects.create(
                user=user,
                skills='General',
                location='Downtown',
                reliability_score=80,
                rating=0.0,
                job_count=0,
                is_new=True,
                earnings=0
            )
        
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    user = request.user
    
    # check if worker
    try:
        worker = Worker.objects.get(user=user)
        jobs = Job.objects.filter(worker=worker)
        return render(request, 'worker_dashboard.html', {'worker': worker, 'jobs': jobs})
    except Worker.DoesNotExist:
        pass
    
    # check if admin
    if user.is_staff:
        workers = Worker.objects.all()
        jobs = Job.objects.all()
        return render(request, 'admin_dashboard.html', {'workers': workers, 'jobs': jobs})
    
    # regular user - check if they have any jobs
    jobs = Job.objects.filter(user=user)
    
    # If no jobs, redirect to job request form
    if not jobs.exists():
        return redirect('create_job_form')
    
    # If has jobs, show tracking dashboard
    workers = Worker.objects.all()
    return render(request, 'user_dashboard.html', {'jobs': jobs, 'workers': workers})

@login_required
def create_job_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        urgency = request.POST.get('urgency')
        location = request.POST.get('location', 'Downtown')
        
        # AI matching simulation
        workers = Worker.objects.filter(skills__icontains=category).order_by('-reliability_score')
        recommended_worker = workers.first() if workers.exists() else None
        
        # price calculation
        base_price = 100
        if urgency == 'high':
            base_price = 150
        elif urgency == 'low':
            base_price = 80
        
        price = base_price + random.randint(-20, 30)
        
        job = Job.objects.create(
            title=title,
            description=description,
            category=category,
            urgency=urgency,
            location=location,
            user=request.user,
            worker=recommended_worker,
            price=price,
            status='assigned' if recommended_worker else 'pending'
        )
        
        messages.success(request, f'Job request submitted! Matched with {recommended_worker.user.first_name if recommended_worker else "pending"}')
        return redirect('dashboard')
    
    return render(request, 'job_request_form.html')

@login_required
def create_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        urgency = request.POST.get('urgency')
        location = request.POST.get('location', 'Downtown')
        
        # AI matching simulation
        workers = Worker.objects.filter(skills__icontains=category).order_by('-reliability_score')
        recommended_worker = workers.first() if workers.exists() else None
        
        # price calculation
        base_price = 100
        if urgency == 'high':
            base_price = 150
        elif urgency == 'low':
            base_price = 80
        
        price = base_price + random.randint(-20, 30)
        
        job = Job.objects.create(
            title=title,
            description=description,
            category=category,
            urgency=urgency,
            location=location,
            user=request.user,
            worker=recommended_worker,
            price=price,
            status='assigned' if recommended_worker else 'pending'
        )
        
        messages.success(request, f'Job created! Matched with {recommended_worker.user.first_name if recommended_worker else "pending"}')
        return redirect('dashboard')
    
    return redirect('dashboard')

def help_page(request):
    return render(request, 'help.html')

def report_issue(request):
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        email = request.POST.get('email')
        
        # In production, save to database and send email notification
        # For now, just show success message
        messages.success(request, f'Issue reported successfully! We will contact you at {email} within 24 hours.')
        return redirect('report_issue')
    
    return render(request, 'report_issue.html')

@login_required
def help_page(request):
    return render(request, 'help.html')

@login_required
def delete_job(request, job_id):
    if request.method == 'POST':
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            job.delete()
            messages.success(request, 'Job deleted successfully!')
        except Job.DoesNotExist:
            messages.error(request, 'Job not found or you do not have permission to delete it.')
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('landing')
