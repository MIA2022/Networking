This study conducted experiments to analyze the performance of TCP variants (Tahoe, Reno, NewReno, and Vegas) under congestion, 
fairness between TCP variants, and the influence of queuing disciplines on overall throughput. These experiments are significant 
as they provide insights into the behavior of different TCP variants under various network conditions, which can help optimize 
network performance and ensure fairness among users.

Experiment 1

The results from the first experiment shed light on the strengths and weaknesses of each TCP variant under congestion. 
Understanding how different TCP variants perform in the presence of unresponsive flows, such as the CBR/UDP flow, 
is crucial for enhancing network efficiency and user experience.
In the koury linux machine, I upload experiment1.tcl tcl script code , analyzeData1 python script code , runExperiment1 Bash shell script, 
and use command order “chmod +x analyzeData1”, “chmod +x runExperiment1”, “./runExperiment1” to run NS-2 simulation 
and get the throughput, packet drop rate, and latency data of the specified TCP stream according to the different CBR flow's rate 
and store them into experiment1data file.


Experiment 2

In the second experiment, we investigated the fairness between different TCP variants. The results revealed that some 
combinations of TCP variants were more unfair than others, and that the fairness could be affected by the design and 
implementation of the TCP protocols. 
In the koury linux machine, I upload experiment2.tcl tcl script code , analyzeData2 python script code , runExperiment2 Bash shell script, 
and use command order “chmod +x analyzeData2”, “chmod +x runExperiment2”, “./runExperiment2” to run NS-2 simulation 
and get three graphs for each pair of TCP variants(Reno/Reno, NewReno/Reno, Vegas/Vegas, NewReno/Vegas). 
The graphs represents the average throughput, packet loss rate, 
and latency of two TCP flows respectively according to the different CBR flow's rate!


Experiment 3

The third experiment focused on the influence of queuing disciplines, such as DropTail and RED, on the overall throughput of TCP and CBR flows. 
In the koury linux machine, I upload experiment3.tcl tcl script code , analyzeData3 python script code , runExperiment3 Bash shell script, 
and use command order “chmod +x analyzeData3”, “chmod +x runExperiment3”, “./runExperiment3” to run NS-2 simulation 
and get latency Comparison and throughput comparison among between queuing disciplines!

