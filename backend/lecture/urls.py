from django.urls import path, include
from .views import lecture_list, lectures_ranking, ranking_overview, \
    lecture_detail, review_list, qna_list, qna_detail, comment_list, comment_detail, \
    review_detail, favorite_sites, favorite_lectures, my_reviews, my_qnas, my_comments, subcategory_list, overall_ranking, category_list
from rest_framework.authtoken.views import obtain_auth_token


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
    path('overall-ranking', overall_ranking),
    path('favorite-sites',favorite_sites),
    path('favorite-lectures', favorite_lectures),
    path('my-reviews', my_reviews),
    path('my-qnas', my_qnas),
    path('my-comments', my_comments),
    path('subcategory-list',subcategory_list),
    path('category-list', category_list),

    path('auth/', obtain_auth_token),  #post로 아이디/비번을 보내면 해당 사용자의 토큰을 넘겨준다

]
