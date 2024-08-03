from matplotlib import pyplot as plt

file = "./side_dist_history.txt"
# read a line at a time
dists = []
times = []
with open(file, "r") as f:
    for line in f:
        dist, time = line.split(" ")
        dists.append(float(dist))
        times.append(float(time))

plt.plot(times, dists)
plt.show()
