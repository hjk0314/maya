from setuptools import setup
from Cython.Build import cythonize


""" 
1.  작성한 파이썬 파일을 .pyx으로 이름을 변경한다.
2.  터미널에서 
        python setup.py build_ext --inplace
3.  경로 문제로 .pyd 파일이 생성되지 않는다면, 
    __init__.py 파일을 지우거나 수정할 것.
4.  .pyd 파일은 파이썬 코드에서 import해서만 사용 가능
5. 사용 예
    - 직접적으로 터미널에서 "python test.cp37-win_amd64.pyd" 처럼 실행 불가
    - 터미널에서 python 입력
    - 파이썬 쉘에서 import test 하여 실행행
    - exit()
 """


setup(ext_modules = cythonize("test.pyx"))

