
.PHONY: all clean

all: server_ttt client_ttt

server_ttt: server_main.py
	cp server_main.py server_ttt
	chmod +x server_ttt

client_ttt: client_main.py
	cp client_main.py client_ttt
	chmod +x client_ttt

clean:
	rm -f server_ttt client_ttt
