from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', obtain_auth_token),
    path('', include('lecture.urls')),
    path('user', include('user.urls')) # 로그인 / 회원 가입

]
