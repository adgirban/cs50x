# TODO
from cs50 import get_float

def main():
    cents = get_cents()

    quarters = int(calculate_quarters(cents))
    cents = cents - quarters * 25

    dimes = int(calculate_dimes(cents))
    cents = cents - dimes * 10

    nickels = int(calculate_nickels(cents))
    cents = cents - nickels * 5

    pennies = int(calculate_pennies(cents))
    cents = cents - pennies * 1

    coins = quarters + dimes + nickels + pennies

    print(coins)


def get_cents():
    while True:
        try:
            n = get_float("Change owed: ");
            n = round(n * 100)
            if n > 0:
                break
        except ValueError:
            print()

    return n

def calculate_quarters(cents):
    return cents / 25

def calculate_dimes(cents):
    return cents / 10

def calculate_nickels(cents):
    return cents / 5

def calculate_pennies(cents):
    return cents / 1

main()



