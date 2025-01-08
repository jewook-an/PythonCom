"""
# 1. conftest.py
#--------------------------------------------------------------------
C:\arch95\PythonCom>pytest Test/PytestTest.py
# 정상
    - from ..common.calculator import Calculator
    - from PythonCom.common.calculator import Calculator
# 에러
    - from common.calculator import Calculator
    - from common import Calculator (__init__.py 내 from ... 입력)
#--------------------------------------------------------------------
import pytest

from ..common.calculator import Calculator

@pytest.fixture
def calculator():
    calculator = Calculator()
    return calculator

"""

"""
# 2. test_calculator.py
import pytest

from common import Calculator

def test_add(calculator):
    #calculator = Calculator()
    assert calculator.add(1, 2) == 3
    assert calculator.add(2, 2) == 4

def test_sub(calculator):
    #calculator = Calculator()
    assert calculator.sub(5, 1) == 4
    assert calculator.sub(3, 2) == 1

def test_mul(calculator):
    #calculator = Calculator()
    assert calculator.mul(2, 2) == 4
    assert calculator.mul(5, 6) == 30

def test_div(calculator):
    #calculator = Calculator()
    assert calculator.div(8, 2) == 4
    assert calculator.div(9, 3) == 3
"""

"""
3. test_calculator_id.py
import pytest

add_test_data = [
    pytest.param(1, 2, 3, id="1 add 2 is 3"),
    pytest.param(2, 2, 4, id="2 add 2 is 4"),
    pytest.param(1, 2, 4, marks=pytest.mark.xfail, id="1 add 2 is not 4"),
    pytest.param(2, 2, 6, marks=pytest.mark.xfail, id="2 add 2 is not 6"),
]

@pytest.mark.parametrize("a, b, result", add_test_data)
def test_add(calculator, a, b, result):
    assert calculator.add(a, b) == result
"""

"""
4. test_calculator_fixture_v1.py
import pytest

from ..common.calculator import Calculator

@pytest.fixture
def calculator():
    calculator = Calculator()
    return calculator

def test_add(calculator):
    assert calculator.add(1, 2) == 3
    assert calculator.add(2, 2) == 4

def test_sub(calculator):
    assert calculator.sub(5, 1) == 4
    assert calculator.sub(3, 2) == 1

def test_mul(calculator):
    assert calculator.mul(2, 2) == 4
    assert calculator.mul(5, 6) == 30

def test_div(calculator):
    assert calculator.div(8, 2) == 4
    assert calculator.div(9, 3) == 3

"""

"""
5. test_calculator_param_v1.py
"""
import pytest
from ..common.calculator import Calculator

# 주석시 > xfailed / 해제시 xpassed
# @pytest.fixture
# def calculator():
#     calculator = Calculator()
#     return calculator

@pytest.mark.parametrize(
    "a, b, expected",
    [pytest.param(1, 2, 3, marks=pytest.mark.xfail),
     pytest.param(2, 2, 4, marks=pytest.mark.xfail)]
)
def test_add_fail_xfail(calculator, a, b, expected):
    assert calculator.add(a, b) == expected

"""
6. test_calculator_param_v2.py
import pytest

@pytest.mark.parametrize(
    "a, b, result",
    [(1, 2, 3),
     (2, 2, 4),
     pytest.param(1, 2, 4, marks=pytest.mark.xfail),
     pytest.param(2, 2, 6, marks=pytest.mark.xfail)]
)
def test_add(calculator, a, b, result):
    assert calculator.add(a, b) == result
"""

"""
7. test_calculator_param_v3.py
import pytest

add_test_data = [
    (1, 2, 3),
    (2, 2, 4),
    pytest.param(1, 2, 4, marks=pytest.mark.xfail),
    pytest.param(2, 2, 6, marks=pytest.mark.xfail),
]

@pytest.mark.parametrize("a, b, result", add_test_data)
def test_add(calculator, a, b, result):
    assert calculator.add(a, b) == result
"""

"""
8. test_calculator_parametrize.py
import pytest

@pytest.mark.parametrize(
    "a, b, result",
    [(1, 2, 3),
     (2, 2, 4)]
)
def test_add(calculator, a, b, result):
    assert calculator.add(a, b) == result

@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 2, 4),
     (2, 2, 6)]
)
def test_add_fail(calculator, a, b, expected):
    assert calculator.add(a, b) != expected
"""

"""
9. test_calculator_xfail_v1.py
import pytest

@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 2, 4),
     (2, 2, 6)]
)
def test_add_fail_parametrize(calculator, a, b, expected):
    assert calculator.add(a, b) != expected

@pytest.mark.xfail(reason="wrong result")
@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 2, 4),
     (2, 2, 6),
     (3, 4, 7)]
)
def test_add_fail_xfail(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
"""

"""
10. test_skip
import pytest

@pytest.mark.skip(reason="no way of currently testing this")
def test_skip_v1():
    assert 1 == 1

def test_skip_v2():
    if True:
        pytest.skip(reason="no way of currently testing this")
    assert 1 == 1
"""

"""
12. test_skipif

import pytest
import sys

@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python 3.7 or higher")
def test_skipif_v1():
    assert 1 == 1

# 조건에 따른 SKIP 진행
try:
    import numpy as np  # Numpy Import 여부에 따른 Skip
except ImportError:
    pass

@pytest.mark.skipif('numpy' not in sys.modules, reason="requires the Numpy library")
def test_skipif_v2():
    assert 1 == 1
"""