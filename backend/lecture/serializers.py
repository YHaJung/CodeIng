from rest_framework import serializers
from .models import Lecture, Category, Review


class LectureSerializer(serializers.ModelSerializer):  # 객체 형식을 xml혹은 json 형식으로 바꿔줌
    class Meta:
        model = Lecture
        fields = ['lectureidx','lecturename', 'no_of_ratings', 'average_rating']


class CategorySerializer(serializers.ModelSerializer):  # 객체 형식을 xml혹은 json 형식으로 바꿔줌
    class Meta:
        model = Category
        fields = ['categoryidx','categoryname']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('lectureidx', 'totalrating', 'pricerating', 'teachingpowerrating', 'recommend','reviewidx')