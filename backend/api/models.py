from django.db import models

from django.db.models import Avg
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)

    def average_rating(self):
        # sum = 0
        # ratings = Review.objects.filter(movie=self)
        # for rating in ratings:
        #     sum += rating.rating
        # if len(ratings) >0:
        #     return sum/len(ratings)
        # else:
        #     return 0
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title

    def no_of_ratings(self):
        ratings = Review.objects.filter(movie=self)
        return len(ratings)


class Review(models.Model):
    RATING_CHOICES = {
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    }
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    user_id = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, default='user')
    comment = models.CharField(max_length=200)
    rating = models.FloatField(choices=RATING_CHOICES, default=None, null=True, blank=True)

    class Meta:
        unique_together = (('user_id', 'movie'),)
        index_together = (('user_id', 'movie'),)

