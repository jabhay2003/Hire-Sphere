from django.utils import timezone
from django.db import models

# Create your models here.

# User Model
class UserProfile(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

# Company Model
class Company(models.Model):
    companyid = models.AutoField(primary_key=True)
    companyname=models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    company_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.companyname
   
# Company Post the Job Model
class JobPost(models.Model):
    jobid = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, to_field='companyid', on_delete=models.CASCADE)
    job_experience = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    website = models.CharField(max_length=128)
    open_position = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    job_package = models.CharField(max_length=100)
    job_requirement=models.CharField(max_length=225)
    job_skill = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    job_desc = models.CharField(max_length=200)
    job_location = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    posting_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job_title
    
# Application Model
class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    applicationid = models.AutoField(primary_key=True)
    JobPost = models.ForeignKey(JobPost, to_field='jobid', on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, to_field='userid', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(default=timezone.now)