# CHARON :
# Script for TCP chat server - relays messages to all clients 

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 5050
BUFSIZ = 1024
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SOCK.accept()
        print("[+] %s connected." % str(client_address))
        client.send("[+] The EYES : \n".encode("utf8"))
        client.send("[+] Type your name !".encode("utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(conn, addr):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = conn.recv(BUFSIZ).decode("utf8")
    print("[+] %s named (%s)" % ((addr),name))
    welcome = '[+] Welcome %s ! [ #quit to exit ]' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "[+] %s joined." % name
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(BUFSIZ)
        if msg != bytes("#quit", "utf8"):
            broadcast(msg, "[+] "+ name + " >> ")
        else:
            conn.send(bytes("#quit", "utf8"))
            print("[+] %s :: %s :: left." % ((addr),name))
            conn.close()
            del clients[conn]
            broadcast(bytes("[+] %s left." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SOCK.listen(5)  # Listens for 5 connections at max.
    print("[+] Chat Server start running on port %s ..." % str(PORT))
    print("[+] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()
