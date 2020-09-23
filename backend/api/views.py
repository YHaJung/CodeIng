import decimal
import simplejson as json
from django.shortcuts import render

# Create your views here.
import datetime
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# from rest_framework.utils import json

# from api.form import LectureReviewForm
# from api.serializers import UserSerializer, LectureReviewSerializer, LectureSerializer
# from .models import LectureReview, Lecture

from surprise import SVD
import pandas as pd
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
from surprise.model_selection import cross_validate

# from .form import ReviewForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.views import generic
from django.contrib.auth.forms import UserCreationForm

import pandas as pd
import numpy as np
import scipy as sp

from sklearn.neighbors import NearestNeighbors

# Create your views here.

# 이후 코드
from lecture.models import Lecture, Review, Profile, Lecturecategory, Categoryinterest, Subcategoryinterest, Category, \
    Subcategory
from lecture.serializers import LectureSerializer, ReviewSerializer


@api_view(['GET'])
def CBRS(request):
    num_reviews = Review.objects.count()
    # all_user_names = list(map(lambda x: x.userinfo, Categoryinterest.objects.only("userIdx")))
    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    # print('all users',all_user_names[0])
    # print(Review.objects.only("lectureidx")[1].pricerating)
    # subcategory 71개 maincategory 12개
    # all_lecture_ids = set(map(lambda x: x.lectureidx, Lecturecategory.objects.only("lectureidx")))
    all_category_ids = list(map(lambda x: x.categoryname, Category.objects.all()))
    # print(Category.objects.all())
    # print('====================')
    # print(type(all_category_ids))
    all_subcategory_ids = list(map(lambda x: x.subcategoryname, Subcategory.objects.all()))
    # print(type(all_subcategory_ids))
    all_categorys = all_category_ids + all_subcategory_ids
    # print(all_categorys)
    num_users = len(list(all_user_names))
    lectureRatings_m = sp.sparse.dok_matrix((num_users, len(all_categorys) + 1), dtype=np.float32)
    for i in range(num_users):
        #     # profile = Profile.objects.filter(userinfo=all_user_names[i])
        #     profile = get_object_or_404(Profile, userinfo=all_user_names[i])
        #     print(all_user_names[i].useridx)
        user_subcategory_interest = Subcategoryinterest.objects.filter(useridx=all_user_names[i].useridx)
        user_category_interest = Categoryinterest.objects.filter(useridx=all_user_names[i].useridx)
        # print(user_category_interest)
    #     for user_review in user_reviews:
    #         lectureRatings_m[i, user_review.lectureidx] = user_review.totalrating
    # lectureRatings = lectureRatings_m.transpose()
    # coo = lectureRatings.tocoo(copy=False)
    # df = pd.DataFrame({'lectures': coo.row, 'users': coo.col, 'rating': coo.data}
    #                   )[['lectures', 'users', 'rating']].sort_values(['lectures', 'users']
    #                                                                ).reset_index(drop=True)
    # mo = df.pivot_table(index=['lectures'], columns=['users'], values='rating')
    # mo.fillna(0, inplace=True)
    # # print('3')
    # selected = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # if mo.shape[0] < 7:
    #     model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=mo.shape[0])
    #     model_knn.fit(mo.values)
    # else:
    #     model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
    #     model_knn.fit(mo.values)
    # context = model_knn.kneighbors([selected])
    response = {'message': 'sussccess'}
    return JsonResponse(response, safe=False)


@api_view(['GET'])
def KNN_IBCF(request, pk=None):
    num_reviews = Review.objects.count()
    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    all_lecture_ids = set(map(lambda x: x.lectureidx, Review.objects.only("lectureidx")))
    num_users = len(list(all_user_names))
    lectureRatings_m = sp.sparse.dok_matrix((num_users, max(all_lecture_ids) + 1), dtype=np.float32)
    for i in range(num_users):
        # print(i)
        # print(Review.objects.filter(profile=all_user_names[i]))
        # profile = Profile.objects.filter(userinfo=all_user_names[i])
        profile = get_object_or_404(Profile, userinfo=all_user_names[i])
        user_reviews = Review.objects.filter(profile=profile)

        for user_review in user_reviews:
            lectureRatings_m[i, user_review.lectureidx] = user_review.totalrating
    lectureRatings = lectureRatings_m.transpose()
    coo = lectureRatings.tocoo(copy=False)
    df = pd.DataFrame({'lectures': coo.row, 'users': coo.col, 'rating': coo.data}
                      )[['lectures', 'users', 'rating']].sort_values(['lectures', 'users']
                                                                     ).reset_index(drop=True)
    mo = df.pivot_table(index=['lectures'], columns=['users'], values='rating')
    mo.fillna(0, inplace=True)
    if mo.shape[0] < 7:
        model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=mo.shape[0])
        model_knn.fit(mo.values)
    else:
        model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        model_knn.fit(mo.values)
    userid = int(pk)
    distances, indices = model_knn.kneighbors(mo.iloc[userid, :].values.reshape(1, -1), return_distance=True)
    # context = list(map(lambda x: Lecture.objects.filter(id=indices.flatten()[x]).values_list('id','title'), range(0, len(distances.flatten()))))
    # for x in range(0, len(distances.flatten())):
    #     # context = Movie.objects.filter(id=indices.flatten()[x]).values()
    #     # print(json.dumps(context))
    #     data = serializers.serialize('json', Movie.objects.filter(id=indices.flatten()[x]), fields=('id','title'))
    #     print(data)

    # context = list(map(lambda x: serializers.serialize('json', Lecture.objects.filter(lectureidx=indices.flatten()[x]),
    #                 fields=('lectureidx','lecturename','thumburl','lecturer','level')),
    #                    range(0, len(distances.flatten())) ))

    # print('5')
    response = {'results': 'show'}
    # print(type(context))
    # print(context)
    # context_json = serializers.serialize('json', context)
    # return JsonResponse(response, status=status.HTTP_200_OK)
    # return HttpResponse(json.dumps(context), content_type='application/json')
    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # context = list(map(lambda x: Lecture.objects.filter(id=indices.flatten()[x]).values_list('id', 'title'),
    #                    range(0, len(distances.flatten()))))
    # categoryIdx = int(request.GET.get('categoryIdx', '1'))
    # overview = Lecturecategory.objects.select_related('lecture')
    overview2 = list(map(
        lambda x: Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('lectureidx', 'lecturename',
                                                                                 'thumburl', 'lecturer',
                                                                                 'level').distinct().order_by(
            'lectureidx')[:5]
        , range(0, len(distances.flatten()))))
    for i in overview2:
        # print(i[0])
        # print(i[0].lectureidx)
        # print(i[0]['lectureidx'], i[0]['lecturename'])
        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', i[0]['thumburl']),
                  ('lecturer', i[0]['lecturer']),
                  ('level', decimal.Decimal(i[0]['level']))
                  ]))
    overview_dict['result'] = overview_list
    return_value = json.dumps(overview_dict,indent=4, use_decimal=True, ensure_ascii=False)
    # use_decimal = True,
    return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)
    # return JsonResponse(context, safe=False)


@api_view(['GET'])
def get_con(request):
    response = {'results': 'show'}
    return JsonResponse(response, safe=False)


# 이후 강의

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()[:8]
    serializer_class = LectureSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_lecture(self, request, pk=None):
        if 'rating' in request.data:
            # movie = Movie.objects.get(id=pk)
            lecture = get_object_or_404(Lecture, id=pk)
            rating = request.data['rating']
            user = request.user
            # print(user)
            # user = User.objects.get(id=1)
            try:
                # try:
                review = Review.objects.get(user=user.id, lecture=lecture.id)
                print(review)
                # review = get_object_or_404(Review, user_id=user.id, movie=movie.id)
                review.rating = rating
                review.save()
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
                # except:
                #     review = None
            except:
                print('create')
                review = Review(user=user, lecture=lecture, rating=rating, pub_date=timezone.now())
                # Review.objects.create(user_id=user.id, movie=movie.id, rating=rating, pub_date=timezone.now())
                # review.rating = rating
                review.save()
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide ratings'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': "You can't update review like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': "You can't create review like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
