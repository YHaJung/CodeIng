from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

#from api.views import MovieViewSet, ReviewViewSet, UserViewSet
from . import views

router = routers.DefaultRouter()
#router.register('movies', MovieViewSet)
#router.register('reviews', ReviewViewSet)
#router.register('users', UserViewSet)

urlpatterns = [
    # path('review/', views.review_list, name='review_list'),
    # path('', views.movie_list, name='movie_list'),
    path('', include(router.urls)),
    # url(r'^api/tutorials$', views.tutorial_list),
    # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    url(r'^api/get_suggestions$', views.get_suggestions)

    # path('reviews/<int:pk>', views.review_detail, name='review_detail'),
    # path('Movie/', views.movie_list, name='movie_list'),
    # path('Movie/<int:pk>', views.movie_detail, name='movie_detail'),
    # path('Movie/<int:pk>/add_review/', views.add_review, name='add_review'),
    # path('accounts/logout/', views.logout_view, name='logout_view'),
    # path('accounts/register/', views.SignUp.as_view(), name='signup'),
    # path('get_suggestions/', views.get_suggestions, name='get_suggestions'),

]
