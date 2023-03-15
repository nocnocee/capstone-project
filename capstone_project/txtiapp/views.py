from django.shortcuts import render
from django.http import HttpResponse
# we want to use the builtin form for our custom view for sign up
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .stability_ai import generate_image as kuvasana

# AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
# AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
# S3_BUCKET = settings.S3_BUCKET
# S3_BASE_URL = settings.S3_BASE_URL


# home view

def home(request):
    return render(request, 'home.html')



# generate image view

def generate_image(request):
    if request.method == 'POST':
        # get the text from the form
        text = request.POST['text']
        # generate an image
        image = kuvasana(text)
        # save the image
        # render the image in the browser
        # import base64
        # encoded = base64.b64encode(image).decode('utf-8')
        from io import BytesIO
        import base64
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        encoded = base64.b64encode(image_bytes).decode()
        return render(request, 'generate_image.html', {'image': encoded})

    # render the form
    return render(request, 'generate_image.html')




# Create your views here.

def about(request):
    return render(request, 'about.html')



# login view
def login(request):
    error_message = ''
    if request.method == 'POST':
        # perform authentication
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login credentials'
    # handle GET request with an empty login form
    form = AuthenticationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registeration/login.html', context)



# view for signup
def signup(request):
    # this view is going to be like our class based views
    # because this is going to be able to handle a GET and a POST request
    error_message = ''
    if request.method == 'POST':
        # this is how to create a user form object that includes data from the browser
        form = UserCreationForm(request.POST)
        # now we check validity of the form, and handle our success and error situations
        if form.is_valid():
            # we'll add the user to the database
            user = form.save()
            # then we'll log the user in
            auth_login(request, user)
            # redirect to our index page
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # a bad POST or GET request will render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registeration/signup.html', context)

# view for logout
def logout(request):
    auth_logout(request)
    return redirect('home')
