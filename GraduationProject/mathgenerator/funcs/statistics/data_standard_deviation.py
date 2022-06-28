from .__init__ import *


def gen_func(number_values=15, minval=5, maxval=50, format='string'):
    random_list = []

    for i in range(number_values):
        n = random.randint(minval, maxval)
        random_list.append(n)

    a = sum(random_list)
    mean = a / number_values

    var = 0
    for i in range(number_values):
        var += (random_list[i] - mean) ** 2

    variance = var / (number_values - 1)
    standardDeviation = variance**0.5
    if format == 'string':
        problem = "Standard Deviation of the data: " + \
                str(random_list)
        solution = f"The Standard Deviation is {round(standardDeviation,2)}"
        return problem, solution
    elif format == 'latex':
        return "Latex unavailable"
    else:
        return random_list, standardDeviation


data_summary = Generator("Standard Deviation", 124,
                         gen_func,
                         ["number_values=15", "minval=5", "maxval=50"])
