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

from api.serializers import MovieSerializer, ReviewSerializer, UserSerializer
from .models import Review, Movie

from surprise import SVD
import pandas as pd
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
from surprise.model_selection import cross_validate

from .form import ReviewForm
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
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'moviesreviews/review_list.html', context)


def review_detail(request, pk):
    review = get_object_or_404(Review, id=pk)
    return render(request, 'moviesreviews/review_detail.html', {'review': review})


def movie_list(request):
    movie_list = Movie.objects.order_by('-title')[:20]
    context = {'movie_list': movie_list}
    return render(request, 'moviesreviews/movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    form = ReviewForm()
    return render(request, 'moviesreviews/movie_detail.html', {'movie': movie})


def add_review(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.movie = movie
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(reverse('movie_detail', args=(movie.id,)))
    return render(request, 'moviesreviews/movie_detail.html', {'movie': movie, 'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def get_top_n(predictions, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def do_Predict(userGroupId, ingredientId, ratings):
    ratings_dict = {'userID': userGroupId,
                    'itemID': ingredientId,
                    'rating': ratings}

    df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(1, 4))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    return get_top_n(predictions)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


# 이후 코드
@api_view(['GET'])
def get_suggestions(request):
    num_reviews = Review.objects.count()
    all_user_names = list(map(lambda x: x.id, User.objects.only("id")))
    all_movie_ids = set(map(lambda x: x.movie_id, Review.objects.only("movie")))
    print(all_movie_ids)
    num_users = len(list(all_user_names))
    movieRatings_m = sp.sparse.dok_matrix((num_users, max(all_movie_ids) + 1), dtype=np.float32)
    for i in range(num_users):
        user_reviews = Review.objects.filter(user_id=all_user_names[i])
        for user_review in user_reviews:
            print(user_review)
            movieRatings_m[i, user_review.movie_id] = user_review.rating
    movieRatings = movieRatings_m.transpose()
    coo = movieRatings.tocoo(copy=False)
    df = pd.DataFrame({'movies': coo.row, 'users': coo.col, 'rating': coo.data}
                      )[['movies', 'users', 'rating']].sort_values(['movies', 'users']
                                                                   ).reset_index(drop=True)
    mo = df.pivot_table(index=['movies'], columns=['users'], values='rating')
    mo.fillna(0, inplace=True)
    model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
    model_knn.fit(mo.values)
    distances, indices = model_knn.kneighbors(mo.iloc[100, :].values.reshape(1, -1), return_distance=True)
    # context = list(map(lambda x: Movie.objects.filter(id=indices.flatten()[x]).values_list('id','title'), range(0, len(distances.flatten()))))
    # for x in range(0, len(distances.flatten())):
    #     # context = Movie.objects.filter(id=indices.flatten()[x]).values()
    #     # print(json.dumps(context))
    #     data = serializers.serialize('json', Movie.objects.filter(id=indices.flatten()[x]), fields=('id','title'))
    #     print(data)
    context = list(map(lambda x: serializers.serialize('json', Movie.objects.filter(id=indices.flatten()[x]), fields=('id','title')),
                       range(0, len(distances.flatten()))))
    response = {'results': 'show'}
    # print(type(context))
    # print(context)
    # context_json = serializers.serialize('json', context)
    # return JsonResponse(response, status=status.HTTP_200_OK)
    # return HttpResponse(json.dumps(context), content_type='application/json')
    return JsonResponse(context, safe=False)

# 이후 강의
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()[:8]
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'rating' in request.data:
            # movie = Movie.objects.get(id=pk)
            movie = get_object_or_404(Movie, id=pk)
            rating = request.data['rating']
            user = request.user
            # print(user)
            # user = User.objects.get(id=1)
            try:
                # try:
                review = Review.objects.get(user_id=user.id, movie=movie.id)
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
                review = Review(user_id=user, movie=movie, rating=rating, pub_date=timezone.now())
                # Review.objects.create(user_id=user.id, movie=movie.id, rating=rating, pub_date=timezone.now())
                # review.rating = rating
                review.save()
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide ratings'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def get_recommended_item(self, request, pk=None):
        userGroupId = list(map(lambda x: x.id, User.objects.only("id")))
        ingredientId = set(map(lambda x: x.movie_id, Review.objects.only("movie")))
        ratings = list(map(lambda x: x, Review.objects.only("rating")))
        itemInfo = []
        recommendations = do_Predict(userGroupId, ingredientId, ratings)
        for users in recommendations.items():
            if users[0] == pk:
                for items in users[1]:
                    movie = get_object_or_404(Movie, id=items)
                    # itemInfo.append(con.getNames(items[0]))
                return (movie)


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
