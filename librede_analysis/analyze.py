import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

    strbuffer = "Activity \t& Number of executions \t& Average execution time \t& Std of execution time \t& Total time spent executing\\\\\\hline\n"

    for target in targets:
        if target[0] in stats:
            values = stats[target[0]]
            strbuffer = strbuffer + "{0}\t&{1:}\t&{2:.1f}\t&{3:.1f}\t&{4}\\\\\n".format(target[1], len(values), np.mean(values), np.std(values), np.sum(values))

    outfile = outfolder + file.split(".")[0]+"-time-analysis.tex"
    with open(outfile, "w+") as f:
        f.write(strbuffer)


def extract_latex_recommendation_statistics(file, folder, outfolder):
    approaches = extract_chosen_approaches(pd.read_csv(folder + "\\" + file))
    if len(approaches) > 0:
        strbuffer = "Approach \t& Number of selections\\\\\\hline\n"
        for name, value in approaches.items():
            if len(name) == 0:
                name = "None "
            strbuffer = strbuffer + "{0} \t& {1}\\\\\n".format(name[:-1], value)
        outfile = outfolder + file.split(".")[0]+"-reco-analysis.tex"
        with open(outfile, "w+") as f:
            f.write(strbuffer)


#log = pd.read_csv("logbook.csv")
#extract_table(log)

