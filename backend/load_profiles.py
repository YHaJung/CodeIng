import sys, os
import pandas as pd

from backend import settings
from lecture.models import Profile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

django.setup()

# from django.contrib.auth.models import User

def save_user_from_row(user_row):
    user = Profile()
    user.userinfo = user_row[0]
    user.name = user_row[1]
    user.userid = user_row[1]
    user.userpwd = user_row[1]
    user.gender = user_row[2]
    user.birthday = user_row[3]
    user.email = user_row[4]
    user.phonenumber = user_row[5]
    user.school = user_row[6]
    user.job = user_row[7]
    user.major = user_row[8]
    user.level = user_row[9]
    user.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file ", str(sys.argv[1]))
        print('hi')
        users_df = pd.read_csv(sys.argv[1], sep=';', )
        print(users_df)

        users_df.apply(save_user_from_row, axis=1)

        print("There are {} users".format(Profile.objects.count()))

    else:
        print("Please, provide User file path")
