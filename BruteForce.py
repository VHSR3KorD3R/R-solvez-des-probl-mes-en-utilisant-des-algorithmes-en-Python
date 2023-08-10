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
    dp = [[-1 for x in range(capacity + 1)] for y in range(len(profits))]
    return knapsack_recursive(dp, profits, weights, capacity, 0)


def knapsack_recursive(dp, profits, weights, capacity, currentIndex):
    # base case checks
    if capacity <= 0 or currentIndex >= len(profits):
        return 0

    # if we have already solved a similar problem, return the result from memory
    if dp[currentIndex][capacity] != -1:
        return dp[currentIndex][capacity]

    # recursive call after choosing the element at the currentIndex
    # if the weight of the element at currentIndex exceeds the capacity, we
    # shouldn't process this
    profit1 = 0
    choices1 = []
    if weights[currentIndex] <= capacity:
        profit1, choices1 = knapsack_recursive(
            dp, profits, weights, capacity - weights[currentIndex], currentIndex + 1)
        profit1 = profits[currentIndex] + profit1
        choices1.append(currentIndex + 1)

    # recursive call after excluding the element at the currentIndex
    profit2, choices2 = knapsack_recursive(
        dp, profits, weights, capacity, currentIndex + 1)

    if profit1 > profit2:
        return dp[currentIndex][capacity], choices1
    else:
        return dp[currentIndex][capacity], choices2
    # dp[currentIndex][capacity] = max(profit1, profit2)


def main():
    # améliorer l'affichage
    data = pd.read_csv('actions.csv')
    percentage = pd.to_numeric(data["Bénéfice (après 2 ans)"].str.replace('%', ''))
    price = pd.to_numeric(data["Coût par action (en euros)"])
    profit = (percentage * price) / 100

    #start = time.time()
    #solution, choices = solve(profit, price, 500)
    #end = time.time()

    #print(choices)
    #print(solution)
    #execTime = end - start
    #print("exec time:" + str(execTime))

    start = time.time()
    print(solve_knapsack(profit, price, 500))
    end = time.time()
    execTime = end - start
    print("exec time:" + str(execTime))

main()
