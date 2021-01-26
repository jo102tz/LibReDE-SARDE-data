import math
from collections import defaultdict

import numpy as np

from librede_analysis import experiment_figures


#
# approaches = [[" tools.descartes.librede.approach.ResponseTimeApproximationApproach", "RT"],
# [" tools.descartes.librede.approach.ServiceDemandLawApproach", "SD"],
# [" tools.descartes.librede.approach.UtilizationRegressionApproach", "UR"],
# [" tools.descartes.librede.approach.ResponseTimeRegressionApproach", "RR"],
# [" tools.descartes.librede.approach.KumarKalmanFilterApproach", "KF"],
# [" tools.descartes.librede.approach.WangKalmanFilterApproach", "WF"]]


def analyze_experiment_split(logs, loads, splits=10, outfile=None):
    # +1 to make sure the very last finish is also in the last interval (and does not crete another new one)
    span = logs["Finish time"].max() + 1
    interval = span / splits

    # iterate through all entries to sort them into their respective bins
    bins = defaultdict(lambda: {"est": [], "eval": defaultdict(lambda: []), "loads" : [0, 0, 0]})
    # first iterate through approach performances
    for index, row in logs.iterrows():
        time = row["Finish time"]
        # round down, to get the interval number of each entry and assign them in the respective list
        bin_index = math.floor(time / interval)
        if row["Type"] == " ESTIMATION":
            bins[bin_index]["est"].append(row["Real error"])
        if row["Type"] == " EVALUATION":
            bins[bin_index]["eval"][experiment_figures.get_approach_short(row["Selected Approach"])].append(
                row["Real error"])

    # secondly add load information
    for index, row in loads.iterrows():
        time = row["Finish time"]
        # round down, to get the interval number of each entry and assign them in the respective list
        bin_index = math.floor(time / interval)
        # arrivals can be larger intervals, therefore we need this check
        if (bin_index < splits and bin_index >= 0):
            bins[bin_index]["loads"][0] += row["wc1-absolute"]/interval
            bins[bin_index]["loads"][1] += row["wc2-absolute"]/interval
            bins[bin_index]["loads"][2] += row["wc3-absolute"]/interval


    approaches = list(experiment_figures.name_mapping.keys())
    # now iterate through intevals and create a statistical for each interval
    #print_split_to_console(bins, approaches)
    print_split_to_latex(bins, approaches, outfile)


def print_split_to_latex(bins, approaches, outfile):
    strbuffer = "Interval&\tProperties&\tSARDE&\t{0}&\t{1}&\t{2}&\t{3}&\t{4}&\t{5}&\tBest\\\\\\midrule\n".format(approaches[0],
                                                                                                    approaches[1],
                                                                                                    approaches[2],
                                                                                                    approaches[3],
                                                                                                    approaches[4],
                                                                                                    approaches[5])
    for i in bins:
        sarde_err = np.mean(bins[i]["est"])
        loads = "({0:.2f}, {1:.2f}, {2:.2f})".format(bins[i]["loads"][0], bins[i]["loads"][1], bins[i]["loads"][2])
        strbuffer += "{0}\t&{1}\t&{2:.2f}\t&".format(str(i + 1), loads, sarde_err)
        best = "SARDE"
        best_val = sarde_err
        for approach in approaches:
            err = np.mean(bins[i]["eval"][approach])
            strbuffer += "{0:.2f}\t&".format(err)
            if err < best_val:
                best_val = err
                best = approach
        strbuffer += "{0}\\\\\n".format(best)

    with open(outfile, "w+") as f:
        f.write(strbuffer)


def print_split_to_console(bins, approaches):
    print("Interval,\tSARDE,\t{0},\t{1},\t{2},\t{3},\t{4},\t{5},\tBest,\t,Best_val".format(approaches[0], approaches[1],
                                                                                           approaches[2], approaches[3],
                                                                                           approaches[4],
                                                                                           approaches[5]))
    for i in bins:
        sarde_err = np.mean(bins[i]["est"])
        print("{0},\t{1:.2f}".format(i + 1, sarde_err), end=',\t')
        best = "SARDE"
        best_val = sarde_err
        for approach in approaches:
            err = np.mean(bins[i]["eval"][approach])
            print("{0:.2f}".format(err), end=',\t')
            if err < best_val:
                best_val = err
                best = approach
        print("{0},\t{1:.2f}".format(best, best_val))
