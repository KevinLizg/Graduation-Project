# Referenced by lukew3/mathgenerator: https://github.com/lukew3/mathgenerator
from .funcs import *
from .__init__ import getGenList

genList = getGenList()


# || Non-generator Functions
def genById(id, *args, **kwargs):
    generator = genList[id][2]
    return (generator(*args, **kwargs))
