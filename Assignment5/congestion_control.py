import matplotlib.pyplot as plt
import random
cwnd = 1
ssthresh = 16
rounds = 20
loss_prob = 0.2

cwnd_values = []
round_numbers = []
for i in range(1, rounds + 1):
    round_numbers.append(i)
    cwnd_values.append(cwnd)
    print(f"Round {i}: cwnd = {cwnd}")

    # Randomly simulate packet loss
    if random.random() < loss_prob:
        print("Packet loss detected! Multiplicative decrease...")
        ssthresh = max(cwnd // 2, 1)
        cwnd = 1  # reset for slow start
        continue

    # Increase cwnd
    if cwnd < ssthresh:
        cwnd *= 2  # slow start
    else:
        cwnd += 1  # congestion avoidance
plt.plot(round_numbers, cwnd_values, marker='o')
plt.title("TCP Congestion Control Simulation")
plt.xlabel("Transmission Rounds")
plt.ylabel("Congestion Window (cwnd)")
plt.grid(True)
plt.show()
