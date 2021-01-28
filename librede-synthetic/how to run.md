# How to run the experiment

This file contains a short instruction on how to execute the presented experiments.

## On the target machine (e.g., 10.1.234.186):

Run in two separate sessions:

First:

`./lmdaemon`

This starts the power-daemon, which is re-written in order to measure the CPU-utilization (contained in this folder).

Second: 

`sudo docker run -p 8080:8080 simoneismann/syntheticcomponents:librede`

This start the synthetic appliction as a Docker container, so the target machine should have Docker installed.

## On the load generator machine (e.g., 10.1.237.53):

Run the loadgenerator slave:

`java -jar httploadgenerator.jar loadgenerator`

Furthermore, ensure that all ports to the target and the director machine are open. The required jar file is included in this folder.

## On the director machine:

Start execution of the benchmark:

`java -cp load.jar:httploadgenerator.jar tools.descartes.dlim.httploadgenerator.runner.Main director --ip 10.1.237.53 --load longSingleSin54.csv --lua call_3wc.lua -p 10.1.234.186:22442 -c measurment.ProcListener -t 100 -o log.csv --randomize-users`

Make sure to replace the example IPs and load descriptions accordingly.

## Collecting results:

After the experment has terminated (as observable from the director machine), the following logs can be collected and parsed.

Collect the `timestamps.csv` from the load generator machine and the `log.csv` from the director machine.
Execute the parse script from librede-parse:

`python .\parse.py .\timestamps.csv .\log.csv`

to extract utilization and request class data.