import json, sys, numpy as np

# File to open and read json file into an object

def get_data(file_name):
    infile = open(file_name, 'r')
    data = json.load(infile)
    avg = (np.array(data['h']) + np.array(data['l'])) / 2
    return avg
