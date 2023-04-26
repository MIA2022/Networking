import matplotlib.pyplot as plt


# Function to read data from a file
def read_data(file_name):
    with open(file_name, 'r') as f:
        content = f.read()

    algorithms = ['Tahoe', 'Reno', 'NewReno', 'Vegas']
    algorithm_data = content.split(
        '------------------------------------------------------------------------')
    parsed_data = {}

    for i, algo in enumerate(algorithms):
        subdata = algorithm_data[i].strip().split('\n')[2:]
        cbr, throughput, latency, packet_drop_rate = [], [], [], []

        for line in subdata:
            values = line.split()
            cbr.append(float(values[0]))
            throughput.append(float(values[1]))
            latency.append(float(values[2]))
            packet_drop_rate.append(float(values[3]))

        parsed_data[algo] = {'CBR': cbr, 'Throughput': throughput, 'Latency': latency,
                             'Packet Drop Rate': packet_drop_rate}

    return parsed_data


# Function to plot data
def plot_data(subdata, metric):
    plt.figure(figsize=(10, 5))
    for algo, values in subdata.items():
        plt.plot(values['CBR'], values[metric], label=algo)

    plt.xlabel('CBR Flow Rate')
    plt.ylabel(metric)
    plt.title(f'{metric} Comparison')
    plt.legend()
    plt.grid()
    plt.show()


data_file = 'data.txt'
data = read_data(data_file)

plot_data(data, 'Throughput')
plot_data(data, 'Latency')
plot_data(data, 'Packet Drop Rate')