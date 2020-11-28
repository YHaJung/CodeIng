from rest_framework import serializers
from .models import Profile, Userinfo, Categoryinterest, Subcategoryinterest


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
       model = Profile
       fields = ['userpwd','name', 'email', 'phonenumber','isdeleted', 'isblocked', 'userinfo','level']


class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userinfo
        fields = ['nickname', 'isdeleted']



class CategoryinterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoryinterest
        fields = ['useridx', 'categoryidx','isdeleted']


class SubcategoryinterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoryinterest
        fields = ['useridx', 'subcategoryidx', 'isdeleted']

class CategoryinterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoryinterest
        fields = ['useridx', 'categoryidx', 'isdeleted']