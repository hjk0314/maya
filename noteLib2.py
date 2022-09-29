import collections
import pathlib
import fileinput
import glob
import filecmp


# pathlib
def pathlib_Test():
    '''pathlib은 경로에 대한 여러 객체를 제공'''
    path0 = 'C:/users/jkhong/Desktop'
    path1 = pathlib.Path.home()/'Desktop'
    path2 = pathlib.Path('C:/users/jkhong/Desktop')
    print(path0)
    print(path1)
    print(path2)
    files = path2.glob('*.*')
    for i in files:
        # i: 'C:\users\jkhong\Desktop\desktop.ini'
        new = i.parent # 'C:\users\jkhong\Desktop'
        # new: 'C:\users\jkhong\Desktop\newDir\desktop.ini'
        new = i.parent.joinpath('newDir', i.name)
        print(new)
        '''replace는 shutil.move와 같음.'''
        # i.replace(new)
    
    # suffix는 .을 포함한 파일 확장자를 뜻함.
    # pathlib.Path.cwd().iterdir() 이런식으로도 사용
    ext = collections.Counter([i.suffix for i in path2.iterdir()])
    print(ext)


# fileinput.input
def fileinput_Test():
    '''fileinput은 여러개의 파일을 한꺼번에 처리할 때 사용하는 모듈이다.'''
    # 한글이 포함된 txt인 경우 cp949에러가 발생할 수 있다.
    path1 = glob.glob('C:/users/jkhong/Desktop/*.txt')
    with fileinput.input(path1) as txt:
        for line in txt:
            print(line)


# filecmp
def filecmp_Test():
    A = r"C:\Users\jkhong\Desktop\git\maya"
    B = r"C:\Users\jkhong\Desktop\git\mmp"
    result = filecmp.dircmp(A, B)
    print(result.left_only) # A에는 있는데, B에는 없는 파일 출력.
    print(result.right_only) # B에는 있는데, A에는 없는 파일 출력.
    print(result.diff_files) # A와 B에 모두 있으나, 파일이 서로 다름.
    result.report() # 위의 내용을 한꺼번에 볼 수 있다.


# pathlib_Test()
# fileinput_Test()
# filecmp_Test()


# 79 char line ================================================================
# 72 docstring or comments line ========================================


