import sys
sys.path.append('../')
money = 0
cnt = 0
data = []

def init_game(val):
    money = val
    data = []


def process(data_tick, money, curr):
    data_tick = data_tick.values.tolist()[0]
    highval = data_tick[1]
    lowval = data_tick[2]
    val = (highval + lowval) / 2
    data.append(val)
    ret_amnt = int(money / val) #
    return "B", ret_amnt #
    if len(data) > 1:
        if data[-2] > val:
            ret_amnt = int(money / val)
            return "B", ret_amnt
        else:
            return "S", curr
    else:
        return "N", 0