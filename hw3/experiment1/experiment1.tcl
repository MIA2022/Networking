proc experiment1 {agent rate} {
	#Create a simulator object
	global ns tf
	set ns [new Simulator]

	# Open the trace file
	set tf [open experiment1_output.tr w]
	$ns trace-all $tf

	#Set up the nodes
	set n1 [$ns node]
	set n2 [$ns node]
	set n3 [$ns node]
	set n4 [$ns node]
	set n5 [$ns node]
	set n6 [$ns node]

	# Set up the links
	$ns duplex-link $n1 $n2 10Mb 2ms DropTail
    $ns duplex-link $n2 $n3 10Mb 2ms DropTail
    $ns duplex-link $n2 $n5 10Mb 2ms DropTail
    $ns duplex-link $n3 $n4 10Mb 2ms DropTail
    $ns duplex-link $n3 $n6 10Mb 2ms DropTail

    #Setting the queue limit
	$ns queue-limit $n2 $n3 10

	# Set TCP variant according to the argument
	#Setup a TCP connection from N1 to a sink at N4
	if {$agent == "Tahoe"} {
		set tcp [new Agent/TCP]
	} else {
		set tcp [new Agent/TCP/$agent]
	}
    $ns attach-agent $n1 $tcp
    set sink [new Agent/TCPSink]
	$ns attach-agent $n4 $sink
	$ns connect $tcp $sink
	$tcp set fid_ 1

	#Setting up the FTP over TCP connection
    set ftp [new Application/FTP]
    $ftp attach-agent $tcp
    $ftp set type_ FTP

    #Setup a UDP connection from source N2 and a sink at N3
    set udp [new Agent/UDP]
    $ns attach-agent $n2 $udp
    set null [new Agent/Null]
    $ns attach-agent $n3 $null
    $ns connect $udp $null
    $udp set fid_ 2

    #Setup a CBR over UDP connection
	set cbr [new Application/Traffic/CBR] 
	$cbr attach-agent $udp
	$cbr set type_ CBR
	$cbr set packetSize_ 500
	$cbr set rate_ ${rate}mb
	$cbr set random_ false 

	# Set up the simulation start and stop times
	$ns at 0.1 "$cbr start"
	$ns at 1.0 "$ftp start"
	$ns at 14.0  "$ftp stop"
	$ns at 14.5 "$cbr stop"
	$ns at 15.0 "finish"

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

# Calling the "experiment1" procedure created above
experiment1 [lindex $argv 0] [lindex $argv 1]
