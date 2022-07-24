import csv
import os
import logging

logging.basicConfig(filename='mining.log', level=logging.DEBUG)

files = ["raw/" + file for file in os.listdir("raw")]

header = ["category", "day", "month", "year", "content"]
rows = []

for file in files:
    category, month, day = file[4:-4].split("-")
    things = open(file, "r").read().split("\n")

    for thing in things:

        try:
            year, content = thing.split(" ", 1)

            if len(content) <= 3:
                continue

            rows.append([category.title(), int(day), month.title(), int(year), content])

        except:
            logging.error(f"Cannot parse '{thing}'")

rows = sorted(rows, key=lambda x: x[3])

print(len(rows))

with open('onthisday.csv', mode='w') as fp:
    csv_writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(header)

    for row in rows:
        csv_writer.writerow(row)
