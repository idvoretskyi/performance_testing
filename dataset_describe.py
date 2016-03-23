import re
import pandas as pd
import logging
import glob
import os
import sys

# FORMAT = '%(asctime)-15s %(user)-8s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == "__main__":

    joined_path = os.path.join(os.path.expanduser("~"), "repos/performance_testing/2.1.5-pre results/[a,c]/16.csv")
    globs = glob.glob(joined_path)

    a_bars = []
    c_bars = []

    a_regex = re.compile(r"^\[UPDATE\]\_\d\d\d\_total")
    c_regex = re.compile(r"^\[READ\]\_\d\d\d\_total")

    # Iterate over sorted list of globs
    for path in sorted(globs, key= lambda path: int(path.split("/")[-1].split(".")[0])):
        logging.info(path)
        # Split out workload and cluster #
        workload, cluster = path.split("/")[-2:]
        cluster = cluster.split(".")[0]

        # Read in data from the csv file into a a dataframe
        data = pd.DataFrame.from_csv(path)

        # Construct regex if A workload or C workload
        if '/a/' in path:
            regex = a_regex
        elif '/c/' in path:
            regex = c_regex
        else:
            logging.error("Something went wrong with pathing")
            sys.exit(1)

        # Filter data columns down based on regex
        data = data.filter(regex=regex)

        # Append to array of Bar charts depending on workload
        if workload == "a":
            a_bars.append({ "{}-{}".format(workload,cluster): data })
        elif workload == "c":
            c_bars.append({ "{}-{}".format(workload,cluster): data })

    print(a_bars)
    print(c_bars)
