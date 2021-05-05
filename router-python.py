###############################################################################
# router-python.py
# Name: Michael and Brian
###############################################################################

import sys
import socket

RECV_BUFFER_SIZE = 2048
QUEUE_LENGTH = 10



def router(router_port):
    """TODO: Listen on socket and send received message to server"""
    # create an INET, STREAMing socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as routersocket:
        # bind the socket to the host and its port
        routersocket.bind(('', router_port))
        routersocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # prepare for connection

        while True:
            routersocket.listen(QUEUE_LENGTH)
            # accept connections from outside
            (clientsocket, address) = routersocket.accept()
            
            with clientsocket:
                data = clientsocket.recv(RECV_BUFFER_SIZE)
                decoded_data = data.decode();
                data_list = decoded_data.split("\n")
                server_ip = data_list[0]
                server_port = data_list[1]

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((server_ip, int(server_port)))
                s.sendall(data)
                data = clientsocket.recv(RECV_BUFFER_SIZE)
                while True:
                    s.sendall(data)
                    clientsocket.settimeout(1.0)
                    try:                  
                        data = clientsocket.recv(RECV_BUFFER_SIZE)
                    except socket.timeout:
                        break

                    if not data:
                        break
                r_msg = s.recv(RECV_BUFFER_SIZE)

                while r_msg:
                    sys.stdout.flush()
                    clientsocket.sendall(r_msg)
                    r_msg = s.recv(RECV_BUFFER_SIZE)

                clientsocket.close()
                s.close()
    pass


def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python router-python.py [Router Port]")
    router_port = int(sys.argv[1])
    router(router_port)

if __name__ == "__main__":
    main()
