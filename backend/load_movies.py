import os
import sys

import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

django.setup()

from api.models import Movie


def save_movie_from_row(movie_row):
    movie = Movie()
    movie.id = movie_row[0]
    movie.title = movie_row[1]
    movie.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file ", str(sys.argv[1]))
        moviesdf = pd.read_csv(sys.argv[1], sep=';', encoding='latin-1')
        print(moviesdf)

        moviesdf.apply(save_movie_from_row, axis=1)

        print("There are {} movies".format(Movie.objects.count()))

    else:
        print("Please, provide Movies file path")
