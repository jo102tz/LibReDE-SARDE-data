import pandas as pd
import matplotlib.pyplot as plt
import math
import os
import numpy as np
from librede_analysis import analyze
from librede_analysis import experiment_figures

name_mapping = {"RR" : ["ResponseTimeRegression"],
                "SD" : ["ServiceDemandLaw"],
                "UR" : ["UtilizationRegression"],
                "MO" : ["MenasceOptimization"],
                "LO": ["LiuOptimization"],
                "RT":["ResponseTimeApprox"],
                "WF" :["WangKalmanFilter"],
                "KF": ["KumarKalmanFilter"]}

def get_approach_short(long_name):
    for key, value in name_mapping.items():
        for name in value:
            if name in long_name:
                return key
    # If no approach known, return SD as default
    return "SD"

def get_real_error(estimate, real):
    if any(np.isinf(estimate)) or any(np.isnan(estimate)):
        return math.inf

    sum_error = 0
    for i, est in enumerate(estimate):
        sum_error = sum_error + math.fabs(est - real[i])/real[i]
    return sum_error/len(estimate)


def add_real_error(df, real_vector):
    error = []
    for index, line in df.iterrows():
        if (line["Type"] == " ESTIMATION" or line["Type"] == " EVALUATION" or line["Type"] == " OPTIMIZED_EVALUATION") and ("Error" not in line["Estimated Demand"]):
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

def plot_double_error_fig(logs, skippedLogs, errorvec, filename):

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
    colors = [estimationColor, respApproxColor,
              utilizationRegressionColor, serviceDemandLawColor, wangKalmanFilterColor, kumarKalmanFilterColor,
              responsetimeRegressionColor]
    timelines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in timecolors]
    lines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in colors]

    # Initialize figure
    plt.rcParams.update({'font.size': 14})
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [1, 5]}, figsize=(18, 6))
    # plt.subplots_adjust(left=0.06, bottom=0.13, right=0.98, top=1.00)

    minwidth = 8
    # Lines for events
    for finishTime, time in zip(estimations['Finish time'], estimations["Start time"]):
        ax1.hlines(y=1, xmin=time, xmax=max(finishTime, time+minwidth), color=estimationColor, linewidth=8)
    for finishTime, time, approach in zip(recommendations['Finish time'], recommendations["Start time"], recommendations['Selected Approach']):
        # print(finishTime)
        ax1.hlines(y=2, xmin=time, xmax=max(finishTime, time+minwidth), color=recommendationColor, linewidth=8)
        ax1.text(x=finishTime+30, y=1.8, s=get_approach_short(approach), color=recommendationColor, fontsize=10)
    for finishTime, time in zip(trainings['Finish time'], trainings["Start time"]):
        ax1.hlines(y=3, xmin=time, xmax=max(finishTime, time+minwidth), color=trainingColor, linewidth=8)
    for finishTime, time in zip(optimizations['Finish time'], optimizations["Start time"]):
        ax1.hlines(y=4, xmin=time, xmax=max(finishTime, time+minwidth), color=optimizationColor, linewidth=8)

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

    #ax1.set_axis_off()
    #ax1.set_frame_on(True)
    ax1.set_xlim(xmin=0, xmax=10800)
    ax1.set_ylim(ymin=0.5, ymax=4.5)
    #ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off',
    #                labelleft='off')
    ax1.set_yticks(ticks=[1,2,3,4])
    ax1.set_yticklabels(["EST", "REC", "TRA", "OPT"])
    ax1.set_xticklabels([])
    #ax1.legend(timelines, ['Estimation', 'Recommendation', 'Optimization', 'Training'], ncol=4)
    #ax1.set_xlabel("Time [min]")
    #ax1.set_ylabel("Estimation Error [%]")

    # Plot estimation accuracy
    plotwidth=2
    ax2.plot(estimations['Finish time'], pd.to_numeric(estimations[errorvec]) * 100, linewidth=plotwidth, color=estimationColor)

    # Plot evaluation
    respApprox = logs[(logs['Type'] == ' EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
    ax2.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec]) * 100, linewidth=plotwidth, color=respApproxColor)
    utilizationRegression = logs[(logs['Type'] == ' EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
    ax2.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec]) * 100, linewidth=plotwidth,
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
    ax2.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec]) * 100, linewidth=plotwidth,
             color=responsetimeRegressionColor)

    if len(logs[(logs['Type'] == ' OPTIMIZED_EVALUATION')]) > 0:
        respApprox = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
        ax2.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec]) * 100, linewidth=plotwidth, linestyle='dotted',
                 color=respApproxColor)
        utilizationRegression = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
        ax2.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec]) * 100,
                 linestyle='dotted',
                 linewidth=plotwidth, color=utilizationRegressionColor)
        serviceDemandLaw = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
        ax2.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw[errorvec]) * 100, linewidth=plotwidth,
                 linestyle='dotted',
                 color=serviceDemandLawColor)
        wangKalmanFilter = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
        ax2.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
                 linestyle='dotted',
                 color=wangKalmanFilterColor)
        kumarKalmanFilter = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
        ax2.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter[errorvec]) * 100, linewidth=plotwidth,
                 linestyle='dotted',
                 color=kumarKalmanFilterColor)
        responsetimeRegression = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
        ax2.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec]) * 100,
                 linestyle='dotted',
                 linewidth=plotwidth, color=responsetimeRegressionColor)

    # Plot estimation accuracy
    ax2.plot(estimations['Finish time'], pd.to_numeric(estimations[errorvec]) * 100, linewidth=plotwidth,
             color=estimationColor)
    ax2.set_xlabel("Time [min]")
    ax2.set_ylabel("Estimation Error [%]")
    ax2.set_xlim(xmin=0, xmax=10800)
    ax2.set_yticks([0,20,40,60,80])
    ax2.set_ylim(ymin=0, ymax=100)

    # Legend
    ax2.legend(lines, ['SARDE','ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter',
                      'KumarKalmanFilter', 'ResponsetimeRegression'], ncol=4, loc="upper right")

    # plt.xlim(0, 180)
    # Finish up plot
    fig.tight_layout(pad=0.1)
    fig.savefig(filename)
    # plt.show()


def print_err(logs, skippedLogs, errorvec, filename):
     # Initialize figure
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(18,6))
    #plt.subplots_adjust(left=0.06, bottom=0.13, right=0.98, top=1.00)

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
    responsetimeRegressionColor= plt.gca()._get_lines.prop_cycler.__next__()['color']

    # Lines for events
    #for finishTime in estimations['Finish time']:
    #    plt.axvline(x=finishTime, color=estimationColor)
    for finishTime, approach in zip(recommendations['Finish time'], recommendations['Selected Approach']):
        #print(finishTime)
        plt.axvline(x=finishTime, color=recommendationColor)
        plt.text(x=finishTime,y=0,s=get_approach_short(approach), color=recommendationColor, fontsize=10)
    for finishTime in optimizations['Finish time']:
        plt.axvline(x=finishTime, color=optimizationColor)
    for finishTime in trainings['Finish time']:
        plt.axvline(x=finishTime, color=trainingColor)

    # dashed lines for skipped events
    for finishTime in (skippedLogs[skippedLogs['Type'] == ' ESTIMATION']['Finish time']):
        plt.axvline(x=finishTime, color=estimationColor, linestyle='dashed')
    for finishTime in (skippedLogs[skippedLogs['Type'] == ' RECOMMENDATION']['Finish time']):
        plt.axvline(x=finishTime, color=recommendationColor, linestyle='dashed')
    for finishTime in (skippedLogs[skippedLogs['Type'] == ' OPTIMIZATION']['Finish time']):
        plt.axvline(x=finishTime, color=optimizationColor, linestyle='dashed')
    for finishTime in (skippedLogs[skippedLogs['Type'] == ' TRAINING']['Finish time']):
        plt.axvline(x=finishTime, color=trainingColor, linestyle='dashed')

    # Plot estimation accuracy
    plt.plot(estimations['Finish time'], pd.to_numeric(estimations[errorvec])*100, linewidth=3, color=estimationColor)
    plt.xlabel("Time [min]")
    plt.ylabel("Estimation Error [%]")

    # Plot evaluation
    respApprox = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
    plt.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec])*100, linewidth=3, color=respApproxColor)
    utilizationRegression = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
    plt.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec])*100, linewidth=3, color=utilizationRegressionColor)
    serviceDemandLaw = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
    plt.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw[errorvec])*100, linewidth=3, color=serviceDemandLawColor)
    wangKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
    plt.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter[errorvec])*100, linewidth=3, color=wangKalmanFilterColor)
    kumarKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
    plt.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter[errorvec])*100, linewidth=3, color=kumarKalmanFilterColor)
    responsetimeRegression = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
    plt.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec])*100, linewidth=3, color=responsetimeRegressionColor)

    if len(logs[(logs['Type'] == ' OPTIMIZED_EVALUATION')]) > 0:
        respApprox = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                    logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
        plt.plot(respApprox['Finish time'], pd.to_numeric(respApprox[errorvec]) * 100, linewidth=3, linestyle='dashed',
                 color=respApproxColor)
        utilizationRegression = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                    logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
        plt.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression[errorvec]) * 100, linestyle='dashed',
                 linewidth=3, color=utilizationRegressionColor)
        serviceDemandLaw = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                    logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
        plt.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw[errorvec]) * 100, linewidth=3, linestyle='dashed',
                 color=serviceDemandLawColor)
        wangKalmanFilter = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                    logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
        plt.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter[errorvec]) * 100, linewidth=3, linestyle='dashed',
                 color=wangKalmanFilterColor)
        kumarKalmanFilter = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                    logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
        plt.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter[errorvec]) * 100, linewidth=3, linestyle='dashed',
                 color=kumarKalmanFilterColor)
        responsetimeRegression = logs[(logs['Type'] == ' OPTIMIZED_EVALUATION') & (
                    logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
        plt.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression[errorvec]) * 100, linestyle='dashed',
                 linewidth=3, color=responsetimeRegressionColor)

    # Plot estimation accuracy
    plt.plot(estimations['Finish time'], pd.to_numeric(estimations[errorvec]) * 100, linewidth=3,
              color=estimationColor)
    plt.xlabel("Time [min]")
    plt.ylabel("Estimation Error [%]")

    # Legend
    colors = [estimationColor, recommendationColor, optimizationColor, trainingColor, estimationColor, respApproxColor, utilizationRegressionColor, serviceDemandLawColor, wangKalmanFilterColor, kumarKalmanFilterColor, responsetimeRegressionColor]
    lines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in colors]
    plt.legend(lines, ['Estimation', 'Recommendation', 'Optimization', 'Training', 'Estimation error', 'ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter', 'KumarKalmanFilter', 'ResponsetimeRegression'], ncol=2)
    #plt.legend(['ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter', 'KumarKalmanFilter', 'ResponsetimeRegression'], ncol=1)


    #plt.xlim(0, 180)
    # Finish up plot
    plt.tight_layout(pad=0.1)
    plt.savefig(filename)
    #plt.show()

def analyze_logbook(file="logbook.csv", folder=None, output=None):
    # Read File
    logs = pd.read_csv(folder + "\\" +file, index_col=False, delimiter=",")
    add_real_error(logs, real_vector=[0.01, 0.03, 0.005])

    # Cleanup and adjust finish time to minutes
    logs = logs[~logs['Estimated Error'].str.contains("Error")]
    logs = logs[~logs['Estimated Error'].str.contains("Infinity")]
    logs["Estimated Error"] = pd.to_numeric(logs["Estimated Error"], errors="coerce")
    logs['Start time'] = (logs['Finish time'] - logs['Time'])/1000
    logs['Finish time'] = (logs['Finish time'])/1000 - logs['Start time'].min()
    logs['Start time'] = logs['Start time'] - logs['Start time'].min()

    # Dump skipped events
    skippedLogs = logs[logs['Time'] == 0]
    logs = logs[~(logs['Time'] == 0)]

    name = file.split(".")[0]
    # plot real error
    plot_double_error_fig(logs, skippedLogs, "Real error", output + "\\" + name+"-figure_real-error.pdf")
    # plot estimated error
    plot_double_error_fig(logs, skippedLogs, "Estimated Error", output + "\\"+name+"-figure_estimated-error.pdf")

def create_paper_figures():
    output = r"librede_analysis/paperfigures/"
    # create data-anylsis figures
    experiment_figures.print_absolute_requests_with_util(r"librede-parsing/arrivals.csv", r"librede-parsing/10.1.234.186.csv", output)
    # create all result figures
    dir = r"librede_analysis/logbooks/paper"
    for filename in os.listdir(dir):
        analyze_logbook(filename, dir, output)
        #analyze.extract_table(pd.read_csv(dir + "\\" + filename))
        analyze.extract_latex_timetable(filename, dir, output)
        if filename == "recommendation.csv":
            analyze.extract_latex_recommendation_statistics(filename, dir, output)
        print("Finished ", filename)


if __name__ == "__main__":
    create_paper_figures()
