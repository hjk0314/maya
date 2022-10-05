import collections
import pathlib
import fileinput
import glob
import filecmp
import tempfile
import fnmatch
import linecache
import pickle
import shelve


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


# tempfile: 임시 파일을 만드는 모듈
def tempfile_Test():
    _tempFile = tempfile.TemporaryFile(mode='w+')
    for i in range(10):
        _tempFile.write(str(i))
        _tempFile.write('\n')
    # seek(0)을 수행하여 파일을 처음부터 읽을 수 있도록 한다.
    # close()가 실행되거나, 프로세스가 종료되면 임시 파일은 삭제된다.
    _tempFile.seek(0)
    _tempFile.close()


# glob: 패턴(유닉스 셸이 사용하는 규칙)으로 파일을 검색하는 모듈
def glob_Test():
    for fileName in glob.glob("**/*.txt", recursive=True):
        print(fileName)


# fnmatch: 특정 패턴과 일치하는 파일을 검색하는 모듈
# 파일명은 a로 시작한다.
# 확장자는 .py이다.
# 확장자를 제외한 파일명의 길이는 5이다.
# 파일명의 마지막 5번째 문자는 숫자이다.
# "a???[0-9].py"
def fnmatch_Test():
    for i in pathlib.Path(".").rglob("*.py"):
        if fnmatch.fnmatch(i, "a???[0-9].py"):
            print(i)


# linecache
# 파일에서 원하는 줄의 값을 읽을 때, 캐시를 사용하여 내부적으로 최적화.
def linecache_Test():
    '''checkcache, clearcache, getline과 getlines 등이 있다.'''
    num = 1
    linecache.getline('fileName.txt', num)


# pickle: 자료형을 변환 없이 그대로 파일로 저장
def pickle_Test():
    data = {}
    data[1] = {"name": "HONGJINKI", "age": 45, "tall": "171cm"}
    with open(r"C:\Users\hjk03\Desktop\data.p", "wb") as pic:
        pickle.dump(data, pic)
    with open(r"C:\Users\hjk03\Desktop\data.p", "rb") as pic:
        temp = pickle.load(pic)
        print(temp)


# shelve: 딕셔너리를 파일로 저장할 때 사용하는 모듈
# shelve는 딕셔너리만을 처리하지만, pickle은 모든 객체를 다룬다. 
class shelve_Test():
    def __init__(self):
        self.main()


    # 바탕화면에 .dat파일을 만든다.
    def save(self, key, value):
        with shelve.open(r"C:\Users\hjk03\Desktop\data.dat") as shlv:
            shlv[key] = value

    # 저장된 .dat파일에서 key값으로 value값을 불러온다.
    def get(self, key):
        with shelve.open(r"C:\Users\hjk03\Desktop\data.dat") as shlv:
            return shlv[key]


    def main(self):
        self.save("number", [1, 2, 3, 4, 5])
        print(self.get("number"))


# pathlib_Test()
# fileinput_Test()
# filecmp_Test()
# tempfile_Test()
# glob_Test()
# fnmatch_Test()
# linecache_Test()
# pickle_Test()
# shelve_Test()


# 79 char line ================================================================
# 72 docstring or comments line ========================================


