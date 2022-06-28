from .__init__ import *


def gen_func(maxA=20, maxB=20, format='string'):
    a = random.randint(1, maxA)
    b = random.randint(1, maxB)
    c = random.randint(abs(b - a) + 1, abs(a + b) - 1)

    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c))**0.5

    if format == 'string':
        problem = "Triangle side lengths: " + \
            str(a) + " " + str(b) + " " + str(c) + ", what is its area?"
        solution = str(round(area, 2))
        return problem, solution
    elif format == 'latex':
        return "Latex unavailable"
    else:
        return a, b, c, area


area_of_triangle = Generator("Area of Triangle", 18, gen_func,
                             ["maxA=20", "maxB=20"])
