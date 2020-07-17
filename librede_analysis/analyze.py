import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import random
from collections import defaultdict

targets = [(" ESTIMATION", "Estimation"),
(" OPTIMIZATION", "Optimization"),
(" RECOMMENDATION", "Recommendation"),
(" TRAINING", "Training")]


def extract_stats(data):
    # Extracting data to a dictionary
    stats = dict()
    for index, row in data.iterrows():
        if row["Type"] not in stats:
            stats[row["Type"]] = []
        stats[row["Type"]].append(row["Time"])
    return stats


def extract_table(data):
    stats = extract_stats(data)

    for target in targets:
        if target[0] in stats:
            print_table_row(stats[target[0]], target[1])

    if " RECOMMENDATION" in stats:
        approaches = extract_chosen_approaches(data)
        print("\n\nChosen approaches:")
        for key, val in approaches.items():
            print(key + ": " + (str(val)))


def extract_chosen_approaches(data):
    approaches = dict()
    for index, row in data.iterrows():
        if row["Type"] == " RECOMMENDATION":
            approach = row["Selected Approach"].split(".")[-1]
            if approach not in approaches:
                approaches[approach] = 0
            approaches[approach] = approaches[approach] + 1
    return approaches


def print_table_row(stats, name):
    print("\n")
    print(name + ":")
    print("Number of executions: " + str(len(stats)))
    print("Average execution time: " + str(np.mean(stats)))
    print("STD of execution time: " + str(np.std(stats)))
    print("Total execution time: " + str(np.sum(stats)))


def extract_latex_timetable(file, folder, outfolder):
    stats = extract_stats(pd.read_csv(folder + "\\" +file))

    strbuffer = "Activity \t& Number of executions \t& Average execution time (ms) \t& Std of execution time (ms) \t& Total time spent executing (ms)\\\\\\hline\n"

    for target in targets:
        if target[0] in stats:
            values = stats[target[0]]
            strbuffer = strbuffer + "{0}\t&{1:}\t&{2:.1f}\t&{3:.1f}\t&{4}\\\\\n".format(target[1], len(values), np.mean(values), np.std(values), np.sum(values))

    outfile = outfolder + file.split(".")[0]+"-time-analysis.tex"
    with open(outfile, "w+") as f:
        f.write(strbuffer)


def extract_latex_recommendation_statistics(file, folder, outfolder):
    data = pd.read_csv(folder + "\\" + file)
    approaches, chosen = extract_reco_quality(data)
    if len(approaches) > 0:
        strbuffer = "Approach \t& Average Rank \t& Accuracy Loss (in \\%) \\\\\\hline\n"
        for name, values in approaches.items():
            arr = np.asarray(values)[:, :-1]
            means = np.mean(arr.astype(np.float), axis=0)
            strbuffer = strbuffer + "{0}\t& {1:.2f} \t& {2:.2f}\\\\\n".format(name, means[1], means[2]*100)
        approach_means = np.mean(chosen, axis=0)
        strbuffer = strbuffer + "\\hline {0} \t& {1:.2f} \t& {2:.2f}\\\\\n".format("Approach", approach_means[1], approach_means[2]*100)
        random_means = np.mean(create_random(approaches), axis=0)
        strbuffer = strbuffer + "{0} \t& {1:.2f} \t& {2:.2f}\\\\\n".format("Random", random_means[1], random_means[2]*100)
        outfile = outfolder + file.split(".")[0]+"-reco-analysis.tex"
        with open(outfile, "w+") as f:
            f.write(strbuffer)


def create_random(approaches):
    random.seed(42)
    chosen = []
    for i, value in enumerate(next(iter(approaches.values()))):
        timestamp = value[0]
        approach = random.choice(list(approaches.values()))
        rank = approach[i][1]
        accuracy = approach[i][2]
        chosen.append([timestamp, rank, accuracy])
    return chosen


def extract_reco_quality(data):
    recommendations = []
    dependents = []
    for index, row in data.iterrows():
        if row["Type"] == " EVALUATION":
            dependents.append(row)
        if row["Type"] == " RECOMMENDATION":
            approach = row["Selected Approach"]
            if row["Selected Approach"] != " None.":
                approach = approach.split(".")[-1].replace(")", "")
            time = row["Finish time"]
            dependents = []
            recommendations.append([time, approach, dependents])
    algo_performances = get_algo_performances(recommendations)
    approach = []
    for key, value in algo_performances.items():
        for row in value:
            if row[3] == key:
                rank = row[1]
                accuracy = row[2]
                timestamp = row[0]
                approach.append([timestamp, rank, accuracy])
    return algo_performances, approach
    # for reco in recommendations:
    #     best_of = get_best_of(reco[2])
    #     # add rank
    #     for i, el in enumerate(best_of):
    #         if el[0] == reco[1]:
    #             reco.append(i+1)
    # # combine into a comprehensible dict
    # result = {}
    # for reco in recommendations:
    #     if reco[1] not in result:
    #         result[reco[1]] = []
    #     if len(reco) > 3:
    #         result[reco[1]].append(reco[3])
    #     else:
    #         result[reco[1]].append(math.nan)
    # overall = []
    # for i in result:
    #     overall.extend(result[i])
    #     result[i] = [np.mean(result[i]), len(result[i])]
    # result["Overall "] = [np.nanmean(overall), (~np.isnan(overall)).sum()]
    # return result


def get_algo_performances(intervals):
    approaches = defaultdict(list)
    for i, val in enumerate(intervals):
        sorted = get_best_of(val[2])
        for i, el in enumerate(sorted):
            approaches[el[0]].append([val[0], int(i+1), el[1]-sorted[0][1], val[1]])
    return approaches



def get_best_of(estimations):
    approaches = {}
    for est in estimations:
        name = est["Selected Approach"].split(".")[-1]
        if name not in approaches:
            approaches[name] = []
        approaches[name].append(get_error(est))
    compresssed = []
    for i in approaches:
        compresssed.append([i, np.mean(approaches[i])])
    return sorted(compresssed, key=lambda tup: tup[1])


def get_error(est):
    return float(est["Estimated Error"])


#log = pd.read_csv("logbook.csv")
#extract_table(log)

