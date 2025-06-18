from django.contrib import messages
from django.shortcuts import redirect,render,HttpResponse,get_object_or_404
from django.contrib.auth import logout
from .models import UserProfile, Contact, JobPost, Company, Application
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.


def index(request):
    latest_jobs = JobPost.objects.order_by('-posting_date')[:8]  # In descending order 8 latest jobs
    recent_jobs = JobPost.objects.order_by('-posting_date')[2:16]  # In descending order 14 recent jobs
    return render(request, "index.html", {'latest_jobs': latest_jobs, 'recent_jobs': recent_jobs})


"""def index(request):
    latest_jobs = JobPost.objects.order_by('-posting_date')[:8]  # In descending order 8 latest jobs
    recent_jobs = JobPost.objects.order_by('-posting_date')[2:16]  # In descending order 14 recent jobs
    categories = [
        {'name': 'Python Developer', 'icon': 'icon-bargraph'},
        {'name': 'Data Science & Analytics', 'icon': 'icon-tools'},
        {'name': 'Accounting & Consulting', 'icon': 'ti-briefcase'},
        {'name': 'Writing & Translations', 'icon': 'ti-ruler-pencil'},
        {'name': 'Sales & Marketing', 'icon': 'icon-briefcase'},
        {'name': 'Graphics & Design', 'icon': 'icon-wine'},
        {'name': 'Digital Marketing', 'icon': 'ti-world'},
        {'name': 'Education & Training', 'icon': 'ti-desktop'},
    ]

    for category in categories:
        category['count'] = JobPost.objects.filter(job_title=category['name']).count()
    return render(request, "index.html", {'latest_jobs': latest_jobs, 'recent_jobs': recent_jobs,'categories': categories})"""


def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('c_password')
        phone = request.POST.get('phone')


        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
        elif UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
        else:
            user = UserProfile(username=username, email=email, password=make_password(password), phone=phone)
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('index')

    return render(request, 'register.html')


"""def user_login(request):
    if request.method == 'POST':
        # Manually getting the form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Basic validation to ensure fields are not empty
        if not email or not password:
            messages.error(request, "Both fields are required.")
        else:
            # Try to authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                # If authentication is successful, log the user in
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('index')  # Redirect to the home page or a success page
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'index.html')"""


def company_register(request):
    if request.method == 'POST':
        companyname = request.POST.get('name')
        company_email = request.POST.get('company_email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('c_password')
        phone = request.POST.get('phone')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif Company.objects.filter(companyname=companyname).exists():
            messages.error(request, 'Company already Exists. Please choose a different one.')
        elif Company.objects.filter(company_email=company_email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
        else:
            user = Company(companyname=companyname, company_email=company_email, password=make_password(password), phone=phone)
            user.save()
            messages.success(request, 'Company Registration successful!')
            return redirect('index')

    return render(request, "company_register.html")


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session['email'] = user.email
                messages.success(request, 'Login successful!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'index.html')


def company_login(request):
    if request.method == 'POST':
        company_email = request.POST.get('company_email')
        password = request.POST.get('password')
        try:
            company = Company.objects.get(company_email=company_email)
            if check_password(password, company.password):
                request.session['company_email'] = company.company_email
                messages.success(request, 'Company Login successful!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
        except Company.DoesNotExist:
            messages.error(request, 'Company does not exist.')
    return render(request, 'index.html')


def post_job(request):
    if 'company_email' not in request.session:
        messages.info(request, 'You have to Company Login for Post a Job.....')
        return redirect('index')

    if request.method == 'POST':
        job_experience = request.POST['job_experience']
        degree = request.POST['degree']
        website = request.POST['website']
        open_position = request.POST['open_position']
        job_type = request.POST['job_type']
        job_package = request.POST['job_package']
        job_requirement = request.POST['job_requirement']
        job_skill = request.POST['job_skill']
        job_title = request.POST['job_title']
        job_desc = request.POST['job_desc']
        job_location = request.POST['job_location']
        company_logo = request.FILES.get('company_logo', None)
        
        company = Company.objects.get(company_email=request.session['company_email'])
        
        JobPost.objects.create(
            company=company,
            job_experience=job_experience,
            degree=degree,
            website=website,
            open_position=open_position,
            job_type=job_type,
            job_package=job_package,
            job_requirement=job_requirement,
            job_skill=job_skill,
            job_title=job_title,
            job_desc=job_desc,
            job_location=job_location,
            company_logo=company_logo
        )
        messages.success(request, 'Post successful!')
    return render(request, 'post_job.html')


def apply_now(request, jobid):
    job = get_object_or_404(JobPost, jobid=jobid)
    
    # Retrieve email from session
    email = request.session.get('email')
    if email:
        # Get the user profile using the email
        user_profile = get_object_or_404(UserProfile, email=email)
        
        # Create and save the application
        application = Application(JobPost=job, UserProfile=user_profile)
        application.save()
        messages.success(request, 'Application submitted successfully!')
        
        # Redirect to the applications page
        return redirect('applications')
    else:
        # If the user is not logged in, show a warning
        messages.warning(request, 'You need to User log in to apply for a job.')
        return redirect('index')


def user_logout(request):
    if 'email' in request.session:
        del request.session['email']
    logout(request)
    if 'company_email' in request.session:
        del request.session['company_email']
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('index')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not email or not subject or not message:
            messages.error(request, 'All fields are required.')
        else:
            # Save the contact message to the database
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')

    return render(request, "contact.html")


def my_resume(request):
    return render(request, "my_resume.html")


def applications(request):
    #allPosts = Application.objects.all()
    # Retrieve email from session
    email = request.session.get('email')
    if email:
        # Filter applications by the logged-in user's email
        allPosts = Application.objects.filter(UserProfile__email=email)
        if not allPosts:
            # If no applications are found, show a warning message
            messages.info(request, 'You have not applied to any job yet Apply Now!.....')
            return redirect('jobs')
    else:
         # If the user is not logged in, show a warning
        allPosts = []
        messages.warning(request, 'You need to User log in to view your applications.')
        return redirect('index')
    return render(request, 'applications.html', {'allPosts': allPosts})


def delete_application(request, applicationid):
    application = get_object_or_404(Application, applicationid=applicationid)
    application.delete()
    messages.success(request, 'Application deleted successfully!')
    return redirect('applications') 


def job_details(request, jobid):
    # Fetch the job post from the database using the jobid
    job = get_object_or_404(JobPost, jobid=jobid)
    
    # Find similar jobs based on category or location
    similar_jobs = JobPost.objects.filter(job_title=job.job_title).exclude(jobid=job.jobid)  

    return render(request, 'job_details.html', {'job': job, 'similar_jobs': similar_jobs})


"""def job_details(request):
    return render(request, "job_details.html")"""


def jobs(request):
    allPosts = JobPost.objects.all()
    return render(request, 'jobs.html', {'allPosts': allPosts})


def search(request):
    query = request.GET.get('query')
    location = request.GET.get('location')
    category = request.GET.get('category')
    
    # Filter the JobPost objects based on query, location, and category
    allPosts = JobPost.objects.all()
    if query:
        allPosts = allPosts.filter(job_title__icontains=query)
    if location and location != 'All Country':
        allPosts = allPosts.filter(job_location__icontains=location)
    if category and category != 'Show All':
        allPosts = allPosts.filter(job_title__icontains=category)
    
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found. Please refine your query.')
    
    params = {'allPosts': allPosts}
    return render(request, 'jobs.html', params)



def view_applications(request):
    company_email = request.session.get('company_email')
    
    if company_email:
        company_application = get_object_or_404(Company, company_email=company_email)
        
        job_posts = JobPost.objects.filter(company=company_application)
        job_applications = Application.objects.filter(JobPost__in=job_posts)
        
        context = {
            'job_applications': job_applications,
        }
        
        return render(request, 'view_applications.html', context)
    
    else:
        messages.warning(request, 'Please log in to view your applications.')
        return redirect('index')




def accept_application(request, applicationid):
    application = get_object_or_404(Application, applicationid=applicationid)
    
    # Check if the current user is the service provider (for job applications)
    if application.JobPost and application.JobPost.company.company_email == request.session.get('company_email'):
        application.status = 'ACCEPTED'
        application.save()
        messages.success(request, 'Application accepted successfully.')
    
    else:
        messages.warning(request, 'You are not authorized to accept this application.')
    
    return redirect('view_applications')

def reject_application(request, applicationid):
    application = get_object_or_404(Application, applicationid=applicationid)
    
    # Check if the current user is the service provider (for job applications)
    if application.JobPost and application.JobPost.company.company_email == request.session.get('company_email'):
        application.status = 'REJECTED'
        application.save()
        messages.success(request, 'Application rejected successfully.')
    
    
    else:
        messages.warning(request, 'You are not authorized to reject this application.')
    
    return redirect('view_applications')




"""def search(request):
    query=request.GET['query']
    allPosts= JobPost.objects.filter(job_title__icontains=query)
    if allPosts.count()==0:
        messages.warning(request, 'No search results found. Please refine your query.')
    params={'allPosts': allPosts}
    return render(request, 'jobs.html', params)"""