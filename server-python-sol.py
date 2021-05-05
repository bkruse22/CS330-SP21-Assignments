###############################################################################
# server-python.py
# Name: Michael and Brian
###############################################################################

import sys
import socket

RECV_BUFFER_SIZE = 2048
QUEUE_LENGTH = 10



def server(server_port):
    """TODO: Listen on socket and print received message to sys.stdout"""
    # create an INET, STREAMing socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        # bind the socket to the host and its port
        serversocket.bind(('', server_port))
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # prepare for connection

        while True:
            # accept connections from outside
            serversocket.listen(QUEUE_LENGTH)

            (router_socket, address) = serversocket.accept()

            with router_socket:
                count = 0
                data = router_socket.recv(RECV_BUFFER_SIZE)
                while True:
                    # receive data and print it out
                    
                    if count == 0:
                        decoded_data = data.decode()
                        data_list = decoded_data.split("\n")
                        for i in data_list:
                            s_ip = data_list[0]
                            s_port = data_list[1]
                        
                        if s_ip != "127.0.0.1" and s_port != server_port:
                            print("ERROR: Incorrect IP and/or Port Number")
                            pass

                        count += 1

                    else:
                        sys.stdout.buffer.raw.write(data)
                        sys.stdout.flush()
                        
                        if count == 1:
                            server_msg = "[SERVER RECEIVED]: "
                            router_socket.sendall(server_msg.encode())
                        router_socket.sendall(data)
                        count += 1

                    router_socket.settimeout(1.0)
                    try:
                        data = router_socket.recv(RECV_BUFFER_SIZE)
                    except socket.timeout:
                        break

                router_socket.close()    
    pass


def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 4:
        sys.exit("Usage: python server-python.py [Server Port] [Router IP] [Router Port]")
    server_port = int(sys.argv[1])
    router_ip = sys.argv[2]
    router_port = sys.argv[3]

    server(server_port)

if __name__ == "__main__":
    main()
