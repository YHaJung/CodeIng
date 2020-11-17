from django.urls import path, include

from .views import check_email, sign_up, google_login, login

urlpatterns = [
    path('check-email',check_email),
    path('user', sign_up),
    path('login', login),
    path('google',google_login)

]
