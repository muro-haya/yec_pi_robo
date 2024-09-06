import csv
import time
import random
import keyboard
import os
import ui

# csv file name
csv_file = '/home/robo2/csv_data/data_periodic.csv'
key_log = False
interval = 0
interval_cnt = 0

def get_data():
    recieved_datas, input_data = ui.set_ui_log()
    return{
        'timestamp'      :time.strftime('%Y-%m-%d %h-:%M:%S'),

        'Input val10'    :input_data[0],
        'Input val11'    :input_data[1],
        'Input val12'    :input_data[2],
        'Input val13'    :input_data[3],
        'Input val14'    :input_data[4],
        'Input val15'    :input_data[5],
        'Input val16'    :input_data[6],
        'Input val17'    :input_data[7],
        'Input val18'    :input_data[8],
        'Input val19'    :input_data[9],

        'receive val10'    :recieved_datas[0],
        'receive val11'    :recieved_datas[1],
        'receive val12'    :recieved_datas[2],
        'receive val13'    :recieved_datas[3],
        'receive val14'    :recieved_datas[4],
        'receive val15'    :recieved_datas[5],
        'receive val16'    :recieved_datas[6],
        'receive val17'    :recieved_datas[7],
        'receive val18'    :recieved_datas[8],
        'receive val19'    :recieved_datas[9],
    }

def write_to_csv(data, file_name):
    file_exists = os.path.isfile(file_name)

    # write csv file
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        fieldnames = [  'timestamp'       ,
                        'Input val10'     ,
                        'Input val11'     ,
                        'Input val12'     ,
                        'Input val13'     ,
                        'Input val14'     ,
                        'Input val15'     ,
                        'Input val16'     ,
                        'Input val17'     ,
                        'Input val18'     ,
                        'Input val19'     ,

                        'receive val10'   ,
                        'receive val11'   ,
                        'receive val12'   ,
                        'receive val13'   ,
                        'receive val14'   ,
                        'receive val15'   ,
                        'receive val16'   ,
                        'receive val17'   ,
                        'receive val18'   ,
                        'receive val19'   ]
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            # write header
            writer.writeheader()

        # write data
        writer.writerow(data)

def cyc_log():
    global key_log
    global interval_cnt

    if keyboard.is_pressed('s'):
        key_log = True
        print("Start")

    if keyboard.is_pressed('z'):
        key_log = False
        print("End")

    if key_log:
        if interval < interval_cnt:
            # get data
            data = get_data()

            # write data to csv
            write_to_csv(data, csv_file)

            interval_cnt = 0
        interval_cnt += 1

