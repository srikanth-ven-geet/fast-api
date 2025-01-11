import pytest
from ..caculations import add, subtract

def test_add():
    assert add(5,3) == 8


#with pytest decorator, pass the arguments and result inside double quotes and 
#second : add an array of tuple with the arguments and expected results
@pytest.mark.parametrize("num1, num2, result",[
    (2,3,5),
    (3,4,7),
    (1,2,3)
])
def test_par_add(num1: int, num2: int, result: int)->int:
    assert add(num1, num2) == result