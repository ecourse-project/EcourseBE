import csv
import json

# with open('data.json', 'r', encoding='utf-8') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         print(row)


file = open("data.txt", encoding="utf=8")
print(json.loads(file.read()))
