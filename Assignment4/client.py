import cv2
import socket
import numpy as np

HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, PORT))
print(f"[Client] Listening for video stream on {HOST}:{PORT}...")

frame_buffer = b''

while True:
    try:
        packet, _ = client_socket.recvfrom(65536)
        if not packet:
            continue
    except socket.error as e:
        print(f"[Error] Socket error: {e}")
        break

    marker = packet[0]
    data = packet[1:]
    frame_buffer += data

    if marker == 1:
        try:
            np_data = np.frombuffer(frame_buffer, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Receiving Video", frame)
            frame_buffer = b''
        except Exception as e:
            print(f"[Error] Decoding frame failed: {e}")
            frame_buffer = b''

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()
print("[Client] Stopped receiving video.")
