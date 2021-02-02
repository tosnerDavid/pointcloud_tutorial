import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_values(path, bins_count=255):
    data = pd.read_csv(path, sep=",", skipinitialspace=True)
    values = data['Coord. Z']
    n, bins, patches = plt.hist(values, bins=bins_count)

    norm = (n - min(n)) / (max(n) - min(n))

    return norm

def moving_average(data, window_size=10):
    data_df = pd.DataFrame(data, columns=['value'])
    return data_df.value.rolling(10, min_periods=1).mean()

bins_count = 255

graph_1 = read_values("C:/Users/david/Downloads/sceny_segmentace/outputs_csv/CC#1.txt")
graph_2 = read_values("C:/Users/david/Downloads/sceny_segmentace/outputs_csv/CC#2.txt")
diff = abs(graph_2-graph_1)
diff_mean = np.mean(diff)

plt.clf()
plt.close('all')

fig1 = plt.figure()
fig1.suptitle('Coordinates in Z, mean_diff=%f' %diff_mean, fontsize=20)
plt.plot(graph_1, color='red', label='cloud_1')
plt.plot(graph_2, color='green', label='cloud_2')
plt.plot(diff, color='blue', label='diff')
plt.hlines(diff_mean, 0, bins_count, color="yellow", label='mean')
plt.legend(loc='best')
plt.draw()

graph_1_ma = moving_average(graph_1,10)
graph_2_ma = moving_average(graph_2,10)
diff_ma = abs(graph_2_ma-graph_1_ma)
diff_ma_mean = np.mean(diff_ma)

fig2 = plt.figure()
fig2.suptitle('Coordinates in Z (MA), mean_diff=%f' %diff_mean, fontsize=20)
plt.plot(graph_1_ma, color='red', label='cloud_1')
plt.plot(graph_2_ma, color='green', label='cloud_2')
plt.plot(diff_ma, color='blue', label='diff')
plt.hlines(diff_ma_mean, 0, bins_count, color="yellow", label='mean')
plt.legend(loc='best')
plt.show()