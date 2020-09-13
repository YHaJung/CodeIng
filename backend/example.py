import csv

path = "C:/Users/user/Downloads/ml-latest-small/movies.csv"
path2 = "C:/Users/user/Downloads/ml-latest-small/movies1.csv"
path3 = "C:/Users/user/Downloads/ml-latest-small/rating2.csv"
# print(list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=',')))
# reader = list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=','))
# writer = csv.writer(open(path3, 'w', encoding='UTF-8'), delimiter=';')
# for row in reader:
#     print(row)
# writer.writerows(row for row in reader)

# for row in reader:
#     print(row[3])
#     row[3] = row[3].replace("\n", "")
#     # print(row)
#     # # row[1] = row[1].replace('"', '')
#     # # row[2] = row[2].replace('"', '')
#     writer.writerows(row)

# for line in open(path2, 'w'):
#     if line == "\n":
#         line.replace("\n", '')

reader = csv.reader(open(path, "r", newline=None, encoding='UTF8'), delimiter=',')
# print(list(reader))
writer = csv.writer(open(path2, 'w', newline='', encoding='UTF8'), delimiter=';')
writer.writerows(list(reader))



