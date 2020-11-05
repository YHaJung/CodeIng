from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import book_list

urlpatterns = [

    path('books',book_list),

]
