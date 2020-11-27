from rest_framework import serializers
from .models import Profile, Userinfo, Categoryinterest, Subcategoryinterest

#원래 모델
#class ProfileSerializer(serializers.ModelSerializer):
#    class Meta:
#       model = Profile
#        fields = ['userpwd', 'gender','name', 'birthday', 'email', 'phonenumber','school',
#                  'job', 'major', 'level', 'isdeleted', 'isblocked']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
       model = Profile
       fields = ['userpwd','name', 'email', 'phonenumber',
                   'isdeleted', 'isblocked', 'level']

#원래
#class UserinfoSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Userinfo
#        fields = ['profileimg', 'nickname', 'isdeleted']

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