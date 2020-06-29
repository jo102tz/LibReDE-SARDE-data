import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

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

def print_absolute_requests_with_util(tpsfile, utilfile, outputfolder=None):
    tps = pd.read_csv(tpsfile, delimiter=",")
    minTS = min(tps['Timestamps'])
    fig, ax1 = plt.subplots()
    ax1.stackplot(tps['Timestamps'] - minTS, [tps["wc1-absolute"], (tps["wc2-absolute"]), (tps["wc3-absolute"])],
                  colors=["g", "r", "b"])

    # plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("# Requests per second")
    ax1.set_xlim(0, 10500)

    util = pd.read_csv(utilfile, delimiter=",", names=["TS", "Util"])
    ax2 = ax1.twinx()
    ax2.set_ylabel('Utilization [%]', color="black")  # we already handled the x-label with ax1
    ax2.plot(util["TS"] - minTS, savgol_filter(util["Util"], 51, 3), color="black")
    ax2.tick_params(axis='y', labelcolor="black")

    fig.legend(["WC1", "WC2", "WC3", "Utilization"], loc="upper right")
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    filename = tpsfile.split("/")[-1].split(".")[0]
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

