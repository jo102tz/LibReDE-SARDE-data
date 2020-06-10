import pandas as pd
import matplotlib.pyplot as plt

def print_relative_requests(file, outputfolder=None):
    tps = pd.read_csv(file, delimiter=",")
    plt.plot(tps['Timestamps'], tps["wc3-relative"].rolling(window=60).mean(), color="b")
    plt.plot(tps['Timestamps'], tps["wc2-relative"].rolling(window=60).mean(), color="r")
    plt.plot(tps['Timestamps'], tps["wc1-relative"].rolling(window=60).mean(), color="g")
    #plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("Relative Share")
    filename = file.split("/")[-1].split(".")[0]
    plt.savefig(outputfolder + filename+"-relative.pdf")

def print_absolute_requests(file, outputfolder=None):
    tps = pd.read_csv(file, delimiter=",")
    minTS = min(tps['Timestamps'])
    plt.stackplot(tps['Timestamps']-minTS, [tps["wc1-absolute"],(tps["wc2-absolute"]),(tps["wc3-absolute"])], colors=["g","r","b"])
    #plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]), color="r")
    #plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]+tps["wc3-absolute"]), color="b")
    plt.legend(["WC1", "WC2", "WC3"])
    # plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("# Requests per second")
    filename = file.split("/")[-1].split(".")[0]
    plt.savefig(outputfolder + filename + "-absolute.pdf")
    plt.close()

def print_utilization(file, outputfolder=None):
    util = pd.read_csv(file, delimiter=",", names=["TS", "Util"])
    minTS = min(util["TS"])
    plt.plot(util["TS"] - minTS, util["Util"])
    # plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]), color="r")
    # plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]+tps["wc3-absolute"]), color="b")
    plt.legend(["Utilization"])
    # plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("Utilization in %")
    plt.savefig(outputfolder + "utilization.pdf")
    plt.close()

