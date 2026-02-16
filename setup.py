#!/usr/bin/env python
"""
Setup script for FixMate AI Django project
Run this after installing requirements.txt
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixmate.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Worker

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user
    if not User.objects.filter(email='admin@gmail.com').exists():
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.save()
        print("✓ Admin: admin@gmail.com / admin")
    
    # Create sample client
    if not User.objects.filter(email='client@gmail.com').exists():
        client = User.objects.create_user('client', 'client@gmail.com', 'client')
        client.first_name = 'Alex'
        client.last_name = 'Johnson'
        client.save()
        print("✓ Client: client@gmail.com / client")
    
    # Create sample workers
    workers_data = [
        {
            'username': 'sarah',
            'email': 'sarah@gmail.com',
            'password': 'sarah',
            'first_name': 'Sarah',
            'last_name': 'Miller',
            'skills': 'Plumbing, Heating',
            'rating': 4.9,
            'job_count': 156,
            'reliability_score': 98,
            'location': 'Downtown',
            'is_new': False,
            'earnings': 4500
        },
        {
            'username': 'marcus',
            'email': 'marcus@gmail.com',
            'password': 'marcus',
            'first_name': 'Marcus',
            'last_name': 'Chen',
            'skills': 'Electrical, Smart Home',
            'rating': 4.7,
            'job_count': 89,
            'reliability_score': 95,
            'location': 'North Side',
            'is_new': False,
            'earnings': 3200
        },
        {
            'username': 'elena',
            'email': 'elena@gmail.com',
            'password': 'elena',
            'first_name': 'Elena',
            'last_name': 'Rodriguez',
            'skills': 'Carpentry, General Repairs',
            'rating': 5.0,
            'job_count': 12,
            'reliability_score': 100,
            'location': 'West End',
            'is_new': True,
            'earnings': 800
        }
    ]
    
    for worker_data in workers_data:
        if not User.objects.filter(email=worker_data['email']).exists():
            user = User.objects.create_user(
                username=worker_data['username'],
                email=worker_data['email'],
                password=worker_data['password']
            )
            user.first_name = worker_data['first_name']
            user.last_name = worker_data['last_name']
            user.save()
            
            Worker.objects.create(
                user=user,
                skills=worker_data['skills'],
                rating=worker_data['rating'],
                job_count=worker_data['job_count'],
                reliability_score=worker_data['reliability_score'],
                location=worker_data['location'],
                is_new=worker_data['is_new'],
                earnings=worker_data['earnings']
            )
            print(f"✓ Worker: {worker_data['email']} / {worker_data['password']}")
    
    print("\n✅ Setup complete!")
    print("\nLogin credentials:")
    print("  Admin:  admin@gmail.com  / admin")
    print("  Client: client@gmail.com / client")
    print("  Worker: sarah@gmail.com  / sarah")
    print("  Worker: marcus@gmail.com / marcus")
    print("  Worker: elena@gmail.com  / elena")

if __name__ == '__main__':
    create_sample_data()
