#!/usr/bin/env python3

import socket
import argparse
import json
import sys

def recv_line(conn):
    data = b''
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
        if b'\n' in chunk:
            break
    if not data:
        return None
    line, _, _ = data.partition(b'\n')
    return line.decode('utf-8').strip()

def send_line(conn, obj):
    s = json.dumps(obj) + '\n'
    conn.sendall(s.encode('utf-8'))

def prompt_name_and_number():
    name = input("Enter your name (e.g. 'Client of John Q. Smith'): ").strip()
    while True:
        s = input("Enter an integer between 1 and 100: ").strip()
        try:
            n = int(s)
        except:
            print("Invalid integer. Try again.")
            continue
        if 1 <= n <= 100:
            return name, n
        else:
            print("Number must be between 1 and 100 (inclusive). Try again.")

def main():
    parser = argparse.ArgumentParser(description="Simple TCP client for assignment")
    parser.add_argument('--server-ip', required=True)
    parser.add_argument('--port', type=int, default=5001)
    args = parser.parse_args()

    client_name, client_number = prompt_name_and_number()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((args.server_ip, args.port))
    except Exception as e:
        print("Could not connect to server:", e)
        sys.exit(1)

    payload = { "name": client_name, "number": client_number }
    try:
        send_line(sock, payload)
    except Exception as e:
        print("Error sending data:", e)
        sock.close()
        sys.exit(1)

    try:
        line = recv_line(sock)
        if line is None:
            print("Server closed connection without reply.")
            sock.close()
            sys.exit(1)
        reply = json.loads(line)
    except Exception as e:
        print("Error receiving/parsing reply:", e)
        sock.close()
        sys.exit(1)

    server_name = reply.get('name', '<unknown>')
    try:
        server_number = int(reply.get('number', 0))
    except:
        server_number = 0

    print("\n----- Exchange Result -----")
    print("Client's name:", client_name)
    print("Server's name:", server_name)
    print("Client's integer:", client_number)
    print("Server's integer:", server_number)
    print("Sum:", client_number + server_number)
    print("---------------------------")

    sock.close()

if __name__ == '__main__':
    main()
