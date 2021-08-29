import sys
sys.path.append('../')
data = []

def process(val):
    data.append(val)
    return "B"
    if len(data) > 1:
        if data[-2] > val:
            return "B"
        else:
            return "S"
    else:
        return "N"