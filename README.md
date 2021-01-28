# Experiment data for the SARDE project

This project contains data, tools, and scripts required to execute workloads and analyses intended for evaluating the Self-aware Resource Demand Estimation (SARDE) project. 
SARDE enables continuous resource demand estimations, while constantly adapting and optimizing its used estimators.
SARDE is designed as an AddOn to the classic LibReDE library.

Check out the source code of SARDE [here](https://gitlab2.informatik.uni-wuerzburg.de/descartes/librede-rrde), and LibReDE [here](https://bitbucket.org/librede/librede/src/master/) for more information.

The main publication for SARDE is currently under review at ACM Transactions on Autonomous and Adaptive Systems (TaaS).

This project currently contains four folders:

1. [librede-artificial_exp](librede-artificial_exp/): Contains the micro-benchmarks data set. 
This data set consists of a set of measurements obtained by executing micro-benchmarks on a real system. 
A set of 210 traces, each with approximately one hour run-time, was collected. 
The micro-benchmarks generate a closed workload with exponentially distributed think times and resource demands. 
The think times themselves were set to fit the targeted load level of each specific experiment. 
As mean values for the resource demands, we selected 14 different subsets of the base set (0.02s, 0.25s, 0.5s, 0.125s, and 0.13s) with a varying number of workload classes (1, 2, and 3} and target load levels (20%, 50%, and 80%) arbitrarily chosen from the base set. 
This way, we can ensure that the resource demands are not linearly growing across workload classes. 
Additionally, the subsets intentionally contained cases where two or three workload classes had the same mean resource demand.
The folder contains only experiments sampled every 1 second, then splits into the three different loads, each with 14 different experiment setting, which were each repeated 5 times.
In addition, a [script](librede-artificial_exp/remove_unnnecessary.py) for removing unnecessary files is provided, that might get created while experimenting on the data.

2.
