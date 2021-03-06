import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

def get_real_error(estimate, real):
    if any(np.isinf(estimate)) or any(np.isnan(estimate)):
        return math.inf

    sum_error = 0
    for i, est in enumerate(estimate):
        sum_error = math.fabs(est - real[i])/real[i]
    return sum_error/len(estimate)


def add_real_error(df, real_vector):
    error = []
    for index, line in df.iterrows():
        if (line["Type"] == " ESTIMATION" or line["Type"] == " EVALUATION") and ("Error" not in line["Estimated Demand"]):
            ests = line["Estimated Demand"][3:-2].split(";")
            parsed = []
            for val in ests:
                val = float(val.replace(" ", ""))
                parsed.append(val)
                if math.isnan(val):
                    parsed.append(math.inf)
            error.append(get_real_error(parsed, real_vector))
        else:
            error.append("-1")
    df["Real error"] = error

# Read File
logs = pd.read_csv("logbook_motivating_example.csv", index_col=False, delimiter=",")
add_real_error(logs, real_vector=[0.01, 0.03, 0.005])

# Adjust finish time to minutes
logs = logs[~logs['Estimated Error'].str.contains("Error")]
logs = logs[~logs['Estimated Error'].str.contains("Infinity")]
logs['Start time'] = logs['Finish time'] - logs['Time']
logs['Finish time'] = (logs['Finish time'] - logs['Start time'].min())/1000/60

# Dump skipped events
skippedLogs = logs[logs['Time'] == 0]
logs = logs[~(logs['Time'] == 0)]

# Initialize figure
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(18,6))
#plt.subplots_adjust(left=0.06, bottom=0.13, right=0.98, top=1.00)

# Color and dataprep
estimations = logs[logs['Type'] == ' ESTIMATION']
estimations = estimations[estimations['Type'] == ' ESTIMATION']
# estimationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
# recommendationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
# recommendations = logs[logs['Type'] == ' RECOMMENDATION']
# optimizationColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
# optimizations = logs[logs['Type'] == ' OPTIMIZATION']
# trainingColor = plt.gca()._get_lines.prop_cycler.__next__()['color']
# trainings = logs[logs['Type'] == ' TRAINING']

# Lines for events
# for finishTime in estimations['Finish time']:
#     plt.axvline(x=finishTime, color=estimationColor)
# for finishTime in recommendations['Finish time']:
#     plt.axvline(x=finishTime, color=recommendationColor)
# for finishTime in optimizations['Finish time']:
#     plt.axvline(x=finishTime, color=optimizationColor)
# for finishTime in trainings['Finish time']:
#     plt.axvline(x=finishTime, color=trainingColor)
#
# # dashed lines for skipped events
# for finishTime in (skippedLogs[skippedLogs['Type'] == ' ESTIMATION']['Finish time']):
#     plt.axvline(x=finishTime, color=estimationColor, linestyle='dashed')
# for finishTime in (skippedLogs[skippedLogs['Type'] == ' RECOMMENDATION']['Finish time']):
#     plt.axvline(x=finishTime, color=recommendationColor, linestyle='dashed')
# for finishTime in (skippedLogs[skippedLogs['Type'] == ' OPTIMIZATION']['Finish time']):
#     plt.axvline(x=finishTime, color=optimizationColor, linestyle='dashed')
# for finishTime in (skippedLogs[skippedLogs['Type'] == ' TRAINING']['Finish time']):
#     plt.axvline(x=finishTime, color=trainingColor, linestyle='dashed')

# Plot estimation accuracy
# plt.plot(estimations['Finish time'], pd.to_numeric(estimations["Real error"])*100, linewidth=3)
plt.xlabel("Time [min]")
plt.ylabel("Estimation Error [%]")

# Plot evaluation
respApprox = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeApproximationApproach')]
plt.plot(respApprox['Finish time'], pd.to_numeric(respApprox["Real error"])*100, linewidth=3)
utilizationRegression = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.UtilizationRegressionApproach')]
plt.plot(utilizationRegression['Finish time'], pd.to_numeric(utilizationRegression["Real error"])*100, linewidth=3)
serviceDemandLaw = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.ServiceDemandLawApproach')]
plt.plot(serviceDemandLaw['Finish time'], pd.to_numeric(serviceDemandLaw["Real error"])*100, linewidth=3)
wangKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.WangKalmanFilterApproach')]
plt.plot(wangKalmanFilter['Finish time'], pd.to_numeric(wangKalmanFilter["Real error"])*100, linewidth=3)
kumarKalmanFilter = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.KumarKalmanFilterApproach')]
plt.plot(kumarKalmanFilter['Finish time'], pd.to_numeric(kumarKalmanFilter["Real error"])*100, linewidth=3)
responsetimeRegression = logs[(logs['Type'] == ' EVALUATION') & (logs['Selected Approach'] == ' tools.descartes.librede.approach.ResponseTimeRegressionApproach')]
plt.plot(responsetimeRegression['Finish time'], pd.to_numeric(responsetimeRegression["Real error"])*100, linewidth=3)
# Legend
#colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
#lines = [plt.Line2D([0], [0], color=c, linewidth=3) for c in colors]
#plt.legend(lines, ['Estimation', 'Recommendation', 'Optimization', 'Training', 'Estimation error', 'ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter', 'KumarKalmanFilter', 'ResponsetimeRegression'], ncol=1, loc='center left', bbox_to_anchor=(1, 0.5))
plt.legend(['ResponsetimeApproximation', 'UtilizationRegression', 'ServiceDemandLaw', 'WangKalmanFilter', 'KumarKalmanFilter', 'ResponsetimeRegression'], ncol=1)


plt.xlim(0, 180)
# Finish up plot
plt.tight_layout(pad=0.1)
plt.savefig("figure.pdf")
plt.show()