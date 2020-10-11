from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', obtain_auth_token),
    path('', include('lecture.urls')),
    path('user/', include('user.urls')), # 로그인 / 회원 가입
    path('accounts/', include('allauth.urls')),



]
