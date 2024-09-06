import csv
import time
import random
import keyboard
import os

# csv file name
csv_file = '/home/robo2/csv_data/data_periodic.csv'

def get_data():
    return{
        'timestamp':time.strftime('%Y-%m-%d %h-:%M:%S'),
        'value'    :random.random()
    }

def write_to_csv(data, file_name):
    file_exists = os.path.isfile(file_name)

    # write csv file
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['timestamp', 'value']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            # write header
            writer.writeheader()

        # write data
        writer.writerow(data)

def main():
    interval = 2
    key_log = False

    while True:
        if keyboard.is_pressed('s'):
            key_log = True
            print("Start")

        if keyboard.is_pressed('e'):
            key_log = False
            print("End")
            break

        if key_log:
            # get data
            data = get_data()

            # write data to csv
            write_to_csv(data, csv_file)

            # wait time
            time.sleep(interval)

if __name__ == '__main__':
    main()