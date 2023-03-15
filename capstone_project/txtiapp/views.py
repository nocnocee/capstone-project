from django.shortcuts import render
from .stability_ai import generate_image
from django.http import HttpResponse
# we want to use the builtin form for our custom view for sign up
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm







# home view

def home(request):
    return render(request, 'home.html')



# generate image view

def generate_image_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        image_data = generate_image(text)
        if image_data:
            return HttpResponse(image_data, content_type='image/png')
    return render(request, 'app_name/generate_image.html')




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
