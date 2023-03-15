from django.shortcuts import render
from django.http import HttpResponse
# we want to use the builtin form for our custom view for sign up
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .stability_ai import generate_image as kuvasana
from .models import Image
from .models import GeneratedImage
from .forms import GeneratedImageForm

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
        # import base64
        # encoded = base64.b64encode(image).decode('utf-8')
        from io import BytesIO
        import base64
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        encoded = base64.b64encode(image_bytes).decode()


        # render the image in the browser
        return render(request, 'generate_image.html', {'image': encoded})

    # render the form
    return render(request, 'generate_image.html')


# saved image view

def generate_png():
    # your code to generate the PNG file here
    # ...

    # save the generated PNG file to a temporary file
    tmp_file_path = os.path.join(settings.BASE_DIR, 'tmp', 'generated.png')
    with open(tmp_file_path, 'wb') as f:
        f.write(png_bytes)

    # open the saved PNG file with Pillow to get the image size and format
    with Image.open(tmp_file_path) as img:
        width, height = img.size
        format = img.format

    # set the image_path attribute of the GeneratedImage model
    generated_image = GeneratedImage()
    generated_image.image_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', 'file.png')
    generated_image.save()

    # move the temporary file to the media directory
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'generated_images'), exist_ok=True)
    os.replace(tmp_file_path, generated_image.image_path)

    return generated_image


# history view
def history(request):
    images = GeneratedImage.objects.all()
    return render(request, 'history.html', {'images': images})



# edit and delete image view
def edit_generated_image(request, pk):
    generated_image = get_object_or_404(GeneratedImage, pk=pk)
    if request.method == 'POST':
        form = GeneratedImageForm(request.POST, request.FILES, instance=generated_image)
        if form.is_valid():
            form.save()
            return redirect('history')
    else:
        form = GeneratedImageForm(instance=generated_image)
    return render(request, 'edit_generated_image.html', {'form': form})

def delete_image(request, image_id):
    image = get_object_or_404(GeneratedImage, id=image_id)
    image.delete()
    return redirect('history')



# about view

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
