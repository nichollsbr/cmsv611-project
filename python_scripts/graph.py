#!/usr/bin/env python
import re
import matplotlib.pyplot as plt
import json
import os

INT_TABLE = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


# converts words "one" through "five" to an int
def word_to_int(word):
    return INT_TABLE[word.lower()]


def parse_spark_output_file(header_name, name):
    delimiter = "Local Basic"
    thread_pattern = "([a-zA-Z]{3,5})\sthread"
    data_file_pattern = "-2018.*Z"
    out_fp = open(name)
    text = out_fp.read().strip().split(delimiter)
    data_dict = {}
    for line in text:
        data_file_name_group = re.search(data_file_pattern, line)
        thread_group = re.search(thread_pattern, line)
        if thread_group and data_file_name_group:
            thread_count = word_to_int(thread_group.group().split()[0])
            data_file_name = data_file_name_group.group()
            key1 = header_name + data_file_name
            key = key1.replace(":", "_")
            data_dict[key] = thread_count
    return data_dict

def generate_thread_count_peak_graph(data_directory, file_header, spark_output_path, plot_title, x_label, y_label, **kwargs):
    files = os.listdir(data_directory)

    thread_counts = parse_spark_output_file(file_header, spark_output_path)

    thread_nums = []
    max_peaks = []
    for a_file in files:
        pathed = os.path.join(data_directory, a_file)
        fp = open(pathed)
        data_obj = json.load(fp)
        peak_exec_mems = []
        for job in data_obj:
            # Get peak memory values from metric data and thread count of given job
            peak_exec_mems.append(int(job["peakExecutionMemory"]))
        thread_nums.append(thread_counts[a_file])
        max_peaks.append(max(peak_exec_mems))
        peak_exec_mems = []

    fig = plt.figure()
    fig.suptitle(plot_title, fontsize=14, fontweight='bold')
    plt.plot(thread_nums, max_peaks)
    plt.axis([0,6,0, kwargs.get("max_peak", 10000000)])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


DATAFRAME_DIRECTORY = r"/Users/bnicholls/Documents/School/cmsc611-project/stats/dataframe-stats"
SPARK_DATAFRAME_OUTPUT_FILE = r"/Users/bnicholls/Documents/School/cmsc611-project/stats/metrics-output/spark-stats-dataframe-task_metrics_run_output"
DATAFRAME_FILE_NAME = "BasicDataframeRunner"
DATAFRAME_PLOT_TITLE = "Spark DataFrame Metrics"
DATAFRAME_X_LABEL = "Thread Count"
DATAFRAME_Y_LABEL = "Peak Memory (Power of 7)"

generate_thread_count_peak_graph(DATAFRAME_DIRECTORY, DATAFRAME_FILE_NAME,
                                 SPARK_DATAFRAME_OUTPUT_FILE, DATAFRAME_PLOT_TITLE, DATAFRAME_X_LABEL, DATAFRAME_Y_LABEL)


DATASET_DIRECTORY = r"/Users/bnicholls/Documents/School/cmsc611-project/stats/dataset-stats"
SPARK_DATASET_OUTPUT_FILE = r"/Users/bnicholls/Documents/School/cmsc611-project/stats/metrics-output/spark-stats-dataset-task_metrics_run_output"
DATASET_FILE_NAME = "BasicDatasetRunner"
DATASET_PLOT_TITLE = "Spark Dataset Metrics"
DATASET_X_LABEL = "Thread Count"
DATASET_Y_LABEL = "Peak Memory (Power of 7)"

generate_thread_count_peak_graph(DATASET_DIRECTORY, DATASET_FILE_NAME,
                                 SPARK_DATASET_OUTPUT_FILE, DATASET_PLOT_TITLE, DATASET_X_LABEL, DATASET_Y_LABEL)

RDD_DIRECTORY = r"/Users/bnicholls/Documents/School/cmsc611-project/stats/rdd-stats"
SPARK_RDD_OUTPUT_FILE = r"/Users/bnicholls/Documents/School/cmsc611-project/stats/metrics-output/spark-stats-rdd-task_metrics_run_output"
RDD_FILE_NAME = "BasicRDDRunner"
RDD_PLOT_TITLE = "Spark RDD Metrics"
RDD_X_LABEL = "Thread Count"
RDD_Y_LABEL = "Peak Memory"

generate_thread_count_peak_graph(RDD_DIRECTORY, RDD_FILE_NAME,
                                 SPARK_RDD_OUTPUT_FILE, RDD_PLOT_TITLE, RDD_X_LABEL, RDD_Y_LABEL, max_peak=6000)