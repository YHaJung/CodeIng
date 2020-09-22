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


path2 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/users6.csv"
path3 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/profilesf.csv"
# print(list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=',')))
reader = list(csv.reader(open(path2, "r", encoding='UTF-8'), delimiter=';'))
# print(reader)
# writer = csv.writer(open(path3, 'w', encoding='UTF-8'), delimiter=';')
writer = csv.writer(open(path3, 'w', newline='', encoding='UTF8'), delimiter=',',quoting=csv.QUOTE_NONE)
r = ['userIdx','userId','userPwd','gender', 'name','birthday','email', 'phoneNumber','school','job','major', 'isBlocked','createdAt','updatedAt','isDeleted','level']
writer.writerows(r)
for row in reader[1:]:
    email = ''.join(choice(string.ascii_lowercase+string.digits) for _ in range(6))
    school = ''.join(choice(string.ascii_lowercase) for _ in range(6)) +" Univ"
    # date(randint(1960, 2020), randint(1, 12)
    r = [row[0], row[1], row[1], choice('FM'), row[1] , str(random_date()), email+"@gmail.com","010"+str(randint(10000000, 99999999)), school,choice('SDN'), choice('YN'), '','','','',randint(0, 5)]
    print(r)
    # print(row)
    writer.writerow(r)
    # writer.writerows(row for row in reader)
    # writer.writerows(row for row in reader)






