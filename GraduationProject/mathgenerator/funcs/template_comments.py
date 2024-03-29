from .__init__ import *


def gen_func(format='string'):
    # your generator code goes here

    if format == 'string':
        # code that generates problem, solution strings goes here
        return problem, solution
    elif format == 'latex':
        # code that generates latex representation of problem, and solution goes here
        # if you can't do this, leave the return 'Latex unavailable'
        # return latex_problem, latex_solution
        return 'Latex unavailable'
    else:
        # Return necessary variables here
        # Any variables that go into the problem and solution string without formatting
        return a, b


# generator_name should be the same as the file name
# replace id with number generated by running nextId.py inside of the scripts folder
# last argument of Generator should be a list of the kwargs used in your gen_func().
generator_name = Generator("<Title>", id, gen_func,
                           ["<kwarg1>"])
# Delete all comments before submitting a pr
