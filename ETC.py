"""
참고 : https://cuorej.tistory.com/entry/PYTHON-%EC%97%AC%EB%9F%AC-%EA%B2%BD%EB%A1%9C%EC%9D%98-%EB%AA%A8%EB%93%88-import-%ED%95%98%EA%B8%B0-1
-------------------------------------------------------
동일 경로 / (동일폴더)
-------------------------------------------------------
import 모듈 as 별칭

from 모듈 import 변수 as 별칭1
from 모듈 import 함수 as 별칭2
from 모듈 import 클래스 as 별칭3
from 모듈 import 변수 as 별칭4, 함수 as 별칭5, 클래스 as 별칭6

-------------------------------------------------------
하위 경로 / (하위폴더)
-------------------------------------------------------

하위 폴더 모듈 import 하기
from 폴더명 import 모듈

from 패키지.모듈 import 변수
from 패키지.모듈 import 함수
from 패키지.모듈 import 클래스
from 패키지.모듈 import 변수, 함수, 클래스

하위 폴더인 test 폴더 내에 있는 example.py 를 import 하려는 경우
from test import example

하위 폴더인 test 폴더 내에 있는 example.py 중 일부 함수만 import 하려는 경우
from test.example import example_function

from 패키지.모듈 import 변수 as 별칭1
from 패키지.모듈 import 변수 as 별칭2, 함수 as 별칭3, 클래스 as 별칭4

-------------------------------------------------------
다른 경로에 있는 모듈 import 하기
sys.path 리스트에 해당 경로를 추가해줘야한다. 이 리스트는 파이썬 인터프리터가 모듈을 찾을 때 검색하는 경로들을 담고있다.

import sys
sys.path.append("/path/to/other/directory")
import other_module
-------------------------------------------------------


"""
