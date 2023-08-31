import time
import pandas as pd


# temps de calcul de l'algo
def solve(profits, weights, capacity):
    return brute_force_recursive(profits, weights, capacity, 0)


def brute_force_recursive(profits, weights, capacity, currentIndex):
    if capacity <= 0 or currentIndex >= len(profits):
        return 0, []

    profit1 = 0
    choices1 = []
    if weights[currentIndex] <= capacity:
        profit, choices1 = brute_force_recursive(
            profits, weights, capacity - weights[currentIndex], currentIndex + 1)
        profit1 = profits[currentIndex] + profit
        choices1.append(currentIndex + 1)

    profit2, choices2 = brute_force_recursive(profits, weights, capacity, currentIndex + 1)

    if profit1 > profit2:
        return profit1, choices1
    else:
        return profit2, choices2
    # return max(profit1, profit2), choices1


def solve_knapsack(profits, weights, capacity):
    # create a two dimensional array for Memoization, each element is initialized to '-1'
    length = len(profits) + 1
    dp = [[-1 for x in range(capacity + 1)] for y in range(length)]
    results = knapsack_recursive(dp, profits, weights, capacity, 0, [])
    selected_items = []
    w = capacity
    n = len(profits)
    res = dp[n][capacity]
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
    return results


def knapsack_recursive(dp, profits, weights, capacity, currentIndex, choices):
    # base case checks
    if capacity <= 0 or currentIndex >= len(profits):
        return 0, []

    # if we have already solved a similar problem, return the result from memory
    if dp[currentIndex][capacity] != -1:
        return dp[currentIndex][capacity], []

    # recursive call after choosing the element at the currentIndex
    # if the weight of the element at currentIndex exceeds the capacity, we
    # shouldn't process this
    profit1 = 0
    choices1 = []
    if weights[currentIndex] <= capacity:
        profit1, choices1 = knapsack_recursive(
            dp, profits, weights, capacity - weights[currentIndex], currentIndex + 1, choices)
        profit1 += profits[currentIndex]

    # recursive call after excluding the element at the currentIndex
    profit2, choices2 = knapsack_recursive(
        dp, profits, weights, capacity, currentIndex + 1, choices)

    if profit1 > profit2:
        choices.append(currentIndex + 1)
        dp[currentIndex][capacity] = profit1
        return dp[currentIndex][capacity], choices
    else:
        dp[currentIndex][capacity] = profit2
        return dp[currentIndex][capacity], choices2
    # dp[currentIndex][capacity] = max(profit1, profit2)


def knapsack(weight, value, max_weight):
    n = len(weight)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            if weight[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight[i - 1]] + value[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i)
            w -= weight[i - 1]

    selected_items.reverse()
    return dp[n][max_weight], selected_items


def knapsack_recursive_with_items(price, profit, max_weight, n):
    if n == 0 or max_weight == 0:
        return 0, []

    weight = price[n - 1]
    value = profit[n - 1]

    if weight > max_weight:
        return knapsack_recursive_with_items(weight, value, max_weight, n - 1)

    # Consider two possibilities: including the current item or excluding it
    value_with_item, selected_items_with = knapsack_recursive_with_items(weight, value, max_weight - weight, n - 1)
    value_without_item, selected_items_without = knapsack_recursive_with_items(weight, value, max_weight, n - 1)

    if value_with_item + value > value_without_item:
        selected_items = selected_items_with + [n - 1]
        return value_with_item + value, selected_items
    else:
        return value_without_item, selected_items_without


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

    start = time.time()
    max_value, selected_items = knapsack(prices, profits, 500 * 100)
    # max_value, selected_items = solve(prices, profits, 500)
    end = time.time()
    #print(max_value, selected_items)
    exec_time = end - start
    print("exec time of " + dataset + ": " + str(exec_time))

    total = 0
    for i in selected_items:
        print(names[i - 1])
        total += prices[i - 1]
    total /= 100
    performance = round((max_value / total) * 100, 2)
    print("total price: " + str(total))
    print("gain: " + str(max_value))
    print("performance: " + str(performance) + "%")


def main():
    # améliorer l'affichage
    data = pd.read_csv('actions.csv')
    percentage = pd.to_numeric(data["Bénéfice (après 2 ans)"].str.replace('%', ''))
    price = pd.to_numeric(data["Coût par action (en euros)"])
    profit = (percentage * price) / 100

    start = time.time()
    solution, choices = solve(profit, price, 500)
    end = time.time()

    print(choices)
    print(solution)
    execTime = end - start
    print("exec time:" + str(execTime))

    # start = time.time()
    # print(solve_knapsack(profit, price, 500))
    # end = time.time()
    # execTime = end - start
    # print("exec time:" + str(execTime))

    start = time.time()
    max_value, selected_items = knapsack(price, profit, 500)
    end = time.time()
    print(max_value, selected_items)
    execTime = end - start
    print("exec time knapsack:" + str(execTime))

    # data = pd.read_csv('dataset1_Python+P7.csv')
    # prices = []
    # profits = []
    # names = []
    # for index, row in data.iterrows():
    #    if float(row["price"]) > 0:
    #        names.append(row["name"])
    #        current_price = int(float(row["price"]) * 100)
    #        prices.append(current_price)
    #        profit = (float(row["profit"]) * float(row["price"])) / 100
    #        profits.append(profit)

    # start = time.time()
    # max_value, selected_items = knapsack(prices, profits, 500*100)
    # end = time.time()
    # print(max_value, selected_items)
    # execTime = end - start
    # print("exec time dataset1:" + str(execTime))

    # total = 0
    # for i in selected_items:
    #    print(names[i-1])
    #    total += prices[i-1]

    # print(total/100)

    read_dataset('dataset1_Python+P7.csv')
    read_dataset('dataset2_Python+P7.csv')


main()
