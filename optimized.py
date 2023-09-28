import time


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


def execute_optimized(prices, profits, names, dataset):
    start = time.time()
    max_value, selected_items = knapsack(prices, profits, 500 * 100)
    # max_value, selected_items = solve(prices, profits, 500)
    end = time.time()
    # print(max_value, selected_items)
    exec_time = end - start
    print("exec time of " + dataset + ": " + str(exec_time))
    print(f"-------------{dataset}-----------------------")
    print("-------------OPTIMIZED SOLUTION-------------")
    total = 0
    print("list of stocks selected:")
    for i in selected_items:
        print(names[i - 1])
        total += prices[i - 1]
    total /= 100
    performance = round((max_value / total) * 100, 2)
    print("total price: " + str(total))
    print("gain: " + str(max_value))
    print("performance: " + str(performance) + "%")