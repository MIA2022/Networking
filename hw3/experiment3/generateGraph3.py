import matplotlib.pyplot as plt


# Function to read data from a file
def read_data(file_name):
    with open(file_name, 'r') as f:
        content = f.read()

    algorithms = ['Reno/RED', 'Reno/DropTail', 'Sack/RED', 'Sack/DropTail']
    algorithm_data = content.split(
        '------------------------------------------------------------------------')
    parsed_data = {}

    for i, algo in enumerate(algorithms):
        subdata = algorithm_data[i].strip().split('\n')[2:]
        time, throughput_tcp, throughput_cbr, latency = [], [], [], []
        reading_latency = False
        for line in subdata:
            if "Time" in line and "Latency" in line:
                reading_latency = True
                continue

            if not reading_latency:
                t, tcp, cbr = line.split()
                time.append(float(t))
                throughput_tcp.append(float(tcp))
                throughput_cbr.append(float(cbr))
            else:
                t, lat = line.split()
                latency.append(float(lat))

        parsed_data[algo] = {'time': time, 'throughput_tcp': throughput_tcp,
                             'throughput_cbr': throughput_cbr, 'Latency': latency}

    return parsed_data


# Function to plot data
def plot_data(subdata, metric):
    plt.figure(figsize=(10, 5))
    t=0
    for algo, values in subdata.items():
        if metric == 'Throughput':
            plt.plot(values['time'], values['throughput_tcp'], label=algo)
            if t < 1:
                plt.plot(values['time'], values['throughput_cbr'], label='CBR')
                t += 1
        else:
            plt.plot(values['time'], values['Latency'], label=algo)

    plt.xlabel('Time')
    plt.ylabel(metric)
    plt.title(f'{metric} Comparison')
    plt.legend()
    plt.grid()
    plt.show()


data_file = 'data.txt'
data = read_data(data_file)

plot_data(data, 'Throughput')
plot_data(data, 'Latency')