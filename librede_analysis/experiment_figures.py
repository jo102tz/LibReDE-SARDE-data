import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter

name_mapping = {
                "RT": ["ResponseTimeApprox"],
                "SD": ["ServiceDemandLaw"],
                "RR": ["ResponseTimeRegression"],
                "UR": ["UtilizationRegression"],
#                "MO": ["MenasceOptimization"],
#                "LO": ["LiuOptimization"],
                "WF": ["WangKalmanFilter"],
                "KF": ["KumarKalmanFilter"]}


def get_approach_short(long_name):
    for key, value in name_mapping.items():
        for name in value:
            if name in long_name:
                return key
    # If nothing recommended (None.), we return the default SD
    if long_name == " None.":
        return "SD"
    # If no approach known, return None
    print("Approach name not found: " + long_name)
    return None

def print_relative_requests(file, outputfolder=None):
    tps = pd.read_csv(file, delimiter=",")
    plt.plot(tps['Timestamps'], tps["wc3-relative"].rolling(window=60).mean(), color="b")
    plt.plot(tps['Timestamps'], tps["wc2-relative"].rolling(window=60).mean(), color="r")
    plt.plot(tps['Timestamps'], tps["wc1-relative"].rolling(window=60).mean(), color="g")
    # plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("Relative Share")
    filename = file.split("/")[-1].split(".")[0]
    plt.savefig(outputfolder + filename + "-relative.pdf")


def print_absolute_requests(file, outputfolder=None):
    tps = pd.read_csv(file, delimiter=",")
    minTS = min(tps['Timestamps'])
    plt.stackplot(tps['Timestamps'] - minTS, [tps["wc1-absolute"], (tps["wc2-absolute"]), (tps["wc3-absolute"])],
                  colors=["g", "r", "b"])
    # plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]), color="r")
    # plt.stackplot(tps['Timestamps']-minTS, (tps["wc1-absolute"]+tps["wc2-absolute"]+tps["wc3-absolute"]), color="b")
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
    plt.rcParams.update({'font.size': 14})
    fig, ax1 = plt.subplots(figsize=(18, 5))
    ax1.stackplot(tps['Timestamps'] - minTS, [tps["wc1-absolute"], (tps["wc2-absolute"]), (tps["wc3-absolute"])],
                  colors=["seagreen", "lightcoral", "darkslateblue"])

    # plt.plot(tps['Timestamps'], tps["Timestamps"], color="black")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("# Requests per second")
    ax1.set_xlim(0, 10500)

    util = pd.read_csv(utilfile, delimiter=",", names=["TS", "Util"])
    ax2 = ax1.twinx()
    ax2.set_ylabel('Utilization [%]', color="black")  # we already handled the x-label with ax1
    ax2.plot(util["TS"] - minTS, savgol_filter(util["Util"], 51, 3), color="black")
    ax2.tick_params(axis='y', labelcolor="black")

    fig.legend(["WC1", "WC2", "WC3", "Utilization"], loc="upper right", bbox_to_anchor=(0.95, 0.95))
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


def plot_double_error_fig(logs, skippedLogs, errorvec, filename, plot_estimation, plot_optimized):
    # Color and dataprep
    estimations = logs[logs['Type'] == ' ESTIMATION']
    estimations = estimations[estimations['Type'] == ' ESTIMATION']
    estimationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    recommendationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    recommendations = logs[logs['Type'] == ' RECOMMENDATION']
    optimizationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    optimizations = logs[logs['Type'] == ' OPTIMIZATION']
    trainingColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    trainings = logs[logs['Type'] == ' TRAINING']
    respApproxColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    utilizationRegressionColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    serviceDemandLawColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    wangKalmanFilterColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    kumarKalmanFilterColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    responsetimeRegressionColor = plt.gca()._get_lines.prop_cycler.__next__()['color']

    timecolors = [estimationColor, recommendationColor, optimizationColor, trainingColor]
    colors = [respApproxColor,
              utilizationRegressionColor, serviceDemandLawColor, wangKalmanFilterColor, kumarKalmanFilterColor,
              responsetimeRegressionColor, estimationColor]
    timelines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in timecolors]
    lines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in colors]

    # Initialize figure
    plt.rcParams.update({'font.size': 14})
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [1, 5]}, figsize=(18, 6))
    # plt.subplots_adjust(left=0.06, bottom=0.13, right=0.98, top=1.00)

    minwidth = 8
    # Lines for events
    for finishTime, time in zip(estimations['Finish time'], estimations["Start time"]):
        ax1.hlines(y=1, xmin=time, xmax=max(finishTime, time + minwidth), color=estimationColor, linewidth=8)
    for finishTime, time, approach in zip(recommendations['Finish time'], recommendations["Start time"],
                                          recommendations['Selected Approach']):
        # print(finishTime)
        ax1.hlines(y=2, xmin=time, xmax=max(finishTime, time + minwidth), color=recommendationColor, linewidth=8)
        ax1.text(x=finishTime + 30, y=1.8, s=get_approach_short(approach), color=recommendationColor, fontsize=10)
    for finishTime, time in zip(trainings['Finish time'], trainings["Start time"]):
        ax1.hlines(y=3, xmin=time, xmax=max(finishTime, time + minwidth), color=trainingColor, linewidth=8)
    for finishTime, time in zip(optimizations['Finish time'], optimizations["Start time"]):
        ax1.hlines(y=4, xmin=time, xmax=max(finishTime, time + minwidth), color=optimizationColor, linewidth=8)

    # Lines for events
    # for finishTime in estimations['Finish time']:
    #    plt.axvline(x=finishTime, color=estimationColor)
    # for finishTime, approach in zip(recommendations['Finish time'], recommendations['Selected Approach']):
    #     # print(finishTime)
    #     ax1.axvline(x=finishTime, color=recommendationColor)
    #     ax1.text(x=finishTime, y=0, s=get_approach_short(approach), color=recommendationColor, fontsize=10)
    # for finishTime in optimizations['Finish time']:
    #     ax1.axvline(x=finishTime, color=optimizationColor)
    # for finishTime in trainings['Finish time']:
    #     ax1.axvline(x=finishTime, color=trainingColor)
    #
    # # dashed lines for skipped events
    # for finishTime in (skippedLogs[skippedLogs['Type'] == ' ESTIMATION']['Finish time']):
    #     ax1.axvline(x=finishTime, color=estimationColor, linestyle='dashed')
    # for finishTime in (skippedLogs[skippedLogs['Type'] == ' RECOMMENDATION']['Finish time']):
    #     ax1.axvline(x=finishTime, color=recommendationColor, linestyle='dashed')
    # for finishTime in (skippedLogs[skippedLogs['Type'] == ' OPTIMIZATION']['Finish time']):
    #     ax1.axvline(x=finishTime, color=optimizationColor, linestyle='dashed')
    # for finishTime in (skippedLogs[skippedLogs['Type'] == ' TRAINING']['Finish time']):
    #     ax1.axvline(x=finishTime, color=trainingColor, linestyle='dashed')

    # ax1.set_axis_off()
    # ax1.set_frame_on(True)
    ax1.set_xlim(xmin=0, xmax=10800)
    ax1.set_ylim(ymin=0.5, ymax=4.5)
    # ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off',
    #                labelleft='off')
    ax1.set_yticks(ticks=[1, 2, 3, 4])
    ax1.set_yticklabels(["Est", "Sel", "Tra", "Opt"])
    ax1.set_xticklabels([])
    # ax1.legend(timelines, ['Estimation', 'Recommendation', 'Optimization', 'Training'], ncol=4)
    # ax1.set_xlabel("Time [min]")
    # ax1.set_ylabel("Estimation Error [%]")

    # Plot estimation accuracy
    plotwidth = 2

    # Plot evaluation
    respApprox = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
    ax2.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec]) * 100, linewidth=plotwidth,
             color=respApproxColor)
    utilizationRegression = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
    ax2.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec]) * 100,
             linewidth=plotwidth,
             color=utilizationRegressionColor)
    serviceDemandLaw = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
    ax2.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw[errorvec]) * 100, linewidth=plotwidth,
             color=serviceDemandLawColor)
    wangKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
    ax2.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
             color=wangKalmanFilterColor)
    kumarKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
    ax2.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
             color=kumarKalmanFilterColor)
    responsetimeRegression = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
    ax2.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec]) * 100,
             linewidth=plotwidth,
             color=responsetimeRegressionColor)

    # ax2.plot(estimations['Finish time'], pd.to_numeric(estimations[errorvec]) * 100, linewidth=plotwidth, color=estimationColor)

    if len(logs[(logs['Type'] == ' OPTIMIZED_EVALUATION')]) > 0 and plot_optimized is True:
        respApprox = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
        ax2.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec]) * 100, linewidth=plotwidth,
                 linestyle='dashed', dashes=(5, 5),
                 color=respApproxColor)
        utilizationRegression = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
        ax2.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec]) * 100,
                 linestyle='dashed', dashes=(5, 5),
                 linewidth=plotwidth, color=utilizationRegressionColor)
        serviceDemandLaw = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
        ax2.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw[errorvec]) * 100, linewidth=plotwidth,
                 linestyle='dashed', dashes=(5, 5),
                 color=serviceDemandLawColor)
        wangKalmanFilter = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
        ax2.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
                 linestyle='dashed', dashes=(5, 5),
                 color=wangKalmanFilterColor)
        kumarKalmanFilter = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
        ax2.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter[errorvec]) * 100,
                 linewidth=plotwidth,
                 linestyle='dashed', dashes=(5, 5),
                 color=kumarKalmanFilterColor)
        responsetimeRegression = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
        ax2.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec]) * 100,
                 linestyle='dashed', dashes=(5, 5),
                 linewidth=plotwidth, color=responsetimeRegressionColor)

    # Plot estimation accuracy
    if plot_estimation:
        ax2.plot(estimations['Finish time'], pd.to_numeric(estimations[errorvec]) * 100, linewidth=plotwidth,
                 color=estimationColor)
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Estimation Error [%]")
    ax2.set_xlim(xmin=0, xmax=10800)
    ax2.set_yticks([0, 20, 40, 60, 80])
    ax2.set_ylim(ymin=0, ymax=100)

    # Legend
    if plot_estimation is True:
        names = ['ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter',
                 'KumarKalmanFilter', 'ResponsetimeRegression', 'SARDE']
        ncols = 4

    else:
        names = ['ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter',
                 'KumarKalmanFilter', 'ResponsetimeRegression']
        ncols = 3
    ax2.legend(lines, names, ncol=ncols, loc="upper right")

    # plt.xlim(0, 180)
    # Finish up plot
    fig.tight_layout(pad=0.1)
    fig.savefig(filename)
    # plt.show()


def plot_base_estimators(logs, output=None):
    filename = output + "\\base-figure_real-error.pdf"
    errorvec = "Real error"

    # Color and dataprep
    estimations = logs[logs['Type'] == ' ESTIMATION']
    estimations = estimations[estimations['Type'] == ' ESTIMATION']
    estimationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    recommendationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    recommendations = logs[logs['Type'] == ' RECOMMENDATION']
    optimizationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    optimizations = logs[logs['Type'] == ' OPTIMIZATION']
    trainingColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    trainings = logs[logs['Type'] == ' TRAINING']
    respApproxColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    utilizationRegressionColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    serviceDemandLawColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    wangKalmanFilterColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    kumarKalmanFilterColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
    responsetimeRegressionColor = plt.gca()._get_lines.prop_cycler.__next__()['color']

    colors = [respApproxColor,
              utilizationRegressionColor, serviceDemandLawColor, wangKalmanFilterColor, kumarKalmanFilterColor,
              responsetimeRegressionColor, estimationColor]
    lines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in colors]

    # Initialize figure
    plt.rcParams.update({'font.size': 14})
    fig, ax2 = plt.subplots(figsize=(18, 5))

    # Plot estimation accuracy
    plotwidth = 2

    # Plot evaluation
    respApprox = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
    ax2.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec]) * 100, linewidth=plotwidth,
             color=respApproxColor)
    utilizationRegression = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
    ax2.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec]) * 100,
             linewidth=plotwidth,
             color=utilizationRegressionColor)
    serviceDemandLaw = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
    ax2.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw[errorvec]) * 100, linewidth=plotwidth,
             color=serviceDemandLawColor)
    wangKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
    ax2.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
             color=wangKalmanFilterColor)
    kumarKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
    ax2.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
             color=kumarKalmanFilterColor)
    responsetimeRegression = logs[(logs['Type'] == ' EVALUATION') & (
            logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
    ax2.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec]) * 100,
             linewidth=plotwidth,
             color=responsetimeRegressionColor)

    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Estimation Error [%]")
    ax2.set_xlim(xmin=0, xmax=10800)
    ax2.set_yticks([0, 20, 40, 60, 80])
    ax2.set_ylim(ymin=0, ymax=100)

    names = ['ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter',
             'KumarKalmanFilter', 'ResponsetimeRegression']
    ncols = 3
    ax2.legend(lines, names, ncol=ncols, loc="upper right")

    # plt.xlim(0, 180)
    # Finish up plot
    fig.tight_layout(pad=0.1)
    fig.savefig(filename)
    # plt.show()
