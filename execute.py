import time
import pandas as pd
import optimized as op
import bruteforce as bf


def read_first_dataset():
    data = pd.read_csv('actions.csv')
    percentage = pd.to_numeric(data["Bénéfice (après 2 ans)"].str.replace('%', ''))
    price = pd.to_numeric(data["Coût par action (en euros)"])
    profit = (percentage * price) / 100
    return profit, price


def read_dataset(dataset):
    data = pd.read_csv(dataset)
    prices = []
    profits = []
    names = []
    for index, row in data.iterrows():
        if float(row["price"]) > 0:
            names.append(row["name"])
            current_price = int(float(row["price"]) * 100)
            prices.append(current_price)
            profit = (float(row["profit"]) * float(row["price"])) / 100
            profits.append(profit)

    return prices, profits, names


def main():
    profit, price = read_first_dataset()

    start = time.time()
    solution, choices = bf.solve(profit, price, 500)
    end = time.time()

    print("-------------20 STOCKS-----------------------")
    print("-------------BRUTEFORCE SOLUTION-------------")
    print("list of stocks selected:")
    print(choices)
    print(f"total price: {solution}")
    exec_time = end - start
    print("exec time:" + str(exec_time))

    print("-------------OPTIMIZED SOLUTION-------------")
    start = time.time()
    max_value, selected_items = op.knapsack(price, profit, 500)
    end = time.time()
    print("list of stocks selected:")
    print(selected_items)
    print(f"total price: {max_value}")
    exec_time = end - start
    print("exec time knapsack:" + str(exec_time))

    prices, profits, names = read_dataset('dataset1_Python+P7.csv')
    op.execute_optimized(prices, profits, names, 'dataset1_Python+P7.csv')

    prices, profits, names = read_dataset('dataset1_Python+P7.csv')
    op.execute_optimized(prices, profits, names, 'dataset1_Python+P7.csv')


main()
