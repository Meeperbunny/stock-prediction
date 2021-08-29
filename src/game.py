import sys, os
from reader.reader import get_data
from pred import process, init_game
import pandas as pd

def get_total(money, shares, share_price):
    return money + shares * share_price

starting = base = 10000.00
amount = 0
log = [base]

if len(sys.argv) != 2:
    print("----------------------------")
    print("Invalid number of arguments.")
    print("py game.py <FILE_NAME>")
    exit()

file_name = sys.argv[1]
prices = get_data(file_name)
prices = pd.DataFrame.from_dict(prices)

init_game(starting)
for i in range(len(prices['c'])):
    if i == 0:
        continue
    curr_price = (prices['h'][i] + prices['l'][i]) / 2
    # GET PRED USING LAST INPUT
    pred_input, amnt = process(prices[i:i + 1], base, amount)
    if pred_input == "B":
        if base - curr_price * amnt < 0:
            # Not enough money
            pass
        else:
            amount += amnt
            base -= curr_price * amnt
    elif pred_input == "S":
        if amount > 0:
            amount -= amnt
            base += curr_price * amnt
    log.append(get_total(base, amount, (prices['h'][i] + prices['l'][i]) / 2))

print("Final Results:\n\tMoney: " + str(base) + "\n\tShares: " + str(amount) + "\n\tTotal: " + str(log[-1]))

print("Algorithm made: ---- " + str(format(log[-1] / starting,".8f")))

start_price = (prices['h'][0] + prices['l'][0]) / 2
end_price = (prices['h'][len(prices) - 1] + prices['l'][len(prices) - 1]) / 2
print(start_price)
print(end_price)
print("Base is: ----------- " + str(format(end_price / start_price,".8f")))
