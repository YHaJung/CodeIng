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
from rest_framework.utils import json

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
from lecture.models import Lecture, Review
from lecture.serializers import LectureSerializer, ReviewSerializer


@api_view(['GET'])
def get_suggestions(request):
    num_reviews = Review.objects.count()
    all_user_names = list(map(lambda x: x.id, User.objects.only("id")))
    # print('lecture',LectureReview.objects.only("lecture"))
    all_lecture_ids = set(map(lambda x: x.lecture, Review.objects.only("lecture")))
    # print(all_lecture_ids)
    num_users = len(list(all_user_names))
    print('num_users', num_users)
    print(max(all_lecture_ids))
    lectureRatings_m = sp.sparse.dok_matrix((num_users, max(all_lecture_ids) + 1), dtype=np.float32)

    for i in range(num_users):
        user_reviews = Review.objects.filter(user=all_user_names[i])
        for user_review in user_reviews:
            print(user_review)
            lectureRatings_m[i, user_review.lecture_id] = user_review.rating
    lectureRatings = lectureRatings_m.transpose()
    coo = lectureRatings.tocoo(copy=False)
    df = pd.DataFrame({'lectures': coo.row, 'users': coo.col, 'rating': coo.data}
                      )[['lectures', 'users', 'rating']].sort_values(['lectures', 'users']
                                                                   ).reset_index(drop=True)
    mo = df.pivot_table(index=['lectures'], columns=['users'], values='rating')
    mo.fillna(0, inplace=True)
    model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
    model_knn.fit(mo.values)
    distances, indices = model_knn.kneighbors(mo.iloc[100, :].values.reshape(1, -1), return_distance=True)
    # context = list(map(lambda x: Lecture.objects.filter(id=indices.flatten()[x]).values_list('id','title'), range(0, len(distances.flatten()))))
    # for x in range(0, len(distances.flatten())):
    #     # context = Movie.objects.filter(id=indices.flatten()[x]).values()
    #     # print(json.dumps(context))
    #     data = serializers.serialize('json', Movie.objects.filter(id=indices.flatten()[x]), fields=('id','title'))
    #     print(data)
    context = list(map(lambda x: serializers.serialize('json', Lecture.objects.filter(id=indices.flatten()[x]), fields=('id','lectureName')),
                       range(0, len(distances.flatten()))))
    response = {'results': 'show'}
    # print(type(context))
    # print(context)
    # context_json = serializers.serialize('json', context)
    # return JsonResponse(response, status=status.HTTP_200_OK)
    # return HttpResponse(json.dumps(context), content_type='application/json')
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

