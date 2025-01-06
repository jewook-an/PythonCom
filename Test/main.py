#1. python Test/main.py (C:\arch95\PythonCom)
#2. python main.py (C:\arch95\PythonCom\Test)
from PythonCom.common.NumpyCm import NumpyClass

# from ..common.NumpyCm import NumpyClass
# >> python -m PythonCom.Test.main # 호출방법 상위경로만 가능(Test 폴더내 사용 불가) : python -m PythonCom.Test.main

numpy_utils = NumpyClass()

print(numpy_utils.create_array([1, 2, 3, 4, 5]))

"""
예시 (TEST 완료)
1. 프로젝트 구조가 다음과 같다고 가정
/project_root
    /PythonCom
        /common
            NumpyCm.py
        /Test
            main.py

2. main.py에서 NumpyCm을 가져오려면
    - from PythonCom.common.NumpyCm import NumpyClass

3. project_root 디렉토리에서 다음과 같이 실행 (c:\arch95)
    - C:\arch95>python -m PythonCom.Test.main

이렇게 하면 Python이 패키지 구조를 인식하고, 상대 경로 문제를 피할 수 있음.
2-1. from common.NumpyCm import NumpyClass
3-1. C:\arch95\PythonCom>python -m Test.main
"""