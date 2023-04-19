#!/usr/bin/env python3

import sys
import client

if len(sys.argv) < 3:
    print("Usage:")
    print("  Start server: ./ttt -s <port>")
    print("  Start client: ./ttt -c <hostname> <port>")
    sys.exit(1)

if sys.argv[1] == "-c":
    if len(sys.argv) < 4:
        print("Usage: ./ttt -c <hostname> <port>")
        sys.exit(1)
    hostname = sys.argv[2]
    port = int(sys.argv[3])
    client.start_client(hostname, port)
else:
    print("Invalid argument. Use '-c' to start client")
    sys.exit(1)


