import numpy as np

# Predict function handles all logic given the data

prev_data = []

def predict(cp, hp, lp, op):
    prev_data.append([cp, hp, lp, op])

    # Calc bands
    past_range = 10
    std_count = 2

    tp_arr = np.array([])
    for n in prev_data[1 - past_range:]:
        tp = (n[0] + n[1] + n[2]) / 3
        tp_arr = np.append(tp_arr, tp)
    
    std_dev = np.std(tp_arr)
    last_val = tp_arr[-1]

    upper_band_val = last_val + std_count * std_dev
    lower_band_val = last_val - std_count * std_dev

    # If cross bands, ret val
    low_crosses = (lp < lower_band_val)
    high_crosses = (hp > upper_band_val)

    if low_crosses and high_crosses:
        return 'O'
    elif low_crosses:
        return 'B'
    elif high_crosses:
        return 'S'
    return 'O'

# Helper

def process(data_tick):
    data_tick = data_tick.values.tolist()[0]
    return predict(data_tick[0], data_tick[1], data_tick[2], data_tick[3])