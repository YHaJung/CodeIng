from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import MovieSerializer, ReviewSerializer
from .models import Review, Movie

from .form import ReviewForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
import datetime

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


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def get_suggestions(request):
    num_reviews = Review.objects.count()
    all_user_names = list(map(lambda x: x.id, User.objects.only("id")))
    all_movie_ids = set(map(lambda x: x.movie_id, Review.objects.only("movie")))
    num_users = len(list(all_user_names))
    movieRatings_m = sp.sparse.dok_matrix((num_users, max(all_movie_ids) + 1), dtype=np.float32)
    for i in range(num_users):
        user_reviews = Review.objects.filter(user_id=all_user_names[i])
        for user_review in user_reviews:
            movieRatings_m[i, user_review.movie_id] = user_review.rating
    movieRatings = movieRatings_m.transpose()
    coo = movieRatings.tocoo(copy=False)
    df = pd.DataFrame({'movies': coo.row, 'users': coo.col, 'rating': coo.data}
                      )[['movies', 'users', 'rating']].sort_values(['movies', 'users']).reset_index(drop=True)
    mo = df.pivot_table(index=['movies'], columns=['users'], values='rating')
    mo.replace(np.nan, 0, regex=True, inplace=True)
    model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
    model_knn.fit(mo.values)
    # .reshape(1, -1)
    distances, indices = model_knn.kneighbors(mo.iloc[100, :].values.reshape(1, -1), return_distance=True)
    # Movie.objects.get(id=indices.flatten()[x])
    # Movie.objects.filter(id=indices.flatten()[x])
    # get_object_or_404(Movie, id=indices.flatten()[x])
    context = list(map(lambda x: Movie.objects.filter(id=indices.flatten()[x]), range(0, len(distances.flatten()))))
    # print(request.user.username)
    return render(request, 'moviesreviews/get_suggestions.html', {'context': context})


# 이후 강의
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'rating' in request.data:
            # movie = Movie.objects.get(id=pk)
            movie = get_object_or_404(Movie, id=pk)
            rating = request.data['rating']
            # user = request.user
            user = User.objects.get(id=1)
            # print('user', user.id, user)

            try:
                try:
                    review = Review.objects.get(user_id=user.id, movie=movie.id)
                    # review = get_object_or_404(Review, user_id=user.id, movie=movie.id)
                    review.rating = rating
                    review.save()
                except:
                    review = None
            except:
                Review.objects.create(user_id=user.id, movie=movie.id, rating=rating)

            response = {'message': 'its working'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide ratings'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
