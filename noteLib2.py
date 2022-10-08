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
import sqlite3
import zlib
import gzip
import bz2
import lzma
import zipfile
import tarfile


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


# sqlite3
def sqlite3_Test():
    '''https://sqlitebrowser.org/dl/'''
    conn = sqlite3.connect('blog.db')
    # 쿼리문을 실행하려면 cursor()가 필요함
    curs = conn.cursor()
    # 테이블 만들기
    # 오라클은 text가 아닌 varchar 형식의 칼럼 타입을 사용
    createTable = '''CREATE TABLE blog 
    (id integer PRIMARY KEY, subject text, content text, date text)'''
    curs.execute(createTable)
    #
    # 데이터 입력하기
    # 방법1: 보안에 취약. SQL injection 공격
    insertValue = '''INSERT INTO blog VALUES 
    (1, "My First Blog.", "This is a First Content.", "20221008")'''
    curs.execute(insertValue)
    # 방법2: 보안에 취약. 사용자가 악의적인 쿼리를 던질 수도 있음
    _id = 2
    subject = 'My Second Blog.'
    content = 'Second content.'
    date = '20221009'
    insertValue = '''INSERT INTO blog VALUES 
    (%d, "%s", "%s", "%s")''' % (_id, subject, content, date)
    curs.execute(insertValue)
    # 방법3: 물음표 스타일. 보안에 그나마 괜찮음.
    _id = 3
    subject = 'My Third Blog.'
    content = 'Third content.'
    date = '20221010'
    insertValue = '''INSERT INTO blog VALUES 
    (?, ?, ?, ?)''', (_id, subject, content, date)
    curs.execute(insertValue)
    # 방법4: 딕셔너리 사용. 보안에 그나마 괜찮음.
    dic = {
        "id": 4, 
        "subject": "My Fourth Blog.", 
        "content": "Fourth content.", 
        "date": "20221011"
    }
    insertValue = '''INSERT INTO blog VALUES 
    (:id, :subject, :content, :date)''', dic
    curs.execute(insertValue)
    #
    # 데이터 조회하기
    curs.execute('SELECT * FROM blog')
    # fetchall()은 한 번 수행하면 끝이다. 다시 수행하면 빈 리스트 출력.
    all = curs.fetchall()
    print(all)
    #
    # 데이터 수정
    curs.execute("UPDATE blog SET subject='Original Blog.' WHERE id=1")
    # fetchone()은 튜플 형태로 반환
    curs.execute("SELECT * FROM blog WHERE id=1")
    one = curs.fetchone()
    print(one)
    #
    # 데이터 삭제: WHERE문을 생략하면 테이블의 모든 데이터 삭제. 주의 요망.
    curs.execute("DELETE FROM blog WHERE id=5")
    #
    # 커밋은 결정 서명과 같은 역할
    # 커밋하지 않고 종료하면 입력했던 데이터는 모두 사라짐.
    conn.commit()
    #
    # 롤백: 커밋되기 전의 데이터 변경 사항을 취소.
    # 이미 커밋된 데이터에는 소용 없음.
    conn.rollback()
    #
    # close()는 자동으로 commit()을 자동으로 수행하지 않음. 주의 요망.
    conn.close()


# sqlite3 데코레이터
# commit()과 close()를 반복 수행한다면 데코레이터를 만들어 사용.
def with_cursor(original_func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('blog.db')
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        result = original_func(curs, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper


# zlib: 문자열을 압축하고 해제할 수 있다.
def zlib_Test():
    data = "Life is too short, You need python." * 10000
    compress_data = zlib.compress(data.encode(encoding='utf-8'))
    print(len(compress_data))
    org_data = zlib.decompress(compress_data).decode(encoding='utf-8')
    print(len(org_data))


# gzip: 파일을 압축할 수 있다. 내부적으로 zlib를 사용.
def gzip_Test():
    data = "Life is too short, You need python.\n" * 10000
    with gzip.open('C:/Users/jkhong/Desktop/data.txt.gz', 'wb') as File:
        File.write(data.encode('utf-8'))
    with gzip.open('C:/Users/jkhong/Desktop/data.txt.gz', 'rb') as File:
        read_data = File.read().decode('utf-8')
    print(len(read_data))


# bz2: 문자열을 압축할 수 있다. 스레드 환경에서 안전함.
def bz2_Test():
    data = "Life is too short, You need python." * 10000
    compress_data = bz2.compress(data.encode(encoding='utf-8'))
    print(len(compress_data))
    org_data = bz2.decompress(compress_data).decode(encoding='utf-8')
    print(len(org_data))
    # 파일도 압축, 해제 할 수 있다.
    data = "Life is too short, You need python.\n" * 10000
    with bz2.open('C:/Users/jkhong/Desktop/data.txt.bz2', 'wb') as File:
        File.write(data.encode('utf-8'))
    with bz2.open('C:/Users/jkhong/Desktop/data.txt.bz2', 'rb') as File:
        read_data = File.read().decode('utf-8')
    print(len(read_data))


# lzma: 문자열을 압축할 수 있다. 스레드 환경에서 안전하지 않음.
def lzma_Test():
    data = "Life is too short, You need python." * 10000
    compress_data = lzma.compress(data.encode(encoding='utf-8'))
    print(len(compress_data))
    org_data = lzma.decompress(compress_data).decode(encoding='utf-8')
    print(len(org_data))
    # 파일도 압축, 해제 할 수 있다.
    data = "Life is too short, You need python.\n" * 10000
    with lzma.open('C:/Users/jkhong/Desktop/data.txt.xz', 'wb') as File:
        File.write(data.encode('utf-8'))
    with lzma.open('C:/Users/jkhong/Desktop/data.txt.xz', 'rb') as File:
        read_data = File.read().decode('utf-8')
    print(len(read_data))


# zipfile: 여러개의 파일을 zip형식으로 합치거나 해제할 수 있다.
def zipfile_Test():
    dir = 'C:/Users/hjk03/Desktop'
    # 파일 모두 압축
    with zipfile.ZipFile(f'{dir}/myText.zip', 'w') as myzip:
        myzip.write(f'{dir}/a.txt')
        myzip.write(f'{dir}/b.txt')
        myzip.write(f'{dir}/c.txt')
    # 파일 모두 압축 해제
    with zipfile.ZipFile(f'{dir}/myText.zip') as myzip:
        myzip.extractall()
    # 파일 중 하나만 압축 해제 가능
    with zipfile.ZipFile(f'{dir}/myText.zip') as myzip:
        myzip.extract(f'{dir}/a.txt')


# tarfile: 여러개의 파일을 tar형식으로 합치거나 해제할 수 있다.
def tarfile_Test():
    dir = 'C:/Users/jkhong/Desktop'
    # 파일 모두 압축
    with tarfile.open(f'{dir}/myText.tar', 'w') as mytar:
        mytar.add(f'{dir}/a.txt')
        mytar.add(f'{dir}/b.txt')
        mytar.add(f'{dir}/c.txt')
    # 파일 모두 압축 해제
    with tarfile.open(f'{dir}/myText.tar') as mytar:
        mytar.extractall()
    # 파일 중 하나만 압축 해제 가능
    with tarfile.open(f'{dir}/myText.tar') as mytar:
        mytar.extract(f'{dir}/a.txt')
    # 압축 방법을 지정
    with tarfile.open(f'{dir}/myText.tar.gz', 'w:gz') as mytar:
        mytar.add(f'{dir}/a.txt')
        mytar.add(f'{dir}/b.txt')
        mytar.add(f'{dir}/c.txt')
    # 파일 모두 압축 해제
    with tarfile.open(f'{dir}/myText.tar.gz') as mytar:
        mytar.extractall()


# pathlib_Test()
# fileinput_Test()
# filecmp_Test()
# tempfile_Test()
# glob_Test()
# fnmatch_Test()
# linecache_Test()
# pickle_Test()
# shelve_Test()
# zlib_Test()
# gzip_Test()
# bz2_Test()
# lzma_Test()
# zipfile_Test()
# tarfile_Test()


# 79 char line ================================================================
# 72 docstring or comments line ========================================


