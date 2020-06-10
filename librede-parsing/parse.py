import csv
import os
import pandas as pd
import argparse
from datetime import datetime
import math

TS_DIVISION_FACTOR = 1000000000
RT_DIVISION_FACTOR = 1000000
ARRIVALS_FILE = "arrivals.csv"


# Request storing all required info per request
class Request:
    def __init__(self, in_time, out_time, wc):
        self.in_time = int(in_time)
        self.out_time = int(out_time)
        self.wc = wc


# Accepts a pandas data frame and parses it into a list of requests dictionary, splitted for WCs.
def parse_df_to_request_dict(df, offset_timestamp):
    ret = {}
    for index, row in df.iterrows():
        in_time = row["Start"]
        out_time = row["Stop"]
        wc = row["Url"]
        wc = wc.split("/")
        wc = wc[len(wc)-1]
        request = Request(offset_timestamp*TS_DIVISION_FACTOR + in_time, offset_timestamp*TS_DIVISION_FACTOR + out_time, wc)
        if wc not in ret:
            ret[wc] = []
        ret[wc].append(request)
    # sort requests for each wc
    for requests in ret.values():
        requests.sort(key=get_request_key)
    return ret


# Accepts a list of requests and return a requests dictionary, splitted for timestamps.
def parse_to_timestamp_dict(requests):
    ret = {}
    for req in requests:
        in_time = req.in_time
        if in_time not in ret:
            ret[in_time] = []
        ret[in_time].append(req)
    return ret


# Returns the sorting key for request objects, i.e., the in_time.
def get_request_key(req):
    return req.in_time


# Exports a given request-list to a csv file
def export_requests(file, requests):
    with open(file, mode='w', newline="") as output_file:
        writer = csv.writer(output_file, delimiter=',')
        for req in requests:
            writer.writerow([(req.in_time/TS_DIVISION_FACTOR), (req.out_time - req.in_time)/RT_DIVISION_FACTOR])


def convert_requests(stub, filename, start_timestamp):
    file = os.path.join(stub, filename)
    print("Analysing "+file)
    csv_frame = pd.read_csv(file)
    first_ts = csv_frame["Start"][0]
    offset_timestamp = start_timestamp - (first_ts/TS_DIVISION_FACTOR)
    requests = parse_df_to_request_dict(csv_frame, offset_timestamp)
    for wc in requests.values():
        outputname = os.path.join(stub, wc[0].wc)
        outputname = outputname + ".csv"
        export_requests(outputname, wc)
    export_throughputs(os.path.join(stub, ARRIVALS_FILE), requests)
    figures.print_throughput_figure(os.path.join(stub, ARRIVALS_FILE))


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


def export_throughputs(filename, requests):
    print("Exporting arrival rates to "+filename)
    wc_ts_dict = {}
    for wc, reqs in requests.items():
        wc_ts_dict[wc] = parse_to_timestamp_dict(reqs)
    counts, wcs = count_dict(wc_ts_dict)
    with open(filename, mode='w', newline="") as output_file:
        writer = csv.writer(output_file, delimiter=',')
        # write header
        header = ["Timestamps"]
        for i in range(0, len(wcs)):
            header.append(wcs[i]+"-absolute")
        for i in range(0, len(wcs)):
            header.append(wcs[i]+"-relative")
        writer.writerow(header)
        # go through the keyset in order
        for ts in sorted(counts.keys()):
            wcs_counts = counts[ts]
            line = [str(ts)]
            # create for each wc the absolute count
            sum = 0
            for i in range(0, len(wcs)):
                if wcs[i] in wcs_counts:
                    line.append(str(wcs_counts[wcs[i]]))
                    sum = sum + wcs_counts[wcs[i]]
                else:
                    # if no entry is found, no requests were seen for this timestamp
                    line.append("0")
            # create for each wc the relative count
            for i in range(0, len(wcs)):
                if wcs[i] in wcs_counts:
                    line.append(str(wcs_counts[wcs[i]]/sum))
                else:
                    # if no entry is found, no requests were seen for this timestamp
                    line.append("0")
            writer.writerow(line)


def count_dict(wc_ts_dict):
    ret_dict = {}
    for wc, ts_dict in wc_ts_dict.items():
        for ts in ts_dict.keys():
            ts = int(ts/TS_DIVISION_FACTOR)
            if ts not in ret_dict:
                ret_dict[ts] = {}
            if wc not in ret_dict[ts]:
                ret_dict[ts][wc] = 0
            ret_dict[ts][wc] = ret_dict[ts][wc]+1
    return ret_dict, list(wc_ts_dict.keys())




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
