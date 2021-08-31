import sys, os
from reader.reader import get_data
from pred import process
import pandas as pd

def get_total(money, shares, share_price):
    return money + shares * share_price

starting = curr_money = 10000.00
curr_shares = 0
log = [curr_money]

if len(sys.argv) != 2:
    print("----------------------------")
    print("Invalid number of arguments.")
    print("py game.py <FILE_NAME>")
    exit()

# Log data
logfile = open('game_log.txt', 'w')

# Get file data
file_name = sys.argv[1]
prices = get_data(file_name)
prices = pd.DataFrame.from_dict(prices)

for i in range(1, len(prices['c'])):
    # Get prediction using last price
    pred_input = process(prices[i - 1:i])
    curr_price = (prices['c'][i] + prices['h'][i] + prices['l'][i]) / 3

    # If "O" string, do nothing
    if pred_input == "O":
        continue

    # Get current max shares that can be bought
    max_buy = int(curr_money / curr_price)

    # Log current price if buying / selling
    log.append(get_total(curr_money, curr_shares, (prices['h'][i] + prices['l'][i]) / 2))
    log_str = str(i) + " " + pred_input + " " + str(max_buy if pred_input == "B" else curr_shares) + " " + " ".join([str(n) for n in prices[i:i + 1].values.tolist()[0][0:4]])
    logfile.write(log_str + '\n')

    # Change money val to match pred
    if pred_input == "B":
        # Buying
        curr_money -= max_buy * curr_price
        curr_shares += max_buy
        
    elif pred_input == "S":
        # Selling
        curr_money += curr_shares * curr_price
        curr_shares -= curr_shares

# Print results
print("Final Results:\n\tMoney: " + str(curr_money) + "\n\tShares: " + str(curr_shares) + "\n\tTotal: " + str(log[-1]))
print("Algorithm made: ---- " + str(format(log[-1] / starting,".8f")))
start_price = (prices['h'][0] + prices['l'][0]) / 2
end_price = (prices['h'][len(prices) - 1] + prices['l'][len(prices) - 1]) / 2
print("curr_money is: ----------- " + str(format(end_price / start_price,".8f")))
