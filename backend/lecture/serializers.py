from rest_framework import serializers
from .models import Lecture, Category, Qna, Review, Comment, Userinfo, Commentimage, Qnaimage, Reviewpros, Reviewcons, \
    Favoritesite, Favoritelecture


class LectureSerializer(serializers.ModelSerializer):  # 객체 형식을 xml혹은 json 형식으로 바꿔줌
    class Meta:
        model = Lecture
        fields = ['lectureidx', 'lecturename', 'no_of_ratings', 'average_rating']


class CategorySerializer(serializers.ModelSerializer):  # 객체 형식을 xml혹은 json 형식으로 바꿔줌
    class Meta:
        model = Category
        fields = ['categoryidx', 'categoryname']


class QnaSerializer(serializers.ModelSerializer):  # 객체 형식을 xml혹은 json 형식으로 바꿔줌
    class Meta:
        model = Qna
        fields = ['title', 'qnades', 'userinfo', 'lecture']

class QnaimageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qnaimage
        fields = ['imgurl','qna','isdeleted']


class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userinfo
        fields = ['useridx']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['commentidx','commentdes','qna','userinfo','parentidx', 'isdeleted']


class CommentimageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commentimage
        fields = ['imageurl','comment','isdeleted']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['lectureidx', 'totalrating', 'pricerating', 'teachingpowerrating', 'recommend', 'improvement', 'isdeleted', 'profile']

class ReviewprosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewpros
        fields = ['review', 'pros', 'isdeleted']

class ReviewconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewcons
        fields = ['review', 'cons', 'isdeleted']

class FavoritesiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoritesite
        fields = ['user', 'siteinfo', 'isdeleted']

class FavoritelectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoritelecture
        fields = ['user', 'lecture', 'isdeleted']