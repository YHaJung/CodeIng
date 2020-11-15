from django.urls import path, include

from .views import check_email, sign_up, google_login

urlpatterns = [
    path('check-email',check_email),
    path('user', sign_up),
    path('google',google_login)

]
