import numpy as np, time, datetime, os, sys, json
from reader.reader import get_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## SETTINGS ##

rectangles = True
highlow = False
openclose = False
bollbands = True

rolling_count = 30
boll_range = 2
width = 0.5

##############

if len(sys.argv) != 2:
    print("----------------------------")
    print("Invalid number of arguments.")
    print("py display_data.py <DATA_FILE>")
    exit()

data_file = sys.argv[1]
data = get_data(data_file)

# Change time val to respect missing days
for n in range(len(data['t'])):
    data['t'][n] = n

d = pd.DataFrame(data=data)
d_low = d.filter(['l','t'], axis=1)
d_high = d.filter(['h','t'], axis=1)
d_avg = d.filter(['l', 'h', 'c', 't'], axis=1)
d_open = d.filter(['o','t'], axis=1)
d_close = d.filter(['c','t'], axis=1)

d_low['sec'] = d_low.apply(lambda x: 'low', axis=1)
d_high['sec'] = d_high.apply(lambda x: 'high', axis=1)
d_avg['sec'] = d_avg.apply(lambda x: 'price', axis=1)
d_open['sec'] = d_avg.apply(lambda x: 'opening', axis=1)
d_close['sec'] = d_avg.apply(lambda x: 'closing', axis=1)


d_low = d_low.rename(columns={'l': 'val'})
d_high = d_high.rename(columns={'h': 'val'})
d_open = d_open.rename(columns={'o': 'val'})
d_close = d_close.rename(columns={'c': 'val'})
d_avg['val'] = d_avg.apply(lambda x: (x['l'] + x['h'] + x['c']) / 3, axis=1)

# Bands
d_band_high = d_avg.copy()
d_band_low = d_avg.copy()
d_band_high['sec'] = d_avg.apply(lambda x: 'boll_high', axis=1)
d_band_low['sec'] = d_avg.apply(lambda x: 'boll_low', axis=1)
std_dev_arr = []

for i, n in enumerate(d_band_high['val']):
    rel = np.array([])
    for q in range(i - 10, i + 1):
        if q >= 0:
            rel = np.append(rel, d_band_high['val'][q])
    
    mean = np.sum(rel) / len(rel)
    std_dev = np.sqrt(np.sum(np.square(rel - mean) / len(rel)))
    std_dev_arr.append(std_dev)


# Apply to dataframes

d_band_high['std_dev'] = pd.Series(std_dev_arr, index=d_band_high.index)
d_band_low['std_dev'] = pd.Series(std_dev_arr, index=d_band_low.index)

d_band_high['val'] = d_band_high.apply(lambda x: x['val'] + x['std_dev'] * boll_range, axis=1)
d_band_low['val'] = d_band_low.apply(lambda x: x['val'] - x['std_dev'] * boll_range, axis=1)

d_range = d_avg

# Colors
base_pal = ["#00FFFF"]

if bollbands:
    d_range = pd.concat([d_band_low, d_avg, d_band_high], ignore_index=True)
    base_pal.insert(0, "#ffffff")
    base_pal.append("#ffffff")

if highlow:
    d_range = pd.concat([d_high, d_low, d_range], ignore_index=True)
    base_pal.insert(0, "#ff0000")
    base_pal.insert(0, "#00ff00")

if openclose:
    d_range = pd.concat([d_open, d_close, d_range], ignore_index=True)
    base_pal.insert(0, "#ea00ff")
    base_pal.insert(0, "#fff300")

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})

plt.style.use("dark_background")

sns.relplot(x="t", y="val", kind="line", hue='sec', data=d_range, palette=base_pal)


if rectangles:
    for i in range(len(d_open['val'])):
        open_price = d_open['val'][i]
        close_price = d_close['val'][i]
        high_val = d_high['val'][i]
        low_val = d_low['val'][i]

        timestamp = d_open['t'][i]
        color = "#ff0000"
        if open_price < close_price:
            color = "#00ff00"

        # Draw rectangle
        plt.plot([timestamp + width / 2, timestamp - width / 2], [open_price, open_price], color=color)
        plt.plot([timestamp + width / 2, timestamp - width / 2], [close_price, close_price], color=color)

        plt.plot([timestamp + width / 2, timestamp + width / 2], [open_price, close_price], color=color)
        plt.plot([timestamp - width / 2, timestamp - width / 2], [open_price, close_price], color=color)

        # Draw centerline
        plt.plot([timestamp, timestamp], [high_val, low_val], color=color)



manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()

