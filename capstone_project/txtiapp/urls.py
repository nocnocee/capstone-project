from django.urls import path
from . import views

urlpatterns = [
    # your other URL routes here
    path('generate-image/', views.generate_image_view, name='generate_image'),
]
