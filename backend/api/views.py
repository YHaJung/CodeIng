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
from scipy.sparse.linalg import svds
from sklearn.metrics.pairwise import cosine_similarity

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
    Subcategory, Siteinfo

# 데이터 저장
from lecture.views import for_exception, login_decorator


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
    response = {'message': 'recommend saved'}
    return JsonResponse(response, safe=False)


@api_view(['GET'])
@login_decorator
def CBRS(request):
    try:
        pk = request.user.userinfo.useridx
        data = pickle.load(open('knn_models/data.pkl', 'rb'))
        querys = pickle.load(open('knn_models/query.pkl', 'rb'))


        recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
        selectIdx = int(request.GET.get('selectIdx', '1'))
        nneigh = 5
        # print(pk)
        # print(recommend[pk])
        # print(np.argsort(-recommend[int(pk)])[:5] )
        krecommend = np.argsort(-recommend[pk])[5 * selectIdx - 5:nneigh * selectIdx]
        overview_list = []
        overview_dict = {}
        overview_dict['isSuccess'] = 'true'
        overview_dict['code'] = 200
        overview_dict['message'] = '추천컨텐츠 조회 성공'

        # .flatten()[x]
        # overview2 = list(map(
        #     lambda x: Lecture.objects.filter(lectureidx=x)
        #         .values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level', 'price', 'rating',
        #                 'siteinfo').distinct()
        #     , krecommend))
        # for i in overview2:
        #     overview_list.append(
        #         dict([('lectureIdx', i[0]['lectureidx']),
        #               ('lectureName', i[0]['lecturename']),
        #               ('thumbUrl', i[0]['thumburl']),
        #               ('lecturer', i[0]['lecturer']),
        #               ('level', decimal.Decimal(i[0]['level'])),
        #               ('price', decimal.Decimal(i[0]['price'])),
        #               ('rating', i[0]['rating']),
        #               ('siteinfo', i[0]['siteinfo']),
        #               ]))
        # print(krecommend)
        for lectureidx in krecommend:
            i = Lecture.objects.filter(lectureidx=lectureidx+1).values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level', 'price', 'rating', 'level__levelidx', 'level__levelname',
                    'siteinfo', 'siteinfo__logoimage').distinct()
            # sitename = Siteinfo.objects.select_related('sitename').get(siteidx=i[0]['siteinfo'])
            sitename = Siteinfo.objects.get(siteidx=i[0]['siteinfo']).sitename
            # print('sitename',Lecture.objects.select_related('siteinfo').filter(lectureidx=lectureidx))
            # sitename = Lecture.objects.select_related('siteinfo').get(lectureidx=lectureidx).sitename
            # # .values('sitename')
            # print(sitename)
            # decimal.Decimal(i[0]['price'])
            price = i[0]['price']
            if price == 0:
                price = 'free'
            elif price == -1:
                price = 'membership'
            else:
                price = format(price, ',')

            # 강의 썸네일 없을 경우
            thumbnail = i[0]['thumburl']
            if not thumbnail:
                thumbnail = i[0]['siteinfo__logoimage']


            overview_list.append(
                dict([('lectureIdx', i[0]['lectureidx']),
                      ('lectureName', i[0]['lecturename']),
                      ('thumbUrl', thumbnail),
                      ('lecturer', i[0]['lecturer']),
                      ('level', decimal.Decimal(i[0]['level'])),
                      ('price', price),
                      ('rating', i[0]['rating']),
                      ('siteinfo', sitename),
                      ('levelIdx', i[0]['level__levelidx']),
                      ('levelName', i[0]['level__levelname'])
                      ]))
        overview_dict['result'] = overview_list
        return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:

        return for_exception()


@api_view(['GET'])
@login_decorator
def CBRSlist(request):
    pk = request.user.userinfo.useridx
    data = pickle.load(open('knn_models/data.pkl', 'rb'))
    querys = pickle.load(open('knn_models/query.pkl', 'rb'))
    recommend = pickle.load(open('knn_models/recommend.pkl', 'rb'))
    nneigh = 25
    krecommend = np.argsort(-recommend[int(pk)])[:nneigh]
    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'

    # .flatten()[x]
    # overview2 = list(map(
    #     lambda x: Lecture.objects.filter(lectureidx=x)
    #         .values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level', 'price', 'rating',
    #                 'siteinfo').distinct()
    #     , krecommend))
    # for i in overview2:
    #     overview_list.append(
    #         dict([('lectureIdx', i[0]['lectureidx']),
    #               ('lectureName', i[0]['lecturename']),
    #               ('thumbUrl', i[0]['thumburl']),
    #               ('lecturer', i[0]['lecturer']),
    #               ('level', decimal.Decimal(i[0]['level'])),
    #               ('price', decimal.Decimal(i[0]['price'])),
    #               ('rating', i[0]['rating']),
    #               ('siteinfo', i[0]['siteinfo']),
    #               ]))
    for lectureidx in krecommend:
        i = Lecture.objects.filter(lectureidx=lectureidx+1).values('lectureidx', 'lecturename', 'thumburl', 'lecturer',
                                                                 'level', 'price', 'rating', 'level__levelidx', 'level__levelname',
                                                                 'siteinfo','siteinfo__logoimage').distinct()
        # sitename = Siteinfo.objects.select_related('sitename').get(siteidx=i[0]['siteinfo'])
        sitename = Siteinfo.objects.get(siteidx=i[0]['siteinfo']).sitename
        # print('sitename',Lecture.objects.select_related('siteinfo').filter(lectureidx=lectureidx))
        # sitename = Lecture.objects.select_related('siteinfo').get(lectureidx=lectureidx).sitename
        # # .values('sitename')
        # print(sitename)
        # decimal.Decimal(i[0]['price'])
        price = i[0]['price']
        if price == 0:
            price = 'free'
        elif price == -1:
            price = 'membership'


        # 강의 썸네일 없을 경우
        thumbnail = i[0]['thumburl']
        if not thumbnail:
            thumbnail = i[0]['siteinfo__logoimage']

        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', thumbnail),
                  ('lecturer', i[0]['lecturer']),
                  ('level', decimal.Decimal(i[0]['level'])),
                  ('price', price),
                  ('rating', i[0]['rating']),
                  ('siteName', sitename),
                  ('levelIdx', i[0]['level__levelidx']),
                  ('levelName', i[0]['level__levelname'])
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
        page = int(request.GET.get('page', '1'))
        if page <1:
            page =1

        krecommend = np.argsort(-recommend)[5 * selectIdx - 5:nneigh * selectIdx]

        cnt = Counter(krecommend.flatten())  # age_C데이터를 카운트한다.
        krecommend = cnt.most_common()[:10]
        # print(krecommend)
        krecommend = [x for x, _ in krecommend]

        overview_list = []
        overview_dict = {}
        overview_dict['isSuccess'] = 'true'
        overview_dict['code'] = 200
        overview_dict['message'] = '초기 추천컨텐츠 조회 성공'
        # .flatten()[x]
        # category_ranking = Lecturecategory.objects.filter(categoryidx=categoryIdx).select_related(
        #     'lecture').order_by('-lecture__rating')
        # overview2 = list(map(
        #     lambda x: Lecture.objects.filter(lectureidx=x)
        #         .values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level', 'price', 'rating',
        #                 'siteinfo').distinct()
        #     , krecommend))


        for lectureidx in krecommend[page * 5 - 5:page * 5]:
            i = Lecture.objects.filter(lectureidx=lectureidx).values('siteinfo__logoimage','lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level','level__levelname', 'price', 'rating',
                    'siteinfo').distinct()

            # sitename = Siteinfo.objects.select_related('sitename').get(siteidx=i[0]['siteinfo'])
            sitename = Siteinfo.objects.get(siteidx=i[0]['siteinfo']).sitename
            # print('sitename',Lecture.objects.select_related('siteinfo').filter(lectureidx=lectureidx))
            # sitename = Lecture.objects.select_related('siteinfo').get(lectureidx=lectureidx).sitename
            # # .values('sitename')
            # print(sitename)
            # decimal.Decimal(i[0]['price'])
            price = i[0]['price']
            if price == 0:
                price = 'free'
            elif price == -1:
                price = 'membership'

            # 강의 썸네일 없을 경우
            thumbnail = i[0]['thumburl']
            if not thumbnail:
                thumbnail = i[0]['siteinfo__logoimage']

            overview_list.append(
                dict([('lectureIdx', i[0]['lectureidx']),
                      ('lectureName', i[0]['lecturename']),
                      ('thumbUrl', thumbnail),
                      ('lecturer', i[0]['lecturer']),
                      ('levelIdx', int(decimal.Decimal(i[0]['level']))),
                      ('levelName', i[0]['level__levelname']),
                      ('price', price),
                      ('rating', i[0]['rating']),
                      ('siteName', sitename),
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
    krecommend = np.argsort(-recommend)[:nneigh]
    cnt = Counter(krecommend.flatten())  # age_C데이터를 카운트한다.
    krecommend = cnt.most_common()[:25]

    krecommend = [x for x, _ in krecommend]
    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '초기 추천컨텐츠 조회 성공'
    # .flatten()[x]
    # overview2 = list(map(
    #     lambda x: Lecture.objects.filter(lectureidx=x)
    #         .values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level', 'price', 'rating',
    #                 'siteinfo').distinct()
    #     , krecommend))
    # for i in overview2:
    #     overview_list.append(
    #         dict([('lectureIdx', i[0]['lectureidx']),
    #               ('lectureName', i[0]['lecturename']),
    #               ('thumbUrl', i[0]['thumburl']),
    #               ('lecturer', i[0]['lecturer']),
    #               ('level', decimal.Decimal(i[0]['level'])),
    #               ('price', decimal.Decimal(i[0]['price'])),
    #               ('rating', i[0]['rating']),
    #               ('siteinfo', i[0]['siteinfo']),
    #               ]))
    for lectureidx in krecommend:
        i = Lecture.objects.filter(lectureidx=lectureidx).values('siteinfo__logoimage','lectureidx', 'lecturename', 'thumburl', 'lecturer',
                                                                 'level', 'price', 'rating', 'level__levelname',
                                                                 'siteinfo').distinct()
        # sitename = Siteinfo.objects.select_related('sitename').get(siteidx=i[0]['siteinfo'])
        sitename = Siteinfo.objects.get(siteidx=i[0]['siteinfo']).sitename
        # print('sitename',Lecture.objects.select_related('siteinfo').filter(lectureidx=lectureidx))
        # sitename = Lecture.objects.select_related('siteinfo').get(lectureidx=lectureidx).sitename
        # # .values('sitename')
        # print(sitename)
        # decimal.Decimal(i[0]['price'])
        price = i[0]['price']
        if price == 0:
            price = 'free'
        elif price == -1:
            price = 'membership'

       # 강의 썸네일 없을 경우
        thumbnail = i[0]['thumburl']
        if not thumbnail:
            thumbnail = i[0]['siteinfo__logoimage']

        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', thumbnail),
                  ('lecturer', i[0]['lecturer']),
                  ('levelIdx', int(decimal.Decimal(i[0]['level']))),
                  ('levelName', i[0]['level__levelname']),
                  ('price', price),
                  ('rating', i[0]['rating']),
                  ('siteName', sitename),
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
    user_item = pd.DataFrame(columns=range(num_lectures), index=all_user_names)
    for i in range(num_users):
        profile = get_object_or_404(Profile, userinfo=all_user_names[i])
        user_reviews = Review.objects.filter(profile=profile)
        for user_review in user_reviews:
            user_item.loc[i, user_review.lectureidx_id - 1] = user_review.totalrating
    user_item.fillna(0, inplace=True)
    if user_item.shape[0] < 7:
        ubcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=user_item.shape[0])
        ubcf_model_knn.fit(user_item.values)
    else:
        ubcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        ubcf_model_knn.fit(user_item.values)
    filename = 'knn_models/ubcf_knn_model.pkl'
    pickle.dump(ubcf_model_knn, open(filename, 'wb'))

    item_user = user_item.T
    # item_user = pd.DataFrame(columns=all_user_names,index=range(all_lecture_ids))
    if user_item.shape[0] < 7:
        ibcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=item_user.shape[0])
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
def create_model(request, pk=None):
    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    all_lecture_ids = list(map(lambda x: x.lectureidx, Lecture.objects.all()))
    num_users = len(list(all_user_names))
    num_lectures = max(all_lecture_ids)
    # user_item = np.zeros([num_users, num_lectures])
    user_item = pd.DataFrame(columns=range(num_lectures), index=all_user_names)
    for i in range(num_users):
        profile = get_object_or_404(Profile, userinfo=all_user_names[i])
        user_reviews = Review.objects.filter(profile=profile)
        for user_review in user_reviews:
            user_item.loc[i, user_review.lectureidx_id - 1] = user_review.totalrating
    user_item.fillna(0, inplace=True)
    if user_item.shape[0] < 7:
        ubcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=user_item.shape[0])
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
        ibcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=item_user.shape[0])
        ibcf_model_knn.fit(item_user.values)
    else:
        ibcf_model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
        ibcf_model_knn.fit(item_user.values)
    filename = 'knn_models/ibcf_knn_model.pkl'
    pickle.dump(ibcf_model_knn, open(filename, 'wb'))
    filename = 'knn_models/item_user_rating.pkl'
    pickle.dump(item_user, open(filename, 'wb'))

    response = {'message': 'model saved'}
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
    distances, indices = model_knn.kneighbors(item_user[lectureid].values.reshape(1, -1), return_distance=True)
    # distances, indices = model_knn.kneighbors(mo.iloc[lectureid, :].values.reshape(1, -1), return_distance=True)

    # print(indices)

    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # print('ok2')
    # overview2 = list(map(
    #     lambda x: Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('lectureidx', 'lecturename',
    #                                                                              'thumburl', 'lecturer',
    #                                                                              'level')
    #     , range(0, len(distances.flatten()))))
    # # .distinct().order_by('lectureidx')
    # for i in overview2:
    #     overview_list.append(
    #         dict([('lectureIdx', i[0]['lectureidx']),
    #               ('lectureName', i[0]['lecturename']),
    #               ('thumbUrl', i[0]['thumburl']),
    #               ('lecturer', i[0]['lecturer']),
    #               ('level', decimal.Decimal(i[0]['level']))
    #               ]))
    for x in range(0, len(distances.flatten())):
        i = Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('siteinfo__logoimage', 'thumburl', 'lecturer',
                                                                 'level', 'price', 'rating', 'level__levelidx', 'level__levelname',
                                                                 'siteinfo').distinct()
        # sitename = Siteinfo.objects.select_related('sitename').get(siteidx=i[0]['siteinfo'])
        sitename = Siteinfo.objects.get(siteidx=i[0]['siteinfo']).sitename
        # print('sitename',Lecture.objects.select_related('siteinfo').filter(lectureidx=lectureidx))
        # sitename = Lecture.objects.select_related('siteinfo').get(lectureidx=lectureidx).sitename
        # # .values('sitename')
        # print(sitename)
        # decimal.Decimal(i[0]['price'])
        price = i[0]['price']
        if price == 0:
            price = 'free'
        elif price == -1:
            price = 'membership'

            # 강의 썸네일 없을 경우
        thumbnail = i[0]['thumburl']
        if not thumbnail:
            thumbnail = i[0]['siteinfo__logoimage']


        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', thumbnail),
                  ('lecturer', i[0]['lecturer']),
                  ('level', decimal.Decimal(i[0]['level'])),
                  ('price', price),
                  ('rating', i[0]['rating']),
                  ('siteName', sitename),
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

    distances, indices = ubcf_model_knn.kneighbors(user_item.iloc[userid, :].values.reshape(1, -1),
                                                   return_distance=True)

    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # print('ok2')
    # overview2 = list(map(
    #     lambda x: Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('lectureidx', 'lecturename',
    #                                                                              'thumburl', 'lecturer',
    #                                                                              'level')
    #     , range(0, len(distances.flatten()))))
    # # .distinct().order_by('lectureidx')
    # for i in overview2:
    #     overview_list.append(
    #         dict([('lectureIdx', i[0]['lectureidx']),
    #               ('lectureName', i[0]['lecturename']),
    #               ('thumbUrl', i[0]['thumburl']),
    #               ('lecturer', i[0]['lecturer']),
    #               ('level', decimal.Decimal(i[0]['level']))
    #               ]))
    for x in range(0, len(distances.flatten())):
        i = Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('siteinfo__logoimage','lectureidx', 'lecturename', 'thumburl',
                                                                           'lecturer',
                                                                           'level', 'price', 'rating','level__levelidx',
                                                                           'siteinfo').distinct()
        # sitename = Siteinfo.objects.select_related('sitename').get(siteidx=i[0]['siteinfo'])
        sitename = Siteinfo.objects.get(siteidx=i[0]['siteinfo']).sitename
        # print('sitename',Lecture.objects.select_related('siteinfo').filter(lectureidx=lectureidx))
        # sitename = Lecture.objects.select_related('siteinfo').get(lectureidx=lectureidx).sitename
        # # .values('sitename')
        # print(sitename)
        # decimal.Decimal(i[0]['price'])
        price = i[0]['price']
        if price == 0:
            price = 'free'
        elif price == -1:
            price = 'membership'

            # 강의 썸네일 없을 경우
        thumbnail = i[0]['thumburl']
        if not thumbnail:
            thumbnail = i[0]['siteinfo__logoimage']



        overview_list.append(
            dict([('lectureIdx', i[0]['lectureidx']),
                  ('lectureName', i[0]['lecturename']),
                  ('thumbUrl', thumbnail),
                  ('lecturer', i[0]['lecturer']),
                  ('level', decimal.Decimal(i[0]['level'])),
                  ('price', price),
                  ('rating', i[0]['rating']),
                  ('siteName', sitename),
                  ('levelIdx', i[0]['level__levelidx'])
                  ]))
    overview_dict['result'] = overview_list
    return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
    return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


@api_view(['GET'])
def create_matrixFactorization_IBCF(request):
    # ratings_df = pd.read_csv('C:/Users/user/Desktop/KME/codeing/backend/data/rating.csv', sep=';')
    # movies_df = pd.read_csv('C:/Users/user/Desktop/KME/codeing/backend/data/movies.csv', sep=';', encoding='latin-1')
    # A_df = ratings_df.pivot_table(index=['userId'], columns=['movieId'], values='rating', aggfunc=np.max)
    # A_df.fillna(0, inplace=True)
    # A = A_df.values
    A_df = pickle.load(open('knn_models/user_item_rating.pkl', 'rb')).astype(float)
    A = A_df.values
    user_rating_mean = np.mean(A, axis=1)

    A_normalized = A - user_rating_mean.reshape(-1, 1)
    # print(A_normalized)
    U, sigma, Vt = svds(A_normalized, k=50)

    sigma = np.diag(sigma)

    predicted_rating = np.dot(np.dot(U, sigma), Vt) + user_rating_mean.reshape(-1, 1)
    predicted_rating_df = pd.DataFrame(predicted_rating, columns=A_df.columns)
    filename = 'knn_models/predicted_rating_df.pkl'
    pickle.dump(predicted_rating_df, open(filename, 'wb'))

    preds_df = np.transpose(predicted_rating_df)
    item_similarity = cosine_similarity(preds_df)
    item_sim_df = pd.DataFrame(item_similarity, index=preds_df.index, columns=preds_df.index)
    filename = 'knn_models/item_sim_df.pkl'
    pickle.dump(item_sim_df, open(filename, 'wb'))

    all_user_names = list(map(lambda x: x.userinfo, Profile.objects.only("userinfo")))
    all_category_ids = list(map(lambda x: x.categoryidx, Category.objects.all()))
    all_subcategory_ids = list(map(lambda x: x.subcategoryidx, Subcategory.objects.all()))
    all_lectures = list(map(lambda x: x.lectureidx, Lecture.objects.all()))
    all_reviews = list(map(lambda x: x.reviewidx, Review.objects.all()))
    all_categorys = len(all_category_ids) + len(all_subcategory_ids)
    # print(all_categorys)
    num_users = len(list(all_user_names))
    num_lectures = len(list(all_lectures))
    num_reviews = len(list(all_reviews))
    # userInterest = np.zeros([num_users, all_categorys])
    userInterest = -np.ones([num_users, all_categorys])
    # lectureData = np.zeros([num_lectures, 1])
    # reviewData = np.zeros([num_reviews, 6])
    lectureData = pd.DataFrame(columns=['lectureidx', 'lecturename'], index=range(num_lectures))
    reviewData = pd.DataFrame(
        columns=['reviewidx', 'useridx', 'lectureidx', 'totalrating', 'pricerating', 'teachrating', 'recommend'],
        index=range(num_reviews))
    # Lecture.objects.filter(lectureidx=indices.flatten()[x]).values('lectureidx', 'lecturename',
    #                                                                'thumburl', 'lecturer',
    #                                                                'level')
    # print(Lecture.objects.all().values('lectureidx', 'lecturename','thumburl', 'lecturer','level'))
    # print(1)
    for i in Lecture.objects.all().values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level'):
        # all_lecturecategory_ids = Lecture.objects.filter(lecture=all_lectures[i])
        # for lecturecategory in all_lecturecategory_ids:
        # print(i[0]['lecturename'])
        # print(i['lecturename'], i['lectureidx'])
        lectureData.loc[i['lectureidx'], 'lectureidx'] = i['lectureidx']
        lectureData.loc[i['lectureidx'], 'lecturename'] = i['lecturename']
        # lectureData[i['lectureidx'], 'rating'] = i['lecturename']
        # lectureData[i, 11 + lecturecategory.subcategory.subcategoryidx] = 2
    # print(2)
    filename = 'knn_models/lecture_df.pkl'
    pickle.dump(lectureData, open(filename, 'wb'))

    for i in Review.objects.all().values('reviewidx', 'profile', 'lectureidx', 'totalrating', 'pricerating',
                                         'teachingpowerrating', 'recommend'):
        # print(i)
        reviewData.loc[i['reviewidx'], 'reviewidx'] = i['reviewidx']
        reviewData.loc[i['reviewidx'], 'useridx'] = i['profile']
        reviewData.loc[i['reviewidx'], 'lectureidx'] = i['lectureidx']
        reviewData.loc[i['reviewidx'], 'totalrating'] = i['totalrating']
        reviewData.loc[i['reviewidx'], 'pricerating'] = i['pricerating']
        reviewData.loc[i['reviewidx'], 'teachrating'] = i['teachingpowerrating']
        reviewData.loc[i['reviewidx'], 'recommend'] = i['recommend']
    # print(3)
    # print(reviewData)
    filename = 'knn_models/review_df.pkl'
    pickle.dump(reviewData, open(filename, 'wb'))

    response = {'message': 'success'}
    return JsonResponse(response, safe=False)
    # item_sim_df.columns=item_sim_df.columns.str.strip()
    # print(item_sim_df)
    # item_sim_df.columns = [col.strip() for col in list(item_sim_df.columns)]


@api_view(['GET'])
def sim_movies_to(request, pk=None):
    item_sim_df = pickle.load(open('knn_models/item_sim_df.pkl', 'rb'))
    # count = 1
    # movieIndex = movies_df.index[movies_df['movieId'] == pk] + 1
    # print('Similar movies to {} are :'.format(movies_df.loc[pk].title))
    # overview2 = list(map(
    #     lambda x: Lecture.objects.filter(lectureidx=x)
    #         .values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level').distinct()
    #     , krecommend))
    # item_id = Lecture.objects.filter(lectureidx=pk).values('lectureidx')
    #                                                     # , 'lecturename', 'thumburl', 'lecturer', 'level').distinct()
    # print(item_id)
    # print(item_sim_df.sort_values(by=movieId, ascending=False))
    # for item in item_sim_df.sort_values(by=pk, ascending=False).index[1:11]:
    #     # itemIndex = movies_df.index[movies_df['movieId'] == item]
    #     item = Lecture.objects.filter(lectureidx=item).values('lectureidx', 'lecturename', 'thumburl', 'lecturer', 'level').distinct()
    # print(item)
    # print('No. {} : {}'.format(count, movies_df.loc[itemIndex].title))
    # count += 1
    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # print('ok2')
    overview2 = list(map(
        lambda x: Lecture.objects.filter(lectureidx=item_sim_df.sort_values(by=pk, ascending=False).index[x]).values(
            'lectureidx', 'lecturename',
            'thumburl', 'lecturer',
            'level')
        , range(1, 11)
    ))
    # , range(0, 10)
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
    # response = {'message': 'success'}
    # return JsonResponse(response, safe=False)


@api_view(['GET'])
def recommend_movies_to(request, pk=None):
    predicted_rating_df = pickle.load(open('knn_models/predicted_rating_df.pkl', 'rb'))
    movies_df = pickle.load(open('knn_models/lecture_df.pkl', 'rb'))
    original_ratings_df = pickle.load(open('knn_models/review_df.pkl', 'rb'))
    num_recommedations = 10

    user_row_number = pk - 1
    sorted_user_predictions = predicted_rating_df.iloc[user_row_number].sort_values(ascending=False)
    print(1)
    user_data = original_ratings_df[original_ratings_df.useridx == (pk)]
    user_full = (user_data.merge(movies_df, how='left', left_on='lectureidx', right_on='lectureidx').
                 sort_values(['totalrating'], ascending=False))
    # , 'pricerating', 'teachrating', 'recommend'
    print(2)
    # print('user {0} has already rated {1} movies.'.format(pk, user_full.shape[0]))
    # print('Recommending hightest {0} precdicted ratings movies not already rated.'.format(num_recommedations))
    # print(1,movies_df[~movies_df['lectureidx'].isin(user_full['lectureidx'])])
    # print(pd.DataFrame(sorted_user_predictions).reset_index())
    recommendations = (movies_df[~movies_df['lectureidx'].isin(user_full['lectureidx'])].
                           merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                                 left_on='lectureidx', right_on='lectureidx').
                           rename(columns={user_row_number: 'Predictions'}).
                           sort_values('Predictions', ascending=False).
                           iloc[:num_recommedations, :-1])
    print(3)
    # print(recommendations)
    # return user_full, recommendations

    # already_rated, predictions = recommend_movies(predicted_rating_df, 2, movies_df, ratings_df, 10)

    # already_rated = already_rated.head(10)
    # predictions = predictions

    overview_list = []
    overview_dict = {}
    overview_dict['isSuccess'] = 'true'
    overview_dict['code'] = 200
    overview_dict['message'] = '추천컨텐츠 조회 성공'
    # print('ok2')
    # overview2 = list(map(
    #     lambda x: Lecture.objects.filter(lectureidx=predicted_rating_df.sort_values(by=pk, ascending=False).index[x]).values('lectureidx', 'lecturename',
    #                                                                              'thumburl', 'lecturer',
    #                                                                              'level')
    #     , range(1, 11)
    #     ))
    # # , range(0, 10)
    # # .distinct().order_by('lectureidx')
    # for i in overview2:
    #     overview_list.append(
    #         dict([('lectureIdx', i[0]['lectureidx']),
    #               ('lectureName', i[0]['lecturename']),
    #               ('thumbUrl', i[0]['thumburl']),
    #               ('lecturer', i[0]['lecturer']),
    #               ('level', decimal.Decimal(i[0]['level']))
    #               ]))
    overview_dict['result'] = overview_list
    return_value = json.dumps(overview_dict, indent=4, default=decimal_default, ensure_ascii=False)
    return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)
    # response = {'message': 'success'}
    # return JsonResponse(response, safe=False)
