
def solve(profits, weights, capacity):
    return brute_force_recursive(profits, weights, capacity, 0)


def brute_force_recursive(profits, weights, capacity, current_index):
    if capacity <= 0 or current_index >= len(profits):
        return 0, []

    profit1 = 0
    choices1 = []
    if weights[current_index] <= capacity:
        profit, choices1 = brute_force_recursive(
            profits, weights, capacity - weights[current_index], current_index + 1)
        profit1 = profits[current_index] + profit
        choices1.append(current_index + 1)

    profit2, choices2 = brute_force_recursive(profits, weights, capacity, current_index + 1)

    if profit1 > profit2:
        return profit1, choices1
    else:
        return profit2, choices2
