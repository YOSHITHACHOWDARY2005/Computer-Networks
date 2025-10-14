import random
import time
total_frames = 5  # number of frames to send
loss_probability = 0.3  # 30% chance a frame or ACK gets lost
timeout = 2  # seconds before retransmission
for frame in range(total_frames):
    print(f"\nSending Frame {frame}")
    time.sleep(1)

    # Randomly decide if frame is lost
    if random.random() < loss_probability:
        print(f"Frame {frame} lost, retransmitting after timeout...")
        time.sleep(timeout)
        print(f"Retransmitting Frame {frame}")
        print(f"ACK {frame} received")
    else:
        # Randomly decide if ACK is lost
        if random.random() < loss_probability:
            print(f"ACK {frame} lost, retransmitting frame after timeout...")
            time.sleep(timeout)
            print(f"Retransmitting Frame {frame}")
            print(f"ACK {frame} received")
        else:
            print(f"ACK {frame} received")
