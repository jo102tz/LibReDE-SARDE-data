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

def index_of_dispersion(datapoints):
    if np.mean(datapoints) == 0:
        return math.nan
    return math.pow(np.std(datapoints),2) / np.mean(datapoints)


def analyze_experiment_split(logs, loads, splits=10, outfile=None):
    # +1 to make sure the very last finish is also in the last interval (and does not crete another new one)
    span = logs["Finish time"].max() + 1
    interval = span / splits

    # iterate through all entries to sort them into their respective bins
    bins = defaultdict(lambda: {"est": [], "eval": defaultdict(lambda: []), "loads": [[], [], []]})
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
            bins[bin_index]["loads"][0].append(row["wc1-absolute"])
            bins[bin_index]["loads"][1].append(row["wc2-absolute"])
            bins[bin_index]["loads"][2].append(row["wc3-absolute"])

    approaches = list(experiment_figures.name_mapping.keys())
    # now iterate through intevals and create a statistical for each interval
    # print_split_to_console(bins, approaches)
    print_split_to_latex(bins, approaches, outfile, print_approaches=False)


def print_split_to_latex(bins, approaches, outfile, print_approaches=False):
    strbuffer = "\\#&\tMean-WC1&\tMean-WC2&\tMean-WC3&\tStd-WC1&\tStd-WC2&\tStd-WC3&\tIoD-WC1&\tIoD-WC2&\tIoD-WC3&\tSARDE"
    if print_approaches:
        strbuffer += "&\t{0}&\t{1}&\t{2}&\t{3}&\t{4}&\t{5}&\tBest".format(approaches[0],
                                                                                      approaches[1],
                                                                                      approaches[2],
                                                                                      approaches[3],
                                                                                      approaches[4],
                                                                                      approaches[5])
    strbuffer += "\\\\\\midrule\n"
    for i in bins:
        strbuffer += str(i + 1) + "&\t"

        strbuffer += "{0:.2f}&\t {1:.2f}&\t {2:.2f}&\t".format(np.mean(bins[i]["loads"][0]), np.mean(bins[i]["loads"][1]),
                                                     np.mean(bins[i]["loads"][2]))
        strbuffer += "{0:.2f}&\t {1:.2f}&\t {2:.2f}&\t".format(np.std(bins[i]["loads"][0]), np.std(bins[i]["loads"][1]),
                                                     np.std(bins[i]["loads"][2]))
        strbuffer += "{0:.2f}&\t {1:.2f}&\t {2:.2f}&\t".format(index_of_dispersion(bins[i]["loads"][0]),
                                                     index_of_dispersion(bins[i]["loads"][1]),
                                                     index_of_dispersion(bins[i]["loads"][2]))
        sarde_err = np.mean(bins[i]["est"])
        strbuffer += "{0:.2f}".format(sarde_err)
        if print_approaches:
            best = "SARDE"
            best_val = sarde_err
            for approach in approaches:
                err = np.mean(bins[i]["eval"][approach])
                strbuffer += "\t&{0:.2f}".format(err)
                if err < best_val:
                    best_val = err
                    best = approach
            strbuffer += "\t&{0}".format(best)
        strbuffer += "\\\\\n"

    with open(outfile, "w+") as f:
        f.write(strbuffer)
