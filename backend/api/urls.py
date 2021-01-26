from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

# from api.views import MovieViewSet, ReviewViewSet, UserViewSet
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    url(r'^api/create_model/$', views.create_model),
    url(r'^api/recommend_save/$', views.recommend_save),

    url(r'^api/knn_ibcf/(?P<pk>\d+)$', views.KNN_IBCF),
    url(r'^api/knn_ubcf/(?P<pk>\d+)$', views.KNN_UBCF),

    # 쓰이는 api
    path('api/user_recommend', views.CBRS),
    path('api/user_recommendlist', views.CBRSlist),
    url(r'^api/recommend/$', views.Poprs),
    url(r'^api/recommendlist', views.Poprslist),

    url(r'^api/matrixfactorization_model', views.create_matrixFactorization_IBCF),
    path('api/<int:pk>/matrixfactorization_IBCF', views.sim_movies_to),
    path('api/<int:pk>/matrixfactorization_UBCF', views.recommend_movies_to),
    path('api/<int:pk>/item_recommend', views.itemcbs),

]
