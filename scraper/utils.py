import csv
import os


def print_scraped_data(data):
    for i in data:
        print("------")
        for k, v in i.items():
            print("{}: {}".format(k, v))


def save_to_csv(data, file):
    file_exists = os.path.isfile(file)
    file_is_empty = not file_exists or os.path.getsize(file) == 0

    with open(file, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if file_is_empty:
            writer.writeheader()
        writer.writerows(data)
    print("done")
