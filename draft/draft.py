import csv
import json

# with open('data.json', 'r', encoding='utf-8') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         print(row)


file = open("data.txt", encoding="utf=8")
a = json.loads(file.read())

# print(a[0]["name"])
print(len(str(a)))
