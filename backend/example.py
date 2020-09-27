import csv

path = "C:/Users/user/Desktop/KME/CodeIng/backend/data/profiles2.csv"
path2 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/users.csv"
path3 = "C:/Users/user/Desktop/KME/CodeIng/backend/data/profiles.csv"
# print(list(csv.reader(open(path, "r", encoding='UTF-8'), delimiter=',')))
# reader = list(csv.reader(open(path3, "r", encoding='UTF-8'), delimiter=','))
# writer = csv.writer(open(path, 'w', encoding='UTF-8'), delimiter=';')
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

reader = csv.reader(open(path3, "r", newline=None, encoding='UTF8'), delimiter=';')
read_list = list(reader)
# print(list(reader))
writer = csv.writer(open(path, 'w', newline='', encoding='UTF8'), delimiter=';',quoting=csv.QUOTE_NONE)
# writer.writerows(list(reader))
for i in read_list[::2]:
    writer.writerow(i)



