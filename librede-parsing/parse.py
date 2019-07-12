import csv
import os
import pandas as pd
import argparse
from datetime import datetime
import math
from pytz import timezone


# Request storing all required info per request
class Request:
    def __init__(self, in_time, out_time, wc):
        self.in_time = int(in_time)
        self.out_time = int(out_time)
        self.wc = wc


# Accepts a pandas data frame and parses it into a list of requests dictionary, splitted for WCs.
def parse_df_to_request_dict(df):
    ret = {}
    for index, row in df.iterrows():
        in_time = row["Start"]
        out_time = row["Stop"]
        wc = row["Url"]
        wc = wc.split("/")
        wc = wc[len(wc)-1]
        request = Request(in_time, out_time, wc)
        if wc not in ret:
            ret[wc] = []
        ret[wc].append(request)
    for requests in ret.values():
        requests.sort(key=get_request_key)
    return ret


# Returns the sorting key for request objects, i.e., the in_time.
def get_request_key(req):
    return req.in_time


# Exports a given request-list to a csv file
def export_requests(file, requests, offset_timestamp):
    with open(file, mode='w', newline="") as output_file:
        writer = csv.writer(output_file, delimiter=',')
        for req in requests:
            writer.writerow([(req.in_time/1000000000) + offset_timestamp, (req.out_time - req.in_time)/1000000])


def convert_requests(stub, filename, start_timestamp):
    file = os.path.join(stub, filename)
    print("Analysing "+file)
    csv_frame = pd.read_csv(file)
    first_ts = csv_frame["Start"][0]
    offset_timestamp = start_timestamp - (first_ts/1000000000)
    requests = parse_df_to_request_dict(csv_frame)
    for wc in requests.values():
        outputname = os.path.join(stub, wc[0].wc)
        outputname = outputname + ".csv"
        export_requests(outputname, wc, offset_timestamp)


def convert_utilizations(stub, filename):
    file = os.path.join(stub, filename)
    csv_frame = pd.read_csv(file)
    utils = {}
    keys = {}
    # detect all columns that have utilizations stored
    for col in csv_frame:
        if(col.startswith("Watts(Utilization of ")):
            key = (col.split("Watts(Utilization of ")[1])[:-1]
            utils[key] = []
            keys[col] = key

    for index, row in csv_frame.iterrows():
        for colname, key in keys.items():
            utils[key].append(row[colname]*100)

    timestamp = parse_datetime(list(csv_frame)[-1])

    for key, value in utils.items():
        export_utilizations(os.path.join(stub, key)+".csv", value, timestamp)
    return timestamp


# Exports a given request-list to a csv file
def export_utilizations(file, utils, timestamp):
    with open(file, mode='w', newline="") as output_file:
        writer = csv.writer(output_file, delimiter=',')
        i = 0
        for ut in utils:
            if not math.isnan(ut):
                writer.writerow([timestamp+i, ut])
            i = i + 1


def parse_datetime(time):
    dtime = datetime.strptime(time, '%d.%m.%Y;%H:%M:%S%f')
    #time = timezone('Europe/Berlin').localize(time)
    print(dtime)
    return dtime.timestamp()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract the request data from a timestamps log.')
    parser.add_argument('timestamps', metavar="timestamps", help='File containing the timestamps measurement file.')
    parser.add_argument('utilizations', metavar="utilizations", help='File containing the utilization measurements.')

    args = parser.parse_args()
    print("Chosen timestamps: " + args.timestamps)
    print("Chosen utilizations: " + args.utilizations)

    path, filename = os.path.split(args.utilizations)
    print("Output is written into: " + path)
    print("Start reading in.")
    start_timestamp = convert_utilizations(path, filename)
    path, filename = os.path.split(args.timestamps)
    convert_requests(path, filename, start_timestamp)

    print("Finished.")
