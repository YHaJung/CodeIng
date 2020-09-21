from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

# from api.views import MovieViewSet, ReviewViewSet, UserViewSet
from . import views

router = routers.DefaultRouter()
# router.register('movies', MovieViewSet)
# router.register('reviews', ReviewViewSet)
# router.register('users', UserViewSet)


urlpatterns = [
    # path('review/', views.review_list, name='review_list'),
    # path('', views.movie_list, name='movie_list'),
    path('', include(router.urls)),
    # url(r'^api/tutorials$', views.tutorial_list),
    # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    url(r'^api/get_suggestions$', views.get_suggestions),
    url(r'^api/get_con$', views.get_con)
    # path('reviews/<int:pk>', views.review_detail, name='review_detail'),
]
