from django.urls import path
from . import views
from .views import history, delete_image


urlpatterns = [
    # your other URL routes here
    path('', views.home, name='home'),

    # URL pattern for the signup view
    path('accounts/signup/', views.signup, name='signup'),

    # URL pattern for the login view
    path('accounts/login/', views.login, name='login'),

    # URL pattern for about page
    path('about/', views.about, name='about'),

    # URL pattern for the logout view
    path('accounts/logout/', views.logout, name='logout'),

    # URL pattern for the generate image view
    path('generate_image/', views.generate_image, name='generate_image'),

    # URL pattern for history view
    path('history/', views.history, name='history'),

    # URL pattern for edit, delete 
    path('history/', history, name='history'),
    path('delete/<int:image_id>/', delete_image, name='delete_image'),

]
