from .__init__ import *


def gen_func(maxAngle=89, format='string'):
    angle1 = random.randint(1, maxAngle)
    angle2 = random.randint(1, maxAngle)
    angle3 = 'The third angle is: '+str(180 - (angle1 + angle2))

    if format == 'string':
        problem = f"Triangle angles are {angle1} and {angle2}"
        return problem, angle3
    elif format == 'latex':
        return "Latex unavailable"
    else:
        return angle1, angle2, angle3


third_angle_of_triangle = Generator("Third Angle of Triangle", 22,
                                    gen_func, ["maxAngle=89"])
