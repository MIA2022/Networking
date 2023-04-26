#!/usr/bin/python
import os


def calculate_throughput():
    trace_data = open('experiment1_output.tr').readlines()
    num_lines = 0
    total_data_bits = 0
    end_time = 0
    start_time = 0
    for data_line in trace_data:
        split_line = data_line.split()
        event_type = split_line[0]
        event_time = float(split_line[1])
        node_source = split_line[2]
        packet_size = int(split_line[5])
        flow_id = split_line[7]
        if flow_id == '1':
            if event_type == '+' and node_source == '0':
                if num_lines == 0:
                    start_time = event_time
                    num_lines += 1
            if event_type == 'r':
                total_data_bits += 8 * packet_size
                end_time = event_time
    time_duration = end_time - start_time
    throughput = total_data_bits / time_duration / (1024 * 1024)
    return str(throughput)


def calculate_latency():
    total_latency = 0.0
    num_packets = 0
    send_time = {}
    arrival_time = {}
    trace_data = open('experiment1_output.tr').readlines()
    for data_line in trace_data:
        split_line = data_line.split()
        event_type = split_line[0]
        event_time = float(split_line[1])
        node_source = split_line[2]
        node_destination = split_line[3]
        flow_id = split_line[7]
        sequence_num = (split_line[10])
        if flow_id == '1':
            if event_type == '+' and node_source == '0':
                send_time.update({sequence_num: event_time})
            if event_type == 'r' and node_destination == '0':
                arrival_time.update({sequence_num: event_time})
    matched_packets = {x for x in send_time.keys() if x in arrival_time.keys()}
    for packet in matched_packets:
        start_time = send_time[packet]
        end_time = arrival_time[packet]
        duration = end_time - start_time
        if duration > 0:
            total_latency += duration
            num_packets += 1
    average_latency = (total_latency / num_packets) * 1000
    latency_str = str(average_latency)
    return latency_str


def calculate_drop_rate():
    total_packets = 0
    dropped_packets = 0
    trace_data = open('experiment1_output.tr').readlines()
    for data_line in trace_data:
        split_line = data_line.split()
        event_type = split_line[0]
        flow_id = split_line[7]
        if flow_id == '1':
            if event_type == 'd':
                dropped_packets += 1
            if event_type == '+':
                total_packets += 1
    drop_rate_percentage = (float(dropped_packets) / float(total_packets)) * 100
    return str(drop_rate_percentage)


throughputData = calculate_throughput()
latencyData = calculate_latency()
dropData = calculate_drop_rate()

print("\t" + throughputData + "\t\t" + latencyData + "\t\t" + dropData)


