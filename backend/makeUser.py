import csv
import string
from datetime import date, time, datetime, timedelta
from random import *

def random_date():
    start_date = date(1960, 1, 1)
    end_date = date(2020, 12, 30)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date

path = 'C:/Users/user/Downloads/13_7651_bundle_archive/NationalNames.csv'
path2 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/users6.csv"
path3 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/userf.csv"
# print(list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=',')))
reader = list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=','))
# print(reader)
# writer = csv.writer(open(path3, 'w', encoding='UTF-8'), delimiter=';')
writer = csv.writer(open(path3, 'w', newline='', encoding='UTF8'), delimiter=',',quoting=csv.QUOTE_NONE)
r = ['userIdx','nickName']
writer.writerows(r)
for row in reader[6:621]:
    r = [row[0], row[1]]
    # print(r)
    # print(row)
    writer.writerow(r)
    # writer.writerows(row for row in reader)
    # writer.writerows(row for row in reader)






