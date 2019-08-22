import pandas as pd
import matplotlib.pyplot as plt

def print_throughput_figure(file):
    tps = pd.read_csv(file, delimiter=",")
    plt.plot(tps['Timestamps'], tps["wc3-relative"].rolling(window=60).mean(), color="b")
    plt.plot(tps['Timestamps'], tps["wc2-relative"].rolling(window=60).mean(), color="r")
    plt.plot(tps['Timestamps'], tps["wc1-relative"].rolling(window=60).mean(), color="g")
    #plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("Relative Share")
    plt.savefig(file+".pdf")

print_throughput_figure("arrivals.csv")
