from django.urls import path, include

from .views import check_email,sign_up

urlpatterns = [
    path('check-email',check_email),
    path('', sign_up),

]
