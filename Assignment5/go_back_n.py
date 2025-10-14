import random
import time

total_frames = 10
window_size = 4
loss_probability = 0.2
next_frame_to_send = 0
ack_expected = 0

while ack_expected < total_frames:
    # Send a window of frames
    print(f"\nSending frames {next_frame_to_send} to {min(next_frame_to_send + window_size - 1, total_frames - 1)}")
    time.sleep(1)

    for frame in range(next_frame_to_send, min(next_frame_to_send + window_size, total_frames)):
        # Randomly simulate loss
        if random.random() < loss_probability:
            print(f"Frame {frame} lost! Retransmitting all frames from {frame} onwards...")
            next_frame_to_send = frame
            break
    else:
        # All frames sent successfully
        ack = next_frame_to_send + window_size - 1
        if ack >= total_frames:
            ack = total_frames - 1
        print(f"ACK {ack} received")
        ack_expected = ack + 1
        next_frame_to_send = ack_expected
