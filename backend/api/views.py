import decimal

# from django.utils import simplejson as json
import simplejson as json
import json
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
#



from rest_framework.utils import json
from collections import Counter
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
import pickle
import joblib


from celery.schedules import crontab
from celery.task import periodic_task
# Create your views here.

# 이후 코드
from lecture.models import Lecture, Review, Profile, Lecturecategory, Categoryinterest, Subcategoryinterest, Category, \
    Subcategory

# 데이터 저장
from lecture.views import for_exception

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def generate_binary():
    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    all_category_ids = list(map(lambda x: x.categoryidx, Category.objects.all()))
    all_subcategory_ids = list(map(lambda x: x.subcategoryidx, Subcategory.objects.all()))
    all_lectures = list(map(lambda x: x.lectureidx, Lecture.objects.all()))
    all_categorys = len(all_category_ids) + len(all_subcategory_ids)
    # print(all_categorys)
    num_users = len(list(all_user_names))
    num_lectures = len(list(all_lectures))
    # userInterest = np.zeros([num_users, all_categorys])
    userInterest = -np.ones([num_users, all_categorys])
    lectureData = -np.ones([num_lectures, all_categorys])
        # np.zeros([num_lectures, all_categorys])

    for i in range(num_users):
        user_subcategory_interests = Subcategoryinterest.objects.filter(useridx=all_user_names[i].useridx)
        user_category_interests = Categoryinterest.objects.filter(useridx=all_user_names[i].useridx)
        for user_category_interest in user_category_interests:
            # userInterest_m[i, user_category_interest.categoryidx-1] = 1
          
            userInterest[i, user_category_interest.categoryidx.categoryidx - 1] = 1
        for user_subcategory_interest in user_subcategory_interests:
            # userInterest_m[i, 11+ user_subcategory_interest.subcategoryidx] = 1
            userInterest[i, 11 + user_subcategory_interest.subcategoryidx.subcategoryidx] = 1
    filename = 'knn_models/query.pkl'
    pickle.dump(userInterest, open(filename, 'wb'))

    for i in range(num_lectures):
        all_lecturecategory_ids = Lecturecategory.objects.filter(lecture=all_lectures[i])
        for lecturecategory in all_lecturecategory_ids:
            lectureData[i, lecturecategory.categoryidx - 1] = 1
            lectureData[i, 11 + lecturecategory.subcategory.subcategoryidx] = 2
    filename = 'knn_models/data.pkl'
    pickle.dump(lectureData, open(filename, 'wb'))

@api_view(['GET'])
def recommend_save(request):
    generate_binary()
    data = pickle.load(open('knn_models/data.pkl', 'rb'))
    querys = pickle.load(open('knn_models/query.pkl', 'rb'))
    num_users, _ = querys.shape
    num_lectures, _ = data.shape
    nneigh = 10
    recommend = np.dot(querys, data.T)
    # recommend = np.zeros([num_users, nneigh])

    # for queryidx, query in enumerate(querys):
    #     # print(findkneigh(query, data))
    #     recommend[queryidx] = findkneigh(query, data)[:nneigh]

    filename = 'knn_models/recommend.pkl'
    pickle.dump(recommend, open(filename, 'wb'))
    print('recommend_saved')
    response = {'message' : 'recommend saved'}
    return JsonResponse(response, safe=False)

@api_view(['GET'])
def CBRS(request, pk=None):

    try:
        data = pickle.load(open('knn_models/data.pkl', 'rb'))
        querys = pickle.load(open('knn_models/query.pkl', 'rb'))
        recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
        selectIdx = int(request.GET.get('selectIdx', '1'))
        nneigh = 5
        krecommend = np.argsort(-recommend[int(pk)])[5*selectIdx-5:nneigh*selectIdx]

        # print("query: {}".format(querys[int(pk)]))
        # print("recommend: {}".format(recommend[int(pk)]))
        #
        # for lectureid in krecommend:
        #     print('{}'.format(data[int(lectureid)]))
        # for lectureid in recommend[pk]:
        #     print('{}'.format(data[int(lectureid)]))

        # response = {'hello' : 'hello'}
        # return JsonResponse(response, safe=False)
        overview_list = []
        overview_dict = {}
        overview_dict['isSuccess'] = 'true'
        overview_dict['code'] = 200
        overview_dict['message'] = '추천컨텐츠 조회 성공'
        # .flatten()[x]
        overview2 = list(map(
            lambda x: Lecture.objects.filter(lectureidx=x)
                .values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level').distinct()
            , krecommend))
        for i in overview2:
            overview_list.append(
                dict([('lectureIdx', i[0]['lectureidx']),
                      ('lectureName', i[0]['lecturename']),
                      ('thumbUrl', i[0]['thumburl']),
                      ('lecturer', i[0]['lecturer']),
                      ('level', decimal.Decimal(i[0]['level']))
                      ]))
        overview_dict['result'] = overview_list
        return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:

        return for_exception()



# @api_view(['GET'])
# def CBRS(request, pk=None):
#    data = pickle.load(open('knn_models/data.pkl', 'rb'))
#    querys = pickle.load(open('knn_models/query.pkl', 'rb'))
#    recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
#    nneigh = 10
#    krecommend =np.argsort(-recommend[int(pk)])[:nneigh]
#
#    # print("query: {}".format(querys[int(pk)]))
#    # print("recommend: {}".format(recommend[int(pk)]))
#    #
#    # for lectureid in krecommend:
#    #     print('{}'.format(data[int(lectureid)]))
#    # for lectureid in recommend[pk]:
#    #     print('{}'.format(data[int(lectureid)]))
#
#    # response = {'hello' : 'hello'}
#    # return JsonResponse(response, safe=False)
#    overview_list = []
#    overview_dict = {}
#    overview_dict['isSuccess'] = 'true'
#    overview_dict['code'] = 200
#    overview_dict['message'] = '추천컨텐츠 조회 성공'
#    # .flatten()[x]
#    overview2 = list(map(
#        lambda x: Lecture.objects.filter(lectureidx=x)
#        .values('lectureidx', 'lecturename','thumburl', 'lecturer','level').distinct()
#        , krecommend  ))
#    for i in overview2:
#        overview_list.append(
#            dict([('lectureIdx', i[0]['lectureidx']),
#                  ('lectureName', i[0]['lecturename']),
#                  ('thumbUrl', i[0]['thumburl']),
#                  ('lecturer', i[0]['lecturer']),
#                  ('level', decimal.Decimal(i[0]['level']))
#                  ]))
#    overview_dict['result'] = overview_list
#    return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
#    return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

   # response = {'hello','hello'}
   # return JsonResponse(response, safe=False)


@api_view(['GET'])
def CBRSlist(request, pk=None):
   data = pickle.load(open('knn_models/data.pkl', 'rb'))
   querys = pickle.load(open('knn_models/query.pkl', 'rb'))
   recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
   nneigh = 25
   krecommend =np.argsort(-recommend[int(pk)])[:nneigh]
   # print("query: {}".format(querys[int(pk)]))
   # print("recommend: {}".format(recommend[int(pk)]))

   # for lectureid in krecommend:
   #     print('{}'.format(data[int(lectureid)]))
   # for lectureid in recommend[pk]:
   #     print('{}'.format(data[int(lectureid)]))

   # response = {'hello' : 'hello'}
   # return JsonResponse(response, safe=False)
   overview_list = []
   overview_dict = {}
   overview_dict['isSuccess'] = 'true'
   overview_dict['code'] = 200
   overview_dict['message'] = '추천컨텐츠 조회 성공'
   # .flatten()[x]
   overview2 = list(map(
       lambda x: Lecture.objects.filter(lectureidx=x)
       .values('lectureidx', 'lecturename','thumburl', 'lecturer','level').distinct()
       , krecommend  ))
   for i in overview2:
       overview_list.append(
           dict([('lectureIdx', i[0]['lectureidx']),
                 ('lectureName', i[0]['lecturename']),
                 ('thumbUrl', i[0]['thumburl']),
                 ('lecturer', i[0]['lecturer']),
                 ('level', decimal.Decimal(i[0]['level']))
                 ]))
   overview_dict['result'] = overview_list
   # use_decimal = True,
   print(overview_dict)
   return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
   return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

@api_view(['GET'])
def Poprs(request, pk=None):
    try:
       # data = pickle.load(open('knn_models/data.pkl', 'rb'))
       # querys = pickle.load(open('knn_models/query.pkl', 'rb'))
        recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
        selectIdx = int(request.GET.get('selectIdx', '1'))
        nneigh = 5
        krecommend =np.argsort(-recommend)[5*selectIdx-5:nneigh*selectIdx]
        cnt = Counter(krecommend.flatten()) # age_C데이터를 카운트한다.
        krecommend =  cnt.most_common()[:10]

        krecommend = [x for x, _ in krecommend]
        overview_list = []
        overview_dict = {}
        overview_dict['isSuccess'] = 'true'
        overview_dict['code'] = 200
        overview_dict['message'] = '초기 추천컨텐츠 조회 성공'
        # .flatten()[x]
        overview2 = list(map(
           lambda x : Lecture.objects.filter(lectureidx=x)
           .values('lectureidx', 'lecturename','thumburl', 'lecturer','level').distinct()
           , krecommend ))

        for i in overview2:
           overview_list.append(
               dict([('lectureIdx', i[0]['lectureidx']),
                     ('lectureName', i[0]['lecturename']),
                     ('thumbUrl', i[0]['thumburl']),
                     ('lecturer', i[0]['lecturer']),
                     ('level', decimal.Decimal(i[0]['level']))
                     ]))

        overview_dict['result'] = overview_list
        return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)

        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

    except Exception:
        return for_exception()

@api_view(['GET'])
def Poprslist(request, pk=None):
   # data = pickle.load(open('knn_models/data.pkl', 'rb'))
   # querys = pickle.load(open('knn_models/query.pkl', 'rb'))
   recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
   nneigh = 25
   krecommend =np.argsort(-recommend)[:nneigh]
   cnt = Counter(krecommend.flatten()) # age_C데이터를 카운트한다.
   krecommend =  cnt.most_common()[:10]

   krecommend = [x for x, _ in krecommend]
   overview_list = []
   overview_dict = {}
   overview_dict['isSuccess'] = 'true'
   overview_dict['code'] = 200
   overview_dict['message'] = '초기 추천컨텐츠 조회 성공'
   # .flatten()[x]
   overview2 = list(map(
       lambda x : Lecture.objects.filter(lectureidx=x)
       .values('lectureidx', 'lecturename','thumburl', 'lecturer','level').distinct()
       , krecommend ))
   for i in overview2:
       overview_list.append(
           dict([('lectureIdx', i[0]['lectureidx']),
                 ('lectureName', i[0]['lecturename']),
                 ('thumbUrl', i[0]['thumburl']),
                 ('lecturer', i[0]['lecturer']),
                 ('level', decimal.Decimal(i[0]['level']))
                 ]))
   overview_dict['result'] = overview_list
   return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
   return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

def generate_rating():
    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    all_lecture_ids = list(map(lambda x: x.lectureidx, Lecture.objects.all()))
    num_users = len(list(all_user_names))
    num_lectures = max(all_lecture_ids)
    # user_item = np.zeros([num_users, num_lectures])
    user_item = pd.DataFrame(columns=range(num_lectures),index=all_user_names)
    for i in range(num_users):
        profile = get_object_or_404(Profile, userinfo=all_user_names[i])
        user_reviews = Review.objects.filter(profile=profile)
        for user_review in user_reviews:
            user_item.loc[i, user_review.lectureidx_id-1] = user_review.totalrating
    user_item.fillna(0, inplace=True)
    if user_item.shape[0] < 7:
        ubcf_model_knn= NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=user_item.shape[0])
        ubcf_model_knn.fit(user_item.values)
    else:
        ubcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        ubcf_model_knn.fit(user_item.values)
    filename = 'knn_models/ubcf_knn_model.pkl'
    pickle.dump(ubcf_model_knn, open(filename, 'wb'))

    item_user = user_item.T
    # item_user = pd.DataFrame(columns=all_user_names,index=range(all_lecture_ids))
    if user_item.shape[0] < 7:
        ibcf_model_knn= NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=item_user .shape[0])
        ibcf_model_knn.fit(item_user.values)
    else:
        ibcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        ibcf_model_knn.fit(item_user.values)
    filename = 'knn_models/ibcf_knn_model.pkl'
    pickle.dump(ibcf_model_knn, open(filename, 'wb'))

    filename = 'knn_models/user_item_rating.pkl'
    pickle.dump(user_item, open(filename, 'wb'))

    filename = 'knn_models/item_user_rating.pkl'
    pickle.dump(item_user, open(filename, 'wb'))

# Final version
# 하루에 한번 Model 바꾸기

# @periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
# @periodic_task(run_every=crontab(hour=4, minute=30))
@periodic_task(run_every=crontab(hour=11, minute=22))
def CREATE_MODEL(request, pk=None):
    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    all_lecture_ids = list(map(lambda x: x.lectureidx, Lecture.objects.all()))
    num_users = len(list(all_user_names))
    num_lectures = max(all_lecture_ids)
    # user_item = np.zeros([num_users, num_lectures])
    user_item = pd.DataFrame(columns=range(num_lectures),index=all_user_names)
    for i in range(num_users):
        profile = get_object_or_404(Profile, userinfo=all_user_names[i])
        user_reviews = Review.objects.filter(profile=profile)
        for user_review in user_reviews:
            user_item.loc[i, user_review.lectureidx_id-1] = user_review.totalrating
    user_item.fillna(0, inplace=True)
    if user_item.shape[0] < 7:
        ubcf_model_knn= NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=user_item.shape[0])
        ubcf_model_knn.fit(user_item.values)
    else:
        ubcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        ubcf_model_knn.fit(user_item.values)
    filename = 'knn_models/ubcf_knn_model.pkl'
    pickle.dump(ubcf_model_knn, open(filename, 'wb'))
    filename = 'knn_models/user_item_rating.pkl'
    pickle.dump(user_item, open(filename, 'wb'))

    item_user = user_item.T
    if item_user.shape[0] < 7:
        ibcf_model_knn= NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=item_user.shape[0])
        ibcf_model_knn.fit(item_user.values)
    else:
        ibcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        ibcf_model_knn.fit(item_user.values)
    filename = 'knn_models/ibcf_knn_model.pkl'
    pickle.dump(ibcf_model_knn, open(filename, 'wb'))
    filename = 'knn_models/item_user_rating.pkl'
    pickle.dump(item_user, open(filename, 'wb'))
    
    response = {'message' : 'model saved'}
    return JsonResponse(response, safe=False)


# 추천 시스템
@api_view(['GET'])
def KNN_IBCF(request, pk=None):
    # aws s3 파일 저장하는 곳
    # 하루에 한번에 하던지
    # 바로 가져옴
    model_knn = pickle.load(open('knn_models/ubcf_knn_model.pkl', 'rb'))
    lectureid = int(pk)
    item_user = pickle.load(open('knn_models/item_user_rating.pkl', 'rb'))
    print(item_user)
    print(model_knn)
    distances, indices = model_knn.kneighbors(item_user[lectureid].values.reshape(1, -1), return_distance=True)
    # distances, indices = model_knn.kneighbors(mo.iloc[lectureid, :].values.reshape(1, -1), return_distance=True)

    # print(indices)

    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # print('ok2')
    overview2 = list(map(
        lambda x: Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('lectureidx', 'lecturename',
                                                                                 'thumburl', 'lecturer',
                                                                                 'level')
        , range(0, len(distances.flatten()))))
    # .distinct().order_by('lectureidx')
    for i in overview2:
        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', i[0]['thumburl']),
                  ('lecturer', i[0]['lecturer']),
                  ('level', decimal.Decimal(i[0]['level']))
                  ]))
    overview_dict['result'] = overview_list
    return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
    return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

@api_view(['GET'])
def KNN_UBCF(request, pk=None):
    # aws s3 파일 저장하는 곳
    # 하루에 한번에 하던지
    # 바로 가져옴
    ubcf_model_knn = pickle.load(open('knn_models/ubcf_knn_model.pkl', 'rb'))
    user_item = pickle.load(open('knn_models/user_item_rating.pkl', 'rb'))
    userid = int(pk)

    distances, indices = ubcf_model_knn.kneighbors(user_item.iloc[userid, :].values.reshape(1, -1), return_distance=True)

    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # print('ok2')
    overview2 = list(map(
        lambda x: Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('lectureidx', 'lecturename',
                                                                                 'thumburl', 'lecturer',
                                                                                 'level')
        , range(0, len(distances.flatten()))))
    # .distinct().order_by('lectureidx')
    for i in overview2:
        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', i[0]['thumburl']),
                  ('lecturer', i[0]['lecturer']),
                  ('level', decimal.Decimal(i[0]['level']))
                  ]))
    overview_dict['result'] = overview_list
    return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
    return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

