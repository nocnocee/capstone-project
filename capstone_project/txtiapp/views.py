from django.shortcuts import render

def home(request):
    return render(request, 'app_name/home.html')


# Create your views here.
