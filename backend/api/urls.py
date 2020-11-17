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
    # <int:pk>
    url(r'^api/KNN_IBCF/(?P<pk>\d+)$', views.KNN_IBCF),
    url(r'^api/KNN_UBCF/(?P<pk>\d+)$', views.KNN_UBCF),
    url(r'^api/recommend_save/$', views.recommend_save),
    # url(r'^api/(?P<pk>\d+)$', views.CBRS),
    path('api/<int:pk>/recommend', views.CBRS),
    path('api/<int:pk>/recommendlist', views.CBRSlist),
    url(r'^api/recommend/$', views.Poprs),
    url(r'^api/recommendlist', views.Poprslist),
    url(r'^api/CREATE_MODEL/$', views.create_model),
    url(r'^api/matrixfactorization_model', views.create_matrixFactorization_IBCF),
    path('api/<int:pk>/matrixfactorization_IBCF', views.sim_movies_to),
    path('api/<int:pk>/matrixfactorization_UBCF', views.recommend_movies_to),
]
