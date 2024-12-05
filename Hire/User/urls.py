from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('my_resume/', views.my_resume, name='my_resume'),
    path('applications/', views.applications, name='applications'),
    path('job_details/', views.job_details, name='job_details'),
    path('jobs/', views.jobs, name='jobs'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
