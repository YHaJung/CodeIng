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


path2 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/ratingt.csv"
path3 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/procont.csv"
# print(list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=',')))
reader = list(csv.reader(open(path2, "r", encoding='UTF-8'), delimiter=','))
# print(reader)
# writer = csv.writer(open(path3, 'w', encoding='UTF-8'), delimiter=';')
writer = csv.writer(open(path3, 'w', newline='', encoding='UTF8'), delimiter=',',quoting=csv.QUOTE_NONE)
r = ['reviewProConsIdx','reviewIdx','prosIdx','consIdx']
writer.writerow(r)
for row in reader[1:]:
    # date(randint(1960, 2020), randint(1, 12)
    p = randint(1, 6)
    c = randint(1, 8)
    if float(row[3])<3:
        c = randint(1,7)
    elif float(row[3])>3:
        p = randint(1,5)
    r = [row[0],row[0], p, c]
    print(r)
    # print(row)
    writer.writerow(r)
    # writer.writerows(row for row in reader)
    # writer.writerows(row for row in reader)
print('end')






