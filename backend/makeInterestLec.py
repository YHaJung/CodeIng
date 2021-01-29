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


path2 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/userf.csv"
path3 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/interestlec.csv"
# path4 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/interest.csv"

reader = list(csv.reader(open(path2, "r", encoding='UTF-8'), delimiter=','))

# writer = csv.writer(open(path3, 'w', encoding='UTF-8'), delimiter=';')
writer1 = csv.writer(open(path3, 'w', newline='', encoding='UTF8'), delimiter=',',quoting=csv.QUOTE_NONE)
# writer2 = csv.writer(open(path4, 'w', newline='', encoding='UTF8'), delimiter=',',quoting=csv.QUOTE_NONE)
r1 = ['userIdx','lectureIdx']
writer1.writerow(r1)

for row in reader[1:]:
    # date(randint(1960, 2020), randint(1, 12)
    c = list(set(randint(1, 12) for i in range(4)))
    s = list(set(randint(1, 71) for i in range(4)))
    # print(c)
    for i in c:
        # print(i)
        r = [row[0],i]
        # print(r)
        writer1.writerow(r)

    # writer.writerows(row for row in reader)
    # writer.writerows(row for row in reader)
print('end')






