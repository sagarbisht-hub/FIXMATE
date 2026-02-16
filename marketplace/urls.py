from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job-request/', views.create_job_form, name='create_job_form'),
    path('create-job/', views.create_job, name='create_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('help/', views.help_page, name='help'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('logout/', views.logout_view, name='logout'),
]
