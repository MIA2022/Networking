import matplotlib.pyplot as plt


# Function to read data from a file
def read_data(file_name):
    with open(file_name, 'r') as f:
        content = f.read()

    algorithms = ['Reno/Reno', 'NewReno/Reno', 'Vegas/Vegas', 'NewReno/Vegas']
    algorithm_data = content.split(
        '------------------------------------------------------------------------')
    parsed_data = {}

    for i, algo in enumerate(algorithms):
        subdata = algorithm_data[i].strip().split('\n')[2:]
        cbr, throughput1, throughput2, latency1, latency2, packet_drop_rate1, packet_drop_rate2 = [], [], [], [], [], [], []

        for line in subdata:
            values = line.split()
            cbr.append(float(values[0]))
            throughput1.append(float(values[1]))
            throughput2.append(float(values[2]))
            latency1.append(float(values[3]))
            latency2.append(float(values[4]))
            packet_drop_rate1.append(float(values[5]))
            packet_drop_rate2.append(float(values[6]))

        parsed_data[algo] = {'CBR': cbr, 'Throughput': (throughput1, throughput2),
                             'Latency': (latency1, latency2),
                             'Packet Drop Rate': (packet_drop_rate1, packet_drop_rate2)}
    print(parsed_data)

    return parsed_data


# Function to plot data
def plot_data(subdata, variants, performances):
    plt.figure(figsize=(10, 5))
    lables = variants.split('/')
    plt.plot(subdata[variants]['CBR'], subdata[variants][performances][0], label=lables[0])
    plt.plot(subdata[variants]['CBR'], subdata[variants][performances][1], label=lables[1])

    plt.xlabel('CBR Flow Rate')
    plt.ylabel(performances)
    plt.title(f'{variants} {performances} Comparison')
    plt.legend()
    plt.grid()
    plt.show()


data_file = 'experiment2data.txt'
data = read_data(data_file)

plot_data(data, 'Reno/Reno', 'Throughput')
plot_data(data, 'Reno/Reno', 'Latency')
plot_data(data, 'Reno/Reno', 'Packet Drop Rate')
plot_data(data, 'NewReno/Reno', 'Throughput')
plot_data(data, 'NewReno/Reno', 'Latency')
plot_data(data, 'NewReno/Reno', 'Packet Drop Rate')
plot_data(data, 'Vegas/Vegas', 'Throughput')
plot_data(data, 'Vegas/Vegas', 'Latency')
plot_data(data, 'Vegas/Vegas', 'Packet Drop Rate')
plot_data(data, 'NewReno/Vegas', 'Throughput')
plot_data(data, 'NewReno/Vegas', 'Latency')
plot_data(data, 'NewReno/Vegas', 'Packet Drop Rate')
