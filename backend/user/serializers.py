from rest_framework import serializers
from .models import Profile, Userinfo, Categoryinterest, Subcategoryinterest


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['userpwd', 'gender','name', 'birthday', 'email', 'phonenumber','school',
                  'job', 'major', 'level', 'isdeleted', 'isblocked']


class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userinfo
        fields = ['profileimg', 'nickname', 'isdeleted']


class CategoryinterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoryinterest
        fields = ['useridx', 'categoryidx','isdeleted']


class SubcategoryinterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoryinterest
        fields = ['useridx', 'subcategoryidx', 'isdeleted']