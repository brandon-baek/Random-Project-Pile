def qpm(population: int, round_value=0):
    """
    Uses the Queue Position Method by Brandon Baek

    Generates a list of probabilities for a given population size, where the probabilities
    are determined by assigning increasing point values to each subsequent item.

    :param population: Amount of items
    :return: A list of normalized probabilities where the sum of all probabilities equals 1.

    Explanation:
        The function initializes an empty list called points. For each item in the population,
        it increments the value of each existing point by 1 and then appends a new point with
        the value of 1 to the list. This means that items that are added earlier in the process
        accumulate higher values over time. The final list of points is then normalized to create
        a list of probabilities.

    Example:
        qpm(population=5) would generate a points list that looks like this:
        - After 1st iteration: [1]
        - After 2nd iteration: [2, 1]
        - After 3rd iteration: [3, 2, 1]
        - After 4th iteration: [4, 3, 2, 1]
        - After 5th iteration: [5, 4, 3, 2, 1]

        These points are then converted into probabilities by dividing each point by the sum of all points.
        For this example, the final probabilities would be [5/15, 4/15, 3/15, 2/15, 1/15], where 15 is the
        sum of all points (5 + 4 + 3 + 2 + 1).
    """
    points = []
    for _ in range(population):
        points = [i + 1 for i in points]
        points.append(1)
    probs = [i / sum(points) for i in points]

    if round_value:
        probs = [round(i, round_value) for i in probs]

    return probs


def ldm(population: int, constant=0.8, round_value=0):
    """
    Uses the Linear Decay Method by Seonho Kim

    Generates a list of probabilities for a given population size, with probabilities
    decreasing exponentially based on the specified constant.

    :param population: Amount of items
    :param constant: The decay factor for the probabilities. This value determines how
                     quickly the probabilities decrease. A constant less than 1 will
                     cause an exponential decay, meaning that the value and thus the
                     probability of each subsequent item will be lower than the previous one.
                     This results in items at the start of the queue having significantly
                     higher probabilities compared to those at the end. The closer the
                     constant is to 1, the more gradual the decrease; the smaller the
                     constant, the steeper the decrease.
    :return: A list of normalized probabilities where the sum of all probabilities equals 1.

    Example:
        ldm(population=5, constant=0.99) would generate probabilities that decrease
        slightly for each subsequent item, with the first item having the highest probability
        and the last item having the lowest. If constant is set to a lower value, the difference
        between the first and last probabilities will be more pronounced.
    """
    current_value = 100
    pre_probs = []
    for _ in range(population):
        pre_probs.append(current_value * constant)
        current_value *= constant
    probs = [i / sum(pre_probs) for i in pre_probs]

    if round_value:
        probs = [round(i, round_value) for i in probs]

    return probs


def f_prob_list(prob_list, round_place=2):
    """
    Formats a list of probabilities as percentages, rounded to a specified number of decimal places.

    :param prob_list: A list of probabilities (floats) where each value is between 0 and 1.
    :param round_place: The number of decimal places to round each percentage to. Default is 2.
    :return: A list of formatted strings, where each probability is represented as a percentage.

    Explanation:
        This function takes a list of probabilities and converts each probability to a percentage
        format. Each probability is multiplied by 100 to convert it from a fraction to a percentage.
        The resulting percentage is then rounded to the specified number of decimal places and
        formatted as a string with a '%' sign.

    Example:
        f_prob_list([0.1234, 0.5678, 0.91011], round_place=2) would return:
        ['12.34%', '56.78%', '91.01%']
    """
    return [f'{round(i * 100, round_place)}%' for i in prob_list]


def optimal_ldm_constant(population, place_value=2):
    increment = float('0.' + '0' * (place_value - 1) + '1')
    constant_guess = increment
    while True:
        probs = ldm(population, constant_guess, place_value)
        print(probs)
        print(increment)
        print(constant_guess)
        if 0.0 in probs:
            constant_guess += increment
        else:
            break
    return constant_guess
