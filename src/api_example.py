import finnhub
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
import os

# Setup client
api_key_local = os.environ.get('FINN_API_KEY')
finnhub_client = finnhub.Client(api_key=api_key_local)

def plot_stock(target_name, day_range, interval='D', smooth_val=1):
    upperTime = datetime.datetime.now()
    subtractor = datetime.timedelta(days=day_range)
    lowerTime = upperTime - subtractor
    upperUnix = int(time.mktime(upperTime.timetuple()))
    lowerUnix = int(time.mktime(lowerTime.timetuple()))

    # Stock candles
    res = finnhub_client.stock_candles(target_name, interval, lowerUnix, upperUnix)

    avg = np.array(res['h']) + np.array(res['l'])
    x = np.arange(1, len(avg) + 1)

    smoothedVals = []
    rollingSum = 0
    for i, n in enumerate(avg):
        rollingSum += avg[i]
        if i - smooth_val >= 0:
            rollingSum -= avg[i - smooth_val]
        smoothedVals.append(rollingSum / min(smooth_val, i + 1))
    smoothAvg = np.array(smoothedVals)

    plt.title(target_name + " Price (" + str(day_range) + ") Days")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.plot(x, smoothAvg, color ="green")
    plt.show()

plot_stock("AAPL", 60, interval='D')