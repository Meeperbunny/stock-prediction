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

d_range = pd.concat([d_low, d_high, d_avg], ignore_index=True)
print(d_range)

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})

plt.style.use("dark_background")
sns.relplot(x="t", y="val", kind="line", hue='sec', data=d_range, palette=["#00ff00", "#ff0000", "#add8e6"])

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()

