proc experiment3 {agent queue} {
	#Create a simulator object
	global ns tf
	set ns [new Simulator]

	# Open the trace file
	set tf [open experiment3_output.tr w]
	$ns trace-all $tf

	#Set up the nodes
	set n1 [$ns node]
	set n2 [$ns node]
	set n3 [$ns node]
	set n4 [$ns node]
	set n5 [$ns node]
	set n6 [$ns node]

	# Set up the links
	$ns duplex-link $n1 $n2 10Mb 10ms $queue
    $ns duplex-link $n2 $n3 10Mb 10ms $queue
    $ns duplex-link $n2 $n5 10Mb 10ms $queue
    $ns duplex-link $n3 $n4 10Mb 10ms $queue
    $ns duplex-link $n3 $n6 10Mb 10ms $queue

    #Setting the queue limit
	$ns queue-limit $n1 $n2 10
	$ns queue-limit $n2 $n3 10
	$ns queue-limit $n2 $n5 10
	$ns queue-limit $n3 $n4 10
	$ns queue-limit $n3 $n6 10

	# Set TCP variant according to the argument
	#Setup a TCP connection from N1 to a sink at N4
	set tcp [new Agent/TCP/$agent]
    $ns attach-agent $n1 $tcp
    if {$agent == "Reno"} {
		 set sink [new Agent/TCPSink]
	}
	if {$agent == "Sack1"} {
		 set sink [new Agent/TCPSink/Sack1]
	}
	$ns attach-agent $n4 $sink
	$ns connect $tcp $sink
	$tcp set fid_ 1

	#Setting a window size
	$tcp set window_ 80
	$tcp set cwnd_ 100

	#Setting up the FTP over TCP connection
    set ftp [new Application/FTP]
    $ftp attach-agent $tcp
    $ftp set type_ FTP

    #Setup a UDP connection from source N5 and a sink at N6
    set udp [new Agent/UDP]
    $ns attach-agent $n5 $udp
    set null [new Agent/Null]
    $ns attach-agent $n6 $null
    $ns connect $udp $null
    $udp set fid_ 2

    #Setup a CBR over UDP connection
	set cbr [new Application/Traffic/CBR]
	$cbr attach-agent $udp
	$cbr set type_ CBR
	$cbr set rate_ 5mb

	# Set up the simulation start and stop times
	$ns at 0.1 "$ftp start"
	$ns at 2.0 "$cbr start"
	$ns at 9.5 "$ftp stop"
	$ns at 9.5 "$cbr stop"
	$ns at 10.0 "finish"

	#Defining finish procedure
	proc finish {} {
	    global ns tf
		$ns flush-trace
		close $tf
	    exit 0
	}

    # Run the simulation
	$ns run
}

# Calling the "experiment3" procedure created above
experiment3 [lindex $argv 0] [lindex $argv 1]
