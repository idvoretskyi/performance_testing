import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import re
import pandas as pd
import logging
import glob
import os
import sys
from secrets import API_KEY

USERNAME = 'dalanmiller'
# FORMAT = '%(asctime)-15s %(user)-8s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == "__main__":

    py.sign_in(USERNAME, API_KEY)
    joined_path = os.path.join(os.path.expanduser("~"), "repos/performance_testing/2.1.5-pre results/[a,c]/16.csv")
    globs = glob.glob(joined_path)

    a_bars = []
    c_bars = []

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
            regex = re.compile(r"^\[UPDATE\]\_\d\d\d\_total")
        elif '/c/' in path:
            regex = re.compile(r"^\[READ\]\_\d\d\d\_total")
        else:
            logging.error("Something went wrong with pathing")
            sys.exit(1)

        # Filter data columns down based on regex
        data = data.filter(regex=regex)

        # Build proper labels rather than "001"
        x_labels = ["{}ms".format(x.split('_')[1]) for x in data.columns.values]

        # Append to array of Bar charts depending on workload
        if workload == "a":
            a_bars.append(go.Bar(x=x_labels[:26], y=data.iloc[0].values[:26], name="{} nodes".format(cluster)))
        elif workload == "c":
            c_bars.append(go.Bar(x=x_labels[:26], y=data.iloc[0].values[:26], name="{} nodes".format(cluster)))

    a_layout = go.Layout(
        barmode='group',
        title="Latency distribution of writes in YCSB Workload A \n in a 16 node RethinkDB cluster",
        )
    a_fig = go.Figure(data=a_bars, layout=a_layout)
    plot_url = py.plot(a_fig, filename='workload-a-16-node-latency-distribution', auto_open=False)
    print(plot_url)
    c_layout = go.Layout(
        barmode='group',
        title="Latency distribution of reads in YCSB Workload C \n in a 16 node RethinkDB cluster",
        )
    c_fig = go.Figure(data=c_bars, layout=c_layout)
    plot_url = py.plot(c_fig, filename='workload-c-16-node-latency-distribution', auto_open=False)
    print(plot_url)
    # distplot_url = py.plot(fig, filename="{}-{}".format(workload, 16), validate=False)

    # bar_url = py.plot(plot_data, filename="{}-{}".format(workload, 16))
    # print(bar_url)
