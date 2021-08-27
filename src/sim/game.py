base = 100.00
amount = 0

prices = [10.00, 11.10, 12.00, 12.10, 12.20, 13.00, 12.00, 11.00, \
          10.00, 11.10, 12.00, 12.10, 12.20, 13.00, 12.00, 11.00, \
          10.00, 11.10, 12.00, 12.10, 12.20, 13.00, 12.00, 11.00, \
          10.00, 11.10, 12.00, 12.10, 12.20, 13.00, 12.00, 11.00]

for n in prices:
    print("Current money: " + str(base) + ", " + str(amount) + " shares")
    print("Input: ", end="")
    f = input()
    if f == "b":
        if base - n < 0:
            print("Not enough money.")
            continue
        amount += 1
        base -= n
    elif f == "s":
        if amount > 0:
            amount -= 1
            base += n
    else:
        pass
    print("Prev Price: " + str(n))
