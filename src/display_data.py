import numpy as np, time, datetime, os, sys, json
from reader.reader import get_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if len(sys.argv) != 2:
    print("----------------------------")
    print("Invalid number of arguments.")
    print("py display_data.py <DATA_FILE>")
    exit()

data_file = sys.argv[1]
data = get_data(data_file)

d = pd.DataFrame(data=data)
d_low = d.filter(['l','t'], axis=1)
d_high = d.filter(['h','t'], axis=1)
d_avg = d.filter(['l', 'h','t'], axis=1)

d_low['sec'] = d_low.apply(lambda x: 'low', axis=1)
d_high['sec'] = d_high.apply(lambda x: 'high', axis=1)
d_avg['sec'] = d_avg.apply(lambda x: 'avg', axis=1)


d_low = d_low.rename(columns={'l': 'val'})
d_high = d_high.rename(columns={'h': 'val'})
d_avg['val'] = d_avg.apply(lambda x: (x['l'] + x['h']) / 2, axis=1)

# Bands
d_band_high = d_avg.copy()
d_band_low = d_avg.copy()
d_band_high['sec'] = d_avg.apply(lambda x: 'boll_high', axis=1)
d_band_low['sec'] = d_avg.apply(lambda x: 'boll_low', axis=1)
std_dev_arr = []

rolling_count = 10
for i, n in enumerate(d_band_high['val']):
    rel = np.array([])
    for q in range(i - 10, i + 1):
        if q >= 0:
            rel = np.append(rel, d_band_high['val'][q])
    
    mean = np.sum(rel) / len(rel)
    std_dev = np.sqrt(np.sum(np.square(rel - mean) / len(rel)))
    std_dev_arr.append(std_dev)


# Apply to dataframes
boll_range = 6

d_band_high['std_dev'] = pd.Series(std_dev_arr, index=d_band_high.index)
d_band_low['std_dev'] = pd.Series(std_dev_arr, index=d_band_low.index)

d_band_high['val'] = d_band_high.apply(lambda x: x['val'] + x['std_dev'] * boll_range, axis=1)
d_band_low['val'] = d_band_low.apply(lambda x: x['val'] - x['std_dev'] * boll_range, axis=1)

d_range = pd.concat([d_band_low, d_low, d_high, d_avg, d_band_high], ignore_index=True)

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})

plt.style.use("dark_background")
sns.relplot(x="t", y="val", kind="line", hue='sec', data=d_range, palette=["#ffffff", "#00ff00", "#ff0000", "#add8e6", "#ffffff"])

# manager = plt.get_current_fig_manager()
# manager.full_screen_toggle()
plt.show()

