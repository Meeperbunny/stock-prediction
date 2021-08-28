import sys, os
from reader.reader import get_data
from pred.pred import process

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

for i, n in enumerate(prices):
    if i == 0:
        continue

    # GET PRED USING LAST INPUT
    pred_input = process(prices[i - 1])

    if pred_input == "B":
        if base - n < 0:
            # Not enough money
            pass
        else:
            amount += 1
            base -= n
    elif pred_input == "S":
        if amount > 0:
            amount -= 1
            base += n
    log.append(get_total(base, amount, prices[i]))

print("Final Results:\n\tMoney: " + str(base) + "\n\tShares: " + str(amount) + "\n\tTotal: " + str(log[-1]))

print("Algorithm made: " + str(format(log[-1] / starting,".8f")))
