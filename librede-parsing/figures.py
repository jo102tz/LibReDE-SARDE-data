import pandas as pd
import matplotlib.pyplot as plt

def print_relative_requests(file):
    tps = pd.read_csv(file, delimiter=",")
    plt.plot(tps['Timestamps'], tps["wc3-relative"].rolling(window=60).mean(), color="b")
    plt.plot(tps['Timestamps'], tps["wc2-relative"].rolling(window=60).mean(), color="r")
    plt.plot(tps['Timestamps'], tps["wc1-relative"].rolling(window=60).mean(), color="g")
    #plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("Relative Share")
    plt.savefig(file+"-relative.pdf")

def print_absolute_requests(file):
    tps = pd.read_csv(file, delimiter=",")
    minTS = min(tps['Timestamps'])
    plt.stackplot(tps['Timestamps']-minTS, [tps["wc1-absolute"],(tps["wc2-absolute"]),(tps["wc3-absolute"])], colors=["g","r","b"])
    #plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]), color="r")
    #plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]+tps["wc3-absolute"]), color="b")
    plt.legend(["WC1", "WC2", "WC3"])
    # plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("# Requests per second")
    plt.savefig(file + "-absolute.pdf")

print_absolute_requests("arrivals.csv")