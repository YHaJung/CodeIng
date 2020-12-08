from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from review.views import wordcloud

urlpatterns = [
    # path('lectures/<int:pk>/qna/<int:qnaIdx>/comment/<int:commentIdx>',comment_detail),
    path('reviews_wordcloud/<int:pk>/', wordcloud),
]
