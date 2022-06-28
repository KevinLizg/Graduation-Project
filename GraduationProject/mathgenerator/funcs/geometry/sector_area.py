from .__init__ import *


def gen_func(maxRadius=49, maxAngle=359, format='string'):
    r = random.randint(1, maxRadius)
    a = random.randint(1, maxAngle)
    secArea = float((a / 360) * math.pi * r * r)
    formatted_float = "{:.5f}".format(secArea)

    if format == 'string':
        ' Find the area of the sector, a sector radius is 29 and angle is 88.'
        problem = f"Find the area of a sector whose radius is {r} and angle is {a}."
        solution = f"Area of sector = {formatted_float}"
        return problem, solution
    elif format == 'latex':
        return "Latex unavailable"
    else:
        return r, a, formatted_float


sector_area = Generator("Area of a Sector", 75, gen_func,
                        ["maxRadius=49", "maxAngle=359"])
