###############################################################################
# client-python.py
# Name: Michael and Brian
###############################################################################

import sys
import socket

SEND_BUFFER_SIZE = 2048

def client(server_ip, server_port, router_ip, router_port):
    """TODO: Open socket and send message from sys.stdin"""
    # create an INET, STREAMing socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # now connect to router
        s.connect((router_ip, router_port))
        
        with open(0, "rb") as fd:
            encoded_msg = str(server_ip) + "\n" + str(server_port) + "\n"
            s.send(encoded_msg.encode())
            while True:
                content = sys.stdin.buffer.raw.read(SEND_BUFFER_SIZE)
                if not content: break
                sent = s.sendall(content)
                if sent == 0:
                    raise RuntimeError("socket connection broken")

            r_msg = s.recv(SEND_BUFFER_SIZE)
            while r_msg:
                sys.stdout.buffer.raw.write(r_msg)
                sys.stdout.flush()
                s.settimeout(1.0)
                try:    
                    r_msg = s.recv(SEND_BUFFER_SIZE)
                except socket.timeout:
                    break

            s.close()

    pass


def main():
    """Parse command-line arguments and call client function """
    if len(sys.argv) != 5:
        sys.exit("Usage: python3 client-python.py [Server IP] [Server Port] [Router IP] [Router Port] < [message]")
    router_ip = sys.argv[3]
    router_port = int(sys.argv[4])
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    client(server_ip, server_port, router_ip, router_port)

if __name__ == "__main__":
    main()
