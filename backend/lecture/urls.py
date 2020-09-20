from django.urls import path, include
from rest_framework import routers
from .views import LectureViewSet, snippet_list, snippet_detail, lecture_list, lectures_ranking, ranking_overview, lecture_detail,review_list
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('', LectureViewSet)


urlpatterns = [
    path('lectures/<int:pk>/reviews',review_list),
    path('lectures/<int:pk>',lecture_detail),
    path('ranking-overview',ranking_overview),
    path('lectures-ranking',lectures_ranking),
    path('lectures',lecture_list),
    path('category', snippet_list),
    path('category/<int:pk>', snippet_detail),
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),  #post로 아이디/비번을 보내면 해당 사용자의 토큰을 넘겨준다

]
