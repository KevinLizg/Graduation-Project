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
        var += (random_list[i] - mean)**2

    variance = var/(number_values-1)
    if format == 'string':
        problem = "Variance of the data: " + \
                  str(random_list)
        solution = f"The variance is {round(variance, 2)}"
        return problem, solution
    elif format == 'latex':
        return "Latex unavailable"
    else:
        return random_list, variance


data_summary = Generator("Variance", 125,
                         gen_func,
                         ["number_values=15", "minval=5", "maxval=50"])
