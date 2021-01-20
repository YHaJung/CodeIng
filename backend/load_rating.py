import sys, os
import pandas as pd
import datetime
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

django.setup()

from api.models import Review
from api.models import Movie
from django.contrib.auth.models import User


def save_review_from_row(review_row):
    review = Review()
    review.user_id = User.objects.get(id=review_row[0])
    review.user_name = User.objects.get(id=review_row[0])
    review.movie = Movie.objects.get(id=review_row[1])
    review.rating = review_row[2]
    review.pub_date = datetime.datetime.now(tz=timezone.utc)
    review.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file ", str(sys.argv[1]))
        ratingdf = pd.read_csv(sys.argv[1], sep=';')
        print(ratingdf)

        ratingdf.apply(
            save_review_from_row,
            axis=1
        )

        print("There are {} reviews ".format(Review.objects.count()))

    else:
        print("Please, provide rating file path")
