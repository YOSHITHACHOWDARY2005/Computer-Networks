#!/usr/bin/env python3

import socket
import argparse
import json
import random
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

def main():
    parser = argparse.ArgumentParser(description="Simple TCP server for assignment")
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--name', default='Server of Your Name')
    parser.add_argument('--number', type=int, default=None)
    args = parser.parse_args()

    server_name = args.name
    fixed_number = args.number

    if args.port <= 5000:
        print("Please use a port number greater than 5000.")
        sys.exit(1)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((args.host, args.port))
    server_sock.listen(5)
    print(f"[SERVER] Listening on {args.host}:{args.port} ...")

    try:
        while True:
            conn, addr = server_sock.accept()
            print(f"\n[SERVER] Connection from {addr}")
            try:
                line = recv_line(conn)
                if line is None:
                    print("[SERVER] No data received; closing connection.")
                    conn.close()
                    continue

                try:
                    data = json.loads(line)
                except Exception as e:
                    print("[SERVER] Received invalid JSON:", e)
                    conn.close()
                    continue

                client_name = data.get('name', '<unknown>')
                try:
                    client_number = int(data.get('number', 0))
                except:
                    client_number = 0

                #print("Client's name:", client_name)
                #print("Server's name:", server_name)

                if not (1 <= client_number <= 100):
                    print("[SERVER] Received number outside 1-100. Closing sockets and terminating as required.")
                    conn.close()
                    server_sock.close()
                    sys.exit(1)

                server_number = fixed_number if fixed_number is not None else random.randint(1, 100)

                print("Client's integer:", client_number)
                print("Server's integer:", server_number)
                print("Sum:", client_number + server_number)

                reply = { "name": server_name, "number": server_number }
                send_line(conn, reply)

                conn.close()
            except Exception as e:
                print("[SERVER] Error while handling connection:", e)
                try:
                    conn.close()
                except:
                    pass

    except KeyboardInterrupt:
        print("\n[SERVER] Keyboard interrupt received. Shutting down.")
    finally:
        server_sock.close()

if __name__ == '__main__':
    main()
