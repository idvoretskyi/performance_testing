#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
from pprint import pprint
import argparse
import csv
import os

def read_file_lines(path):
    with open(path, "r") as o:
        for line in o.readlines():
            yield line

def split_clean_line(line):
    return map(lambda x: x.strip(), line.split(","))

def combine_data(parsed_files):

    combined = {}

    for p in parsed_files:
        for k, v in p.items():
	    if "Percentile" in k: 
		pass	

            elif "MaxLatency" in k:

		key = "{}_max".format(k)
		combined.setdefault(key, 0)
		combined[key] = max(combined[key], v) 

	    elif "MinLatency" in k:

		key = "{}_min".format(k)
		combined.setdefault(key, v)
		combined[key] = min(combined[key], v) 


	    elif "Operations" in k or "Throughput" in k:

		key = "{}_total".format(k)
		combined.setdefault(key, 0)
		combined[key] += v

            elif k.startswith("[READ]_data") or k.startswith("[UPDATE]_data") or k.startswith("OVERALL_"):

                #Create list for mean calculation later
                running_list = combined.setdefault("{}_mean".format(k), [])
                running_list.append(v)

            elif k.startswith("[READ]") or k.startswith("[UPDATE]"):

                #Sum up histogram values
                key = "{}_total".format(k)
                combined.setdefault(key, 0)
                combined[key] += v

    for k,v in combined.items():
        if k.endswith("_mean"):
            combined[k] = sum(v) / len(v)

    return combined

def parse_file(path):

    data = {}

    for line in read_file_lines(path):
        if line.startswith("[READ]") or line.startswith("[UPDATE]"):

            operation, index, value = split_clean_line(line)

            if index.isdigit():
                data["{0}_{1:03d}".format(operation, int(index))] = int(value)
            elif index.startswith(">"):
                data["{0}_{1:03d}".format(operation, int(1000))] = int(value)
            else:
                data["{}_data_{}".format(operation, index)] = float(value)

        elif line.startswith("[OVERALL]"):
            operation, name, value = split_clean_line(line)
            data["OVERALL_{}".format(name)] = float(value)

    return data

def write_data(data, path):
    with open(path, "w") as o:
        fieldnames = sorted(data.keys())
        writer = csv.DictWriter(o, fieldnames=fieldnames)
        headers = {key:key for key in fieldnames}
        writer.writerow(headers)
        writer.writerow(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YCSB output parser')
    parser.add_argument("-o", "--output", action="store", dest="output_path", type=str, default=os.path.abspath("."))
    source_group = parser.add_mutually_exclusive_group(required = True)
    source_group.add_argument('-f', "--file_path", action="store", dest="file_path", type=str)
    source_group.add_argument('-d', "--dir_path", action="store", dest="dir_path", type=str)
    args = parser.parse_args()

    if args.dir_path:
        full_path = os.path.abspath(args.dir_path)
        output_file_paths = (os.path.join(full_path, x) for x in os.listdir(full_path) if x.endswith(".out"))
        parsed_files = [parse_file(x) for x in output_file_paths]
        data = combine_data(parsed_files)

    else:
        data = parse_file(args.file_path)

    output_file_path = os.path.join(args.output_path, "output.csv")
    write_data(data, output_file_path)

