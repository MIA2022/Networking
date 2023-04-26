#!/usr/bin/python
import os


def calculate_throughput():
    file_path = 'experiment3_output.tr'
    time_interval = 0.5
    clock = 0.0
    total_bits_tcp = 0
    total_bits_cbr = 0

    print("Time\tThroughput_tcp\tThroughput_cbr")

    with open(file_path, 'r') as file:
        trace_lines = file.readlines()

    for line in trace_lines:

        trace_value = line.split()
        event = trace_value[0]
        time = float(trace_value[1])
        size = int(trace_value[5])
        fid = trace_value[7]

        if fid == '1' and event == 'r':
            total_bits_tcp += 8 * size

        if fid == '2' and event == 'r':
            total_bits_cbr += 8 * size

        if time - clock > time_interval:
            throughput_tcp = float(total_bits_tcp) / time_interval / (1024 * 1024)
            throughput_cbr = float(total_bits_cbr) / time_interval / (1024 * 1024)
            print(str(clock) + "\t" + str(throughput_tcp) + "\t" + str(throughput_cbr))

            clock += time_interval
            total_bits_tcp = 0
            total_bits_cbr = 0


def calculate_latency():
    file_path = 'experiment3_output.tr'
    time_interval = 0.5
    clock = 0.0
    total_latency = 0.0
    packet_count = 0
    send_times = {}
    arrival_times = {}

    print("Time\tLatency")

    with open(file_path, 'r') as file:
        trace_lines = file.readlines()

    for line in trace_lines:
        trace_value = line.split()
        event = trace_value[0]
        time = float(trace_value[1])
        source = trace_value[2]
        dest = trace_value[3]
        fid = trace_value[7]
        seq = (trace_value[10])

        if fid == '1':
            if event == '+' and source == '0':
                send_times[seq] = time
            if event == 'r' and dest == '0':
                arrival_times[seq] = time

        if time - clock > time_interval:
            common_packets = {x for x in send_times.keys() if x in arrival_times.keys()}

            for packet in common_packets:
                start = send_times[packet]
                end = arrival_times[packet]
                duration = float(end) - float(start)

                if duration > 0:
                    total_latency += duration
                    packet_count += 1

            if packet_count == 0:
                avg_latency = 0
            else:
                avg_latency = (total_latency / packet_count) * 1000

            print(str(clock) + '\t' + str(avg_latency))

            clock += time_interval
            send_times.clear()
            arrival_times.clear()
            packet_count = 0
            total_latency = 0.0


calculate_throughput()
calculate_latency()

