#!/usr/bin/python
import os


def calculate_throughputs():
    trace_lines = open('experiment2_output.tr').readlines()
    count1 = count2 = 0
    total_bits1 = total_bits2 = 0
    end_time1 = start_time1 = end_time2 = start_time2 = 0
    for line in trace_lines:
        elements = line.split()
        event, timestamp, src, packet_size, flow_id = elements[0], float(elements[1]), elements[2], int(elements[5]), elements[7]

        if flow_id == '1':
            if event == '+' and src == '2':
                if count1 == 0:
                    start_time1 = timestamp
                    count1 += 1
            if event == 'r':
                total_bits1 += 8 * packet_size
                end_time1 = timestamp

        if flow_id == '2':
            if event == '+' and src == '2':
                if count2 == 0:
                    start_time2 = timestamp
                    count2 += 1
            if event == 'r':
                total_bits2 += 8 * packet_size
                end_time2 = timestamp

    duration1, duration2 = end_time1 - start_time1, end_time2 - start_time2
    throughput1 = str(total_bits1 / duration1 / (1024 * 1024))
    throughput2 = str(total_bits2 / duration2 / (1024 * 1024))

    return throughput1, throughput2


def calculate_latencies():
    total_latency1 = total_latency2 = 0.0
    count1 = count2 = 0
    sent_timestamps1 = {}
    received_timestamps1 = {}
    sent_timestamps2 = {}
    received_timestamps2 = {}

    trace_lines = open('experiment2_output.tr').readlines()

    for line in trace_lines:
        elements = line.split()
        event, timestamp, src, dest, flow_id, seq_num = elements[0], float(elements[1]), elements[2], elements[3], elements[7], elements[10]

        if flow_id == '1':
            if event == '+' and src == '0':
                sent_timestamps1.update({seq_num: timestamp})
            if event == 'r' and dest == '0':
                received_timestamps1.update({seq_num: timestamp})

        if flow_id == '2':
            if event == '+' and src == '4':
                sent_timestamps2.update({seq_num: timestamp})
            if event == 'r' and dest == '4':
                received_timestamps2.update({seq_num: timestamp})

    common_packets1 = {x for x in sent_timestamps1.viewkeys() if x in received_timestamps1.viewkeys()}
    common_packets2 = {x for x in sent_timestamps2.viewkeys() if x in received_timestamps2.viewkeys()}

    for packet in common_packets1:
        start_time, end_time = sent_timestamps1[packet], received_timestamps1[packet]
        duration = end_time - start_time
        if duration > 0:
            total_latency1 += duration
            count1 += 1

    for packet in common_packets2:
        start_time, end_time = sent_timestamps2[packet], received_timestamps2[packet]
        duration = end_time - start_time
        if duration > 0:
            total_latency2 += duration
            count2 += 1

    avg_latency1 = (total_latency1 / count1) * 100
    avg_latency2 = (total_latency2 / count2) * 100

    return str(avg_latency1), str(avg_latency2)


def calculate_drop_rates():
    total_packets1 = total_packets2 = 0
    dropped_packets1 = dropped_packets2 = 0

    trace_lines = open('experiment2_output.tr').readlines()

    for line in trace_lines:
        elements = line.split()
        event, flow_id = elements[0], elements[7]

        if flow_id == '1':
            if event == 'd':
                dropped_packets1 += 1
            if event == '+':
                total_packets1 += 1

        if flow_id == '2':
            if event == 'd':
                dropped_packets2 += 1
            if event == '+':
                total_packets2 += 1

    drop_rate1 = str((float(dropped_packets1) / float(total_packets1)) * 100)
    drop_rate2 = str((float(dropped_packets2) / float(total_packets2)) * 100)

    return drop_rate1, drop_rate2


throughputData1, throughputData2 = calculate_throughputs()
latencyData1, latencyData2 = calculate_latencies()
dropData1, dropData2 = calculate_drop_rates()

print("\t" + throughputData1 + "\t" + throughputData2 + "\t" + latencyData1 + "\t"+ latencyData2 + "\t"+ dropData1 + "\t" + dropData2)

