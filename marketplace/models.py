from django.db import models
from django.contrib.auth.models import User

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=500)
    rating = models.FloatField(default=0.0)
    job_count = models.IntegerField(default=0)
    reliability_score = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    is_new = models.BooleanField(default=True)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avatar = models.CharField(max_length=200, default='https://picsum.photos/100')
    
    def __str__(self):
        return self.user.username

class Job(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
