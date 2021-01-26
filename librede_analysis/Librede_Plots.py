import math
import os

import numpy as np
import pandas as pd

from librede_analysis import analyze, experiment_split, experiment_figures

real_rds = [0.01, 0.03, 0.005]


def get_real_error(estimate, real):
    if any(np.isinf(estimate)) or any(np.isnan(estimate)):
        return math.inf

    sum_error = 0
    for i, est in enumerate(estimate):
        sum_error = sum_error + math.fabs(est - real[i]) / real[i]
    return sum_error / len(estimate)


def add_real_error(df, real_vector):
    error = []
    for index, line in df.iterrows():
        if (line["Type"] == " ESTIMATION" or line["Type"] == " EVALUATION" or line[
            "Type"] == " OPTIMIZED_EVALUATION") and ("Error" not in line["Estimated Demand"]):
            ests = line["Estimated Demand"][3:-2].split(";")
            parsed = []
            for val in ests:
                try:
                    val = float(val.replace(" ", ""))
                except ValueError:
                    print("Not a float")
                    val = -1
                parsed.append(val)
                if math.isnan(val):
                    parsed.append(math.inf)
            error.append(get_real_error(parsed, real_vector))
        else:
            error.append("-1")
    df["Real error"] = error


def analyze_logbook(file="logbook.csv", folder=None, output=None, print_estimation=True, print_optimizations=True):
    # Read File
    logs = pd.read_csv(folder + "/" + file, index_col=False, delimiter=",")
    add_real_error(logs, real_vector=real_rds)

    # Cleanup and adjust finish time to minutes
    logs = logs[~logs['Estimated Error'].str.contains("Error")]
    logs = logs[~logs['Estimated Error'].str.contains("Infinity")]
    logs["Estimated Error"] = pd.to_numeric(logs["Estimated Error"], errors="coerce")
    logs['Start time'] = (logs['Finish time'] - logs['Time']) / 1000
    logs['Finish time'] = (logs['Finish time']) / 1000 - logs['Start time'].min()
    logs['Start time'] = logs['Start time'] - logs['Start time'].min()

    # Dump skipped events
    skippedLogs = logs[logs['Time'] == 0]
    logs = logs[~(logs['Time'] == 0)]

    name = file.split(".")[0]

    # plot real error
    experiment_figures.plot_double_error_fig(logs, skippedLogs, "Real error", output + name + ".pdf",
                                             print_estimation, print_optimizations)


def print_base_estimators(file="logbook.csv", folder=None, output=None):
    # Read File
    logs = pd.read_csv(folder + "/" + file, index_col=False, delimiter=",")
    add_real_error(logs, real_vector=real_rds)

    # Cleanup and adjust finish time to minutes
    logs = logs[~logs['Estimated Error'].str.contains("Error")]
    logs = logs[~logs['Estimated Error'].str.contains("Infinity")]
    logs["Estimated Error"] = pd.to_numeric(logs["Estimated Error"], errors="coerce")
    logs['Start time'] = (logs['Finish time'] - logs['Time']) / 1000
    logs['Finish time'] = (logs['Finish time']) / 1000 - logs['Start time'].min()
    logs['Start time'] = logs['Start time'] - logs['Start time'].min()

    # Dump skipped events
    logs = logs[~(logs['Time'] == 0)]

    experiment_figures.plot_base_estimators(logs, output)


def create_paper_figures():
    output = r"librede_analysis/paperfigures/"
    # create data-anylsis figures
    experiment_figures.print_absolute_requests_with_util(r"librede-parsing/arrivals.csv",
                                                         r"librede-parsing/10.1.234.186.csv", output)
    # create all result figures
    dir = r"librede_analysis/logbooks/paper"
    for filename in os.listdir(dir):
        if not os.path.isdir(dir + "/" + filename):
            # this prints on console only
            #analyze.extract_table(pd.read_csv(dir + "/" + filename))
            # same analysis but to file
            analyze.extract_latex_timetable(filename, dir, output)
            if filename == "recommendation.csv":
                # print only base estimators
                print_base_estimators(filename, dir, output)
                # print estimation
                analyze_logbook(filename, dir, output, print_estimation=True, print_optimizations=False)
                # extract recommendation statistics
                data = pd.read_csv(dir + "/" + filename)
                add_real_error(data, real_vector=real_rds)
                analyze.extract_latex_recommendation_statistics(data, filename, output)
            if filename == "optimization.csv":
                analyze_logbook(filename, dir, output, print_estimation=False, print_optimizations=True)
            if filename == "combined.csv":
                analyze_logbook(filename, dir, output, print_estimation=True, print_optimizations=False)
                # extract recommendation statistics
                data = pd.read_csv(dir + "/" + filename)
                add_real_error(data, real_vector=real_rds)
                analyze.extract_latex_recommendation_statistics(data, filename, output)
                # split experiment analysis only for combination
                analyze_experiment_split(filename, dir, output)
            print("Finished ", filename)


def analyze_experiment_split(file, folder=None, output=None):
    # Read File
    logs = pd.read_csv(folder + "\\" + file, index_col=False, delimiter=",")
    add_real_error(logs, real_vector=real_rds)

    # Cleanup and adjust finish time to minutes
    logs = logs[~logs['Estimated Error'].str.contains("Error")]
    logs = logs[~logs['Estimated Error'].str.contains("Infinity")]
    logs["Estimated Error"] = pd.to_numeric(logs["Estimated Error"], errors="coerce")
    logs['Start time'] = (logs['Finish time'] - logs['Time']) / 1000
    logs['Finish time'] = (logs['Finish time']) / 1000 - logs['Start time'].min()
    logs['Start time'] = logs['Start time'] - logs['Start time'].min()

    # Dump skipped events
    logs = logs[~(logs['Time'] == 0)]

    # give to splitter
    experiment_split.analyze_experiment_split(logs, splits=10, outfile=output + "\\experiment_split.tex")


if __name__ == "__main__":
    print("Analyzing logbooks...")
    create_paper_figures()
    print("Done!")
