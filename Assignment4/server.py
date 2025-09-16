import cv2
import socket
import time
HOST = '127.0.0.1'  
PORT = 9999
CLIENT_ADDR = (HOST, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    cap = cv2.VideoCapture('video.mp4')
    if not cap.isOpened():
        raise IOError("Cannot open video.mp4")
except Exception as e:
    print(f"Error opening video file: {e}")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = 1 / fps  
print(f"Streaming video at {fps:.2f} FPS...")
CHUNK_SIZE = 60000 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or failed to read frame.")
        break 
    frame = cv2.resize(frame, (640, 480))
    
    result, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    if not result:
        continue
    buffer_bytes = buffer.tobytes()
    buffer_size = len(buffer_bytes)

    for i in range(0, buffer_size, CHUNK_SIZE):
        chunk = buffer_bytes[i:i + CHUNK_SIZE]
        marker = b'\x01' if (i + CHUNK_SIZE) >= buffer_size else b'\x00'
        
        try:
            server_socket.sendto(marker + chunk, CLIENT_ADDR)
        except socket.error as e:
            print(f"Socket Error: {e}")
            break
    time.sleep(frame_interval)
cap.release()
server_socket.close()
print("Streaming finished.")