#1. python Test/main.py (C:\arch95\PythonCom)
#2. python main.py (C:\arch95\PythonCom\Test)
from PythonCom.common.NumpyCm import NumpyClass

# from ..common.NumpyCm import NumpyClass
# >> python -m PythonCom.Test.main # 호출방법 상위경로만 가능(Test 폴더내 사용 불가) : python -m PythonCom.Test.main

numpy_utils = NumpyClass()

print(numpy_utils.create_array([1, 2, 3, 4, 5]))
