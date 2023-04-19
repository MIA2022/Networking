#!/usr/bin/env python3

import sys
import server

if len(sys.argv) < 3:
    print("Usage:")
    print("  Start server: ./ttt -s <port>")
    print("  Start client: ./ttt -c <hostname> <port>")
    sys.exit(1)

if sys.argv[1] == "-s":
    port = int(sys.argv[2])
    server.start_server(port)
else:
    print("Invalid argument. Use '-s' to start server")
    sys.exit(1)
