from django.urls import path, include
from rest_framework import routers
from .views import LectureViewSet, lecture_list, lectures_ranking, ranking_overview, \
    lecture_detail, review_list, qna_list, qna_detail, comment_list, comment_detail, \
    review_detail
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('', LectureViewSet)


urlpatterns = [
    path('lectures/<int:pk>/qna/<int:qnaIdx>/comment/<int:commentIdx>',comment_detail),
    path('lectures/<int:pk>/qna/<int:qnaIdx>/comment',comment_list),
    path('lectures/<int:pk>/qna/<int:qnaIdx>',qna_detail),
    path('lectures/<int:pk>/qna',qna_list),
    path('lectures/<int:pk>/review/<int:reviewIdx>',review_detail),
    path('lectures/<int:pk>/review',review_list),
    path('lectures/<int:pk>',lecture_detail),
    path('ranking-overview',ranking_overview),
    path('lectures-ranking',lectures_ranking),
    path('lectures',lecture_list),
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),  #post로 아이디/비번을 보내면 해당 사용자의 토큰을 넘겨준다

]
