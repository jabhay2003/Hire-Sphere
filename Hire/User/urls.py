from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('company_register/', views.company_register, name='company_register'),
    path('company_login/', views.company_login, name='company_login'),
    path('post_job/', views.post_job, name='post_job'),
    path('job/<int:jobid>/apply/', views.apply_now, name='apply_now'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('contact/', views.contact, name='contact'),
    path('my_resume/', views.my_resume, name='my_resume'),
    path('applications/', views.applications, name='applications'),
    path('delete_application/<int:applicationid>/', views.delete_application, name='delete_application'),
    #path('job_details/', views.job_details, name='job_details'),
    path('job_details/<int:jobid>/', views.job_details, name='job_details'),
    path('jobs/', views.jobs, name='jobs'),
    path('search/', views.search, name="search"),
    path('view_applications/', views.view_applications, name="view_applications"),
    path('accept-application/<int:applicationid>/', views.accept_application, name='accept_application'),
    path('reject-application/<int:applicationid>/', views.reject_application, name='reject_application'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
