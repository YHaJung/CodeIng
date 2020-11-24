from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import class_list, myclass_list

urlpatterns = [
    path('classes', class_list),
    path('my-classes', myclass_list),



]
