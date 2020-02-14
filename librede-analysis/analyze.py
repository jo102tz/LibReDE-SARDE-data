import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def extract_table(data):
    # Extracting data to a dictionary
    stats = dict()
    for index, row in data.iterrows():
        if row["Type"] not in stats:
            stats[row["Type"]] = []
        stats[row["Type"]].append(row["Time"])

    if " ESTIMATION" in stats:
        print_table_row(stats[" ESTIMATION"], "Estimation")
    if " OPTIMIZATION" in stats:
        print_table_row(stats[" OPTIMIZATION"], "Optimization")
    if " RECOMMENDATION" in stats:
        print_table_row(stats[" RECOMMENDATION"], "Recommendation")
        print_chosen_approaches_summary(data)
    if " TRAINING" in stats:
        print_table_row(stats[" TRAINING"], "Training")

def print_chosen_approaches_summary(data):
    approaches = dict()
    for index, row in data.iterrows():
        if row["Type"] == " RECOMMENDATION":
            approach = row["Selected Approach"].split(".")[-1]
            if approach not in approaches:
                approaches[approach] = 0
            approaches[approach] = approaches[approach] + 1

    print("Chosen approaches:")
    for key, val in approaches.items():
        print(key+": "+(str(val)))



def print_table_row(stats, name):
    print("\n")
    print(name + ":")
    print("Number of executions: " + str(len(stats)))
    print("Average execution time: " + str(np.mean(stats)))
    print("STD of execution time: " + str(np.std(stats)))
    print("Total execution time: " + str(np.sum(stats)))


log = pd.read_csv("logbook.csv")
extract_table(log)

