from django.shortcuts import render
from .stability_ai import generate_image
from django.http import HttpResponse


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



# register view

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')




# Create your views here.
