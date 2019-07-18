import os

whitelist = ["host1_CPU_UTILIZATION.csv",
             "host1_THROUGHPUT.csv",
             "host1_VISIT_COUNTS.csv",
             "experiment1_WC2_RESPONSE_TIME.csv",
             "experiment1_WC2_ARRIVAL_TIMES.csv",
             "experiment1_WC1_RESPONSE_TIME.csv",
             "experiment1_WC1_ARRIVAL_TIMES.csv",
             "experiment1_WC0_RESPONSE_TIME.csv",
             "experiment1_WC0_ARRIVAL_TIMES.csv",
             "experiment1_VISIT_COUNTS.csv",
             "experiment1_THROUGHPUT.csv",
             "experiment1_AVERAGE_RESPONSE_TIME.csv"]

def to_delete(file):
    name = os.path.basename(file)
    if name in whitelist:
        return False
    return True
             
path = os.getcwd()
print(path)

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            if to_delete(file):
                files.append(os.path.join(r, file))

for f in files:
    print(f)
    os.remove(f)
