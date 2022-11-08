import textwrap
import re
import struct
import datetime
import calendar
import collections
import heapq
import pprint
import bisect
import enum
import math
import decimal
import fractions
import random
import statistics
import itertools
import functools
import time
import operator
import pathlib
import fileinput
import filecmp
import tempfile
import glob
import fnmatch
import linecache
import pickle
import copyreg
import shelve
import sqlite3
import zlib
import gzip
import bz2
import lzma
import zipfile
import tarfile
import csv
import configparser
import hashlib
import hmac
import secrets
import io
import argparse
import logging
import getpass
import curses
import platform
import ctypes
import threading
import multiprocessing
import concurrent
import subprocess
import sched
import asyncio
import socket
import ssl
import select
import selectors
import signal
import json
import base64
import binascii
import quopri
import uu
import html
import xml.etree.ElementTree
import webbrowser
import cgi
import cgitb
import wsgiref
import urllib
import http.client
import ftplib
import poplib
import imaplib
import nntplib
import smtplib
import telnetlib
import uuid
import socketserver
import http.server
import xmlrpc
import imghdr
import turtle
import cmd
import shlex
import tkinter
import unittest
import doctest
import timeit
import pdb
import dataclasses
import abc
import atexit
import traceback
import typing


# textwrap.shorten: 문자열을 원하는 길이에 맞게 줄여 표시(...)
# textwrap.wrap: 긴 문자열을 원하는 길이로 줄 바꿈.
# textwrap.fill: wrap과 같은 기능이지만 조금 더 간편하다.
""" longStr = '''We are not now that strength which in old days 
Moved earth and heaven; that which we are, we are; 
One equal temper of heroic hearts, 
Made weak by time and fate, but strong in will 
To strive, to seek, to find, and not to yield. - Alfred Lord Tennyson
'''
textwrap.shorten(longStr, width=15, placeholder='...')
textwrap.wrap(longStr, width=30)
textwrap.fill(longStr, width=45)
 """


# re: 정규표현식. 다양한 표현 방법이 있음
""" data = '780314-1234567'
temp = re.compile('(\d{6})[-](\d{7})')
print(temp.sub('\g<1>-*******', data))
 """


# struct: C언어로 만든 구조체 이진 데이터를 처리할 때 활요하는 모듈.
""" C구조체로 만들어진 파일을 읽거나, 네트워크로 전달되는 C구조체 이진 데이터를
파이썬에서 처리할 때 사용.
 """


# datetime.date: 년, 월, 일로 날짜를 표현.
# datetime.timedelta: 두 날짜의 차이를 계산할 때 사용.
""" today = datetime.date.today()
year = today.year
mon = today.month
day = today.day
HJK = datetime.date(1978, 3, 14)
SYR = datetime.date(1991, 4, 12)
HSE = datetime.date(2020, 3, 30)
WED = datetime.date(2018, 10, 28)
THO = datetime.timedelta(days=1000)
 """


# calendar.isleap: 인수로 입력한 연도가 윤년인지를 확인할 때 사용.
""" curr = datetime.date.today()
year = curr.year
if calendar.isleap(year):
    print('It\'s a leap year.')
 """


# collections.deque: 양방향 자료형. "데크"라 읽는다.
# 스택(stack)처럼 써도 되고, 큐(queue)처럼 써도 된다.
# [1, 2, 3, 4, 5]이 다이얼을 오른쪽으로 2칸 돌려 [4, 5, 1, 2, 3]으로 바꾼다.
""" a = [1, 2, 3, 4, 5]
q = collections.deque(a)
q.rotate(2) # 음수 가능
result = list(q)
print(result)
 """


# collections.nametuple: 튜플은 인덱스를 통해서만 데이터에 접근할 수 있지만, 
# 네임드튜플은 인덱스뿐만 아니라 키(key)로도 데이터에 접근할 수 있다.


# collections.Counter: 리스트나 문자열과 같은 자료형의 요소 중 
# 같은 요소가 몇 개인지 확인할 때 사용하는 클래스이다.


# collections.defaultdict는 값에 초깃값을 지정하여 딕셔너리를 생성한다.


# heapq: 순위가 가장 높은 자료를 가장 먼저 꺼내는 "우선순위 큐" 모듈이다. 
# 리스트를 사용하여 직접 구현하기 어렵지 않지만, 
# 이런 작업에 최적화된 heapq를 사용하자.


# pprint: 데이터를 보기 좋게 출력.


# bisect: 이진 탐색 알고리즘을 구현한 모듈로, 
# bisect.bisect() 함수는 정렬된 리스트에 값을 삽입할 때 
# 정렬을 유지할 수 있는 인덱스를 반환한다.
""" result = []
scoreList = [33, 99, 77, 70, 89, 90, 100]
gradeList = [60, 70, 80, 90]
for i in scoreList:
    # bisect.bisect_left()
    idx = bisect.bisect(gradeList, i)
    # 77은 70과 80 사이에 있으므로 인덱스 값 2를 반환한다.
    print(f'idx: {idx}')
    grade = 'FDCBA'[idx]
    result.append(grade)
bisect.insort(gradeList, 85) # insort()
print(gradeList)
print(result)
 """


# enum: 서로 관련이 있는 여러 개의 상수 집합을 정의할 때 사용.
""" class Week(enum.IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
 """


# graphlib.TopologicalSorter: 그래프 위상 정렬에 사용하는 클래스.(파이썬 3.9)


# math.gcd: 최대공약수
# math.lcm: 최소공배수
# gcd(): 3개 이상의 최대공약수를 구하는 것은 파이썬 ver 3.9 에서 가능
# lcm(): 3개 이상의 최소공배수를 구하는 것은 파이썬 ver 3.9 에서 가능
""" math.gcd(60, 100)
math.isclose(0.1 * 3, 0.3)
 """


# decimal: 정확한 소숫점 자리를 표현할 때 사용.
# 파이썬은 float 연산이 가끔씩 미세한 오차가 발생한다.
# decimal.Decimal('0.1') * 3.0 -> error: 곱하는 수는 정수여야 함.
""" decimal.Decimal('0.1') * 3
decimal.Decimal('1.2') + decimal.Decimal('0.1')
float(sum)
 """


# fractions: 유리수를 계산할 때 사용하는 모듈.
""" A = fractions.Fraction(1, 5)
A = fractions.Fraction('1/5')
B = fractions.Fraction(2, 5)
print(A)
print(B)
print(A.numerator)
print(A.denominator)
print(A + B)
print(float(A + B))
 """


# random: 난수 생성.
""" numList = [1, 2, 3, 4, 5]
a = random.randint(1, 45)
b = random.shuffle(numList)
c = random.choice(numList)
 """


# statistics: 평균값과 중앙값을 구할 때 사용.
""" scoreList = [78, 93, 99, 95, 51, 71, 52, 43, 81, 78]
A = statistics.mean(scoreList)
B = statistics.median(scoreList)
 """


# itertools.cycle(반복 객체): 반복 가능한 객체를 무한히 반복하도록 함.
# 이터레이터란 next() 함수 호출시 계속 그 다음 값을 반환. 
""" nameList = ['kim', 'lee', 'hong']
cyl = itertools.cycle(nameList)
print(next(cyl), next(cyl), next(cyl), next(cyl))
 """


# itertools.accumulate: 리스트 안에 요소들의 합계를 구한다.
""" saleList = [
    1161, 1814, 1270, 2256, 1413, 1842, 
    2221, 2207, 2450, 2823, 2540, 2134, 
    ]
result = itertools.accumulate(saleList)
result = list(result)
result = itertools.accumulate(saleList, max)
result = list(result)
 """


# itertools.groupby: 키 값으로 분류하고 그 결과를 반환.


# itertools.zip_longest(*iterables, fillvalue=None): 
# 같은 개수의 자료형을 묶는 파이썬 내장 함수인 zip()과 똑같이 동작한다. 
# 하지만 itertools.zip_longest는 객체의 길이가 다르다면 
# 긴 것을 기준으로 빠진 값은 fillvalue에 설정한 값으로 채운다.
""" student = ['kim', 'lee', 'hong', 'han', 'choi']
rewards = ['candy', 'jelly', 'chocolate']
result = zip(student, rewards)
result = list(result)
print(result)
result = itertools.zip_longest(student, rewards, fillvalue='caramel')
result = list(result)
print(result)
 """


# itertools.permutatins(iterable, r=None): 객체 중에서 r개를 선택하는 순열.
""" numList = ['1', '2', '3']
result = itertools.permutations(numList, 2)
result = list(result)
print(result)
 """


# itertools.combinations(iterable, r): 객체 중에서 r개를 선택하는 조합.
# 로또 = len(list(itertools.combinations(range(1, 46), 6)))
""" numList = ['1', '2', '3']
result = itertools.combinations(numList, 2)
result = list(result)
print(result)
 """


# functools.cmp_to_key: sorted()와 같은 정렬 함수의 key 매개변수에 
# 함수를 전달할 때 사용하는 함수이다. 단 func() 한수는 두 개의 인수를 입력하여 
# 첫 번째 인수를 기준으로 그 둘을 비교하고 작으면 음수, 같으면 0, 
# 크면 양수를 반환하는 비교 함수여야 한다.



# functools.lru_cache: 함수의 반환 결과를 캐시하는 데코레이터이다. 
# 최초 요청 이후에는 캐시한 결과를 반환한다. 
# maxsize는 캐시할 수 있는 최대 개수를 의미하며, 
# 이를 초과할 때는 호출 빈도가 가장 작은 것부터 캐시에서 사라진다.
""" 사용법: @functools.lru_cache(maxsize=32) """


# functools.partial: 인수가 이미 채워진, 새 버전의 함수를 만들 때 사용.
# cal('add', 1, 2, 3) -> Use it like below.
""" def cal(typ: str, *args) -> float:
    if typ == 'add':
        result = 0
        for i in args:
            result += i
        return result
    elif typ == 'mul':
        result = 1
        for i in args:
            result *= i
        return result
    else:
        print('Unknow type.')


def usage():
    add = functools.partial(cal, 'add')
    mul = functools.partial(cal, 'mul')
    print(add(1, 2, 3))
    print(mul(4, 5, 6))
    print(add.func, add.args)
    print(mul.func, mul.args)
 """


# functools.reduce(function, iterable): function을 반복 가능한 객체에 
# 차례대로(왼쪽에서 오른쪽으로) 누적 적용하여 값을 줄이는 함수.
""" data = [1, 2, 3, 4, 5]
result = functools.reduce(lambda x, y: x + y, data)
# ((((1 + 2) + 3) + 4) + 5)
print(result)
 """


# functools.wraps(wrapped)는 래퍼 함수를 정의할 때 
# 함수의 이름이나 설명문 같은 속성을 유지하도록 하는 데코레이터이다.
""" def elapsed(original_func):
    # wraps is here.
    @functools.wraps(original_func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = original_func(*args, **kwargs)
        end = time.time()
        print(f'Running time: {end - start}sec')
        return result
    return wrapper


@elapsed
def add(num1, num2):
    '''Function that returns the sum.'''
    result = num1 + num2
    return result
 """


# operator.itemgetter: 주로 sorted와 같은 함수의 
# key 매개변수에 적용하여 다양한 기준으로 정렬할 수 있도록 하는 모듈.
""" students = [
    ('jane', 22, 'A'), 
    ('dave', 32, 'B'), 
    ('sally', 17, 'B'), 
]
result = sorted(students, key=operator.itemgetter(1))
print(result)
students = [
    {'name': 'jane', 'age': 22, 'grade': 'A'}, 
    {'name': 'dave', 'age': 32, 'grade': 'B'}, 
    {'name': 'sally', 'age': 17, 'grade': 'B'}, 
]
result = sorted(students, key=operator.itemgetter('age'))
# 클래스의 객체인 경우 attrgetter 사용
# result = sorted(students, key=operator.attrgetter('age'))
print(result)
 """


# pathlib: 파일 시스템 경로를 문자열이 아닌 객체로 취급한다.
""" path0 = 'C:/users/jkhong/Desktop'
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
    # replace는 shutil.move와 같음.
    # i.replace(new)
# suffix는 .을 포함한 파일 확장자를 뜻함.
# pathlib.Path.cwd().iterdir() 이런식으로도 사용
ext = collections.Counter([i.suffix for i in path2.iterdir()])
print(ext)
 """


# fileinput: 여러 개의 파일을 한꺼번에 처리.
# 한글이 포함된 txt인 경우 cp949에러가 발생할 수 있다.
""" path1 = glob.glob('C:/users/jkhong/Desktop/*.txt')
with fileinput.input(path1) as txt:
    for line in txt:
        print(line)
 """


# filecmp: 파일이나 디렉터리 두 곳을 비교
""" A = r"C:\Users\jkhong\Desktop\git\maya"
B = r"C:\Users\jkhong\Desktop\git\mmp"
result = filecmp.dircmp(A, B)
print(result.left_only) # A에는 있는데, B에는 없는 파일 출력.
print(result.right_only) # B에는 있는데, A에는 없는 파일 출력.
print(result.diff_files) # A와 B에 모두 있으나, 파일이 서로 다름.
result.report() # 위의 내용을 한꺼번에 볼 수 있다.
 """


# tempfile: 임시 파일을 만드는 모듈
""" _tempFile = tempfile.TemporaryFile(mode='w+')
for i in range(10):
    _tempFile.write(str(i))
    _tempFile.write('\n')
# seek(0)을 수행하여 파일을 처음부터 읽을 수 있도록 한다.
# close()가 실행되거나, 프로세스가 종료되면 임시 파일은 삭제된다.
_tempFile.seek(0)
_tempFile.close()
 """


# glob: 패턴(유닉스 셸이 사용하는 규칙)으로 파일을 검색하는 모듈
""" for fileName in glob.glob("**/*.txt", recursive=True):
    print(fileName)
 """


# fnmatch: 특정 패턴과 일치하는 파일을 검색하는 모듈
# 파일명은 a로 시작한다.
# 확장자는 .py이다.
# 확장자를 제외한 파일명의 길이는 5이다.
# 파일명의 마지막 5번째 문자는 숫자이다.
# "a???[0-9].py"
""" for i in pathlib.Path(".").rglob("*.py"):
    if fnmatch.fnmatch(i, "a???[0-9].py"):
        print(i)
 """


# linecache: 파일에서 원하는 줄의 값을 읽을 때, 
# 캐시를 사용하여 내부적으로 최적화.
# checkcache, clearcache, getline과 getlines 등이 있다.
""" num = 1
linecache.getline('fileName.txt', num)
 """


# pickle: 자료형을 변환 없이 그대로 파일로 저장
""" data = {}
data[1] = {"name": "HONGJINKI", "age": 45, "tall": "171cm"}
with open(r"C:\Users\hjk03\Desktop\data.p", "wb") as pic:
    pickle.dump(data, pic)
with open(r"C:\Users\hjk03\Desktop\data.p", "rb") as pic:
    temp = pickle.load(pic)
    print(temp)
 """


# copyreg: pickle로 저장한 객체를 불러올 때 객체를 생성하는 함수.


# shelve: 딕셔너리를 파일로 저장할 때 사용하는 모듈
# shelve는 딕셔너리만을 처리하지만, pickle은 모든 객체를 다룬다. 
""" class shelve_Test():
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
 """


# sqlite3: SQLite 데이터베이스를 사용하는 데 필요한 인터페이스 모듈.
""" '''https://sqlitebrowser.org/dl/'''
conn = sqlite3.connect('blog.db')
# 쿼리문을 실행하려면 cursor()가 필요함
curs = conn.cursor()
# 테이블 만들기
# 오라클은 text가 아닌 varchar 형식의 칼럼 타입을 사용
createTable = '''CREATE TABLE blog 
(id integer PRIMARY KEY, subject text, content text, date text)'''
curs.execute(createTable)

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

# 데이터 조회하기
curs.execute('SELECT * FROM blog')
# fetchall()은 한 번 수행하면 끝이다. 다시 수행하면 빈 리스트 출력.
all = curs.fetchall()
print(all)

# 데이터 수정
curs.execute("UPDATE blog SET subject='Original Blog.' WHERE id=1")
# fetchone()은 튜플 형태로 반환
curs.execute("SELECT * FROM blog WHERE id=1")
one = curs.fetchone()
print(one)

# 데이터 삭제: WHERE문을 생략하면 테이블의 모든 데이터 삭제. 주의 요망.
curs.execute("DELETE FROM blog WHERE id=5")

# 커밋은 결정 서명과 같은 역할
# 커밋하지 않고 종료하면 입력했던 데이터는 모두 사라짐.
conn.commit()

# 롤백: 커밋되기 전의 데이터 변경 사항을 취소.
# 이미 커밋된 데이터에는 소용 없음.
conn.rollback()

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
 """


# zlib: 문자열을 압축하고 해제할 수 있다.
""" data = "Life is too short, You need python." * 10000
compress_data = zlib.compress(data.encode(encoding='utf-8'))
print(len(compress_data))
org_data = zlib.decompress(compress_data).decode(encoding='utf-8')
print(len(org_data))
 """


# gzip: 파일을 압축할 수 있다. 내부적으로 zlib를 사용.
""" data = "Life is too short, You need python.\n" * 10000
with gzip.open('C:/Users/jkhong/Desktop/data.txt.gz', 'wb') as File:
    File.write(data.encode('utf-8'))
with gzip.open('C:/Users/jkhong/Desktop/data.txt.gz', 'rb') as File:
    read_data = File.read().decode('utf-8')
print(len(read_data))
 """


# bz2: 문자열을 압축할 수 있다. 스레드 환경에서 안전함.
""" data = "Life is too short, You need python." * 10000
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
 """


# lzma: 문자열을 압축할 수 있다. 스레드 환경에서 안전하지 않음.
""" data = "Life is too short, You need python." * 10000
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
 """


# zipfile: 여러개의 파일을 zip형식으로 합치거나 해제할 수 있다.
""" dir = 'C:/Users/hjk03/Desktop'
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
 """


# tarfile: 여러개의 파일을 tar형식으로 합치거나 해제할 수 있다.
""" dir = 'C:/Users/jkhong/Desktop'
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
    mytar.extractall() """


# csv: CSV 파일을 읽고 쓸 때 사용.
# 엑셀 파일 안에 쉼표가 있을 경우 split(',') 이것 사용은 위험하다.
""" result = []
CSV_FILE = "C:/folder/file.csv"
CSV_NEW = "C:/folder/new.csv"
# 마이크로소프트 엑셀은 csv 파일을 기본적으로 euc-kr로 인코딩 한다.
with open(CSV_FILE, 'r', encoding='euc-kr') as File:
    # reader
    reader = csv.reader(File)
    for line in reader:
        average = sum(map(int, line[1].split(','))) / 2
        line.append(average)
        result.append(line)
# newline=''은 윈도우 시스템에서 줄 바꿈 문제를 방지하기 위함이다.
with open(CSV_NEW, 'w', newline='') as File:
    # writer
    writer = csv.writer(File)
    # writerows() 리스트를 한번에 처리해줌.
    writer.writerows(result)
 """


# configparser: ini 파일은 프로그램 정보를 저장하는 텍스트 문서로
# 섹션과 그 섹션에 해당하는 "키 = 값"으로 구성된다. 
# configparser는 이러한 형식의 ini 파일을 처리할 때 사용하는 모듈이다.
""" '''파일명: ftp.ini
[FTP1]
SERVER_IP = 111.23.56.78
PORT = 21
USERNAME = foo
PASSWORD = bar

[FTP2]
SERVER_IP = 111.23.56.79
PORT = 22221
USERNAME = foo
PASSWORD = bar
'''
config = configparser.ConfigParser()
config.read('C:/folder/ftp.ini')
ftp2_port = config['FTP2']['PORT']
print(ftp2_port) # 22221 출력
 """


# hashlib: MD5, SHA256 등의 알고리즘으로 문자열을 해싱한다.
# 해싱은 단방향 암호화 알고리즘이므로 원래의 문자열을 복구할 수는 없다.
""" m = hashlib.sha256()
m.update('Life is too short'.encode('utf-8'))
m.update(', you need python.'.encode('utf-8'))
# digest(): 바이트 문자열을 반환
byteStr = m.digest()
# hexdigest(): 바이트 문자열을 16진수로 반환
hexaStr = m.hexdigest()
print(byteStr)
print(hexaStr)
 """


# hmac: 메시지 변조를 확인할 수 있다. 단, 비밀키가 있어야 한다.
""" SECRET = 'password'
msg = 'This is a message.'
# 메시지 작성
with open('C:/folder/file.txt', 'w') as txt:
    txt.write(msg)
# 메시지 해싱: 원본 문자열을 알아볼 수 없도록 난해한 문자열로 바꿈.
with open('C:/folder/file_digest.txt', 'w') as txt:
    secretKey = SECRET.encode('utf-8')
    msg = msg.encode('utf-8')
    # hmac.new(비밀키, 메시지, 암호화 방식)
    i = hmac.new(secretKey, msg, hashlib.sha256)
    txt.write(i.hexdigest())
# 해싱된 메시지를 받고 읽어들임.
with open('C:/folder/file_digest.txt') as txt:
    msg_digest = txt.read()
# 원본과 비교
with open('C:/folder/file.txt') as txt:
    secretKey = SECRET.encode('utf-8')
    msg = txt.read()
    msg = msg.encode('utf-8')
    i = hmac.new(secretKey, msg, hashlib.sha256)
    if i.hexdigest() == msg_digest:
        print('The message has not been tampered with.')
 """


# secrets: 안전한 난수 발생
# 1바이트는 2개의 16진수 문자열로 반환되므로 (16)은 32자리 난수가 된다.
""" key = secrets.token_hex(16)
print(key)
 """


# io.StringIO: 문자열을 파일 객체처럼 다룰 수 있도록 하는 클래스이다.
""" class io_Test():
    def __init__(self):
        # csv 파일의 내용을 아래처럼 간단하게 문자열로 만든다.
        self.src = '20,40\n'
        self.src += '50,90\n'
        self.src += '77,22\n'
        self.main()


    # (파일 객체)가 인수인 함수는 상당히 많다.
    # 이러한 함수를 테스트할 때 직접 파일을 만들기보다 io를 사용하자.
    def execute(self, obj):
        result = []
        reader = csv.reader(obj)
        for line in reader:
            one = int(line[0])
            two = int(line[1])
            three = one + two
            line.append(three)
            result.append(line)
        return result


    def main(self):
        # txt라는 파일 객체를 execute함수에 직접 넣었다.
        with io.StringIO(self.src) as txt:
            result = self.execute(txt)
            print(result)
 """


# argparse: 파이썬 스크립트의 명령행 옵션을 파싱할 때 사용하는 모듈
""" python module.py -a 1 2 3 4 5
python module.py --add 1 2 3 4 5
 """


# logging: 로그를 파일로 출력할 때 사용하는 모듈
# getpass: 비밀번호를 입력할 때 화면에 노출하지 않도록 한다.
# curses: 터미널 그래픽 애플리케이션을 만들 때 사용.
# platform: 시스템 정보를 확인할 때 사용.
# ctypes: C로 작성한 라이브러리를 파이썬에서 사용.
# threading: 스레드를 이용하여 한 프로세스에서 2가지 이상의 일을 실행.
# multiprocessing: 멀티 프로세스를 활용하여, 2가지 이상의 일을 동시에 실행.
# concurrent.futures: 같은 규칙으로 threading과 multiprocessing을 더 쉽게 사용.


# subprocess: 시스템 명령을 수행.
""" with open(r"C:\Users\jkhong\Desktop\file.txt", 'wb') as txt:
    out = subprocess.run(['cmd', '/c', 'dir'], capture_output=True)
    txt.write(out.stdout)
 """


# sched: 지정된 시간에 원하는 이벤트를 실행하게 해주는 이벤트 스케줄러이다.
# asyncio: 단일 스레드 작업을 병렬로 처리.
# socket: TCP 서버/클라이언트 프로그램을 작성할 때 사용.
# ssl: socket 모듈로 작성한 서버/클라이언트에 공개키 암호화 방식을 적용.
# select: socket 프로그래밍에서 "I/O멀티플랙싱"을 가능하게 하는 모듈.


# selectors: select를 확장하여 "고수준I/O멀티플랙싱"을 가능하도록 한 모듈로, 
""" select 대신 사용하도록 권장하는 모듈이다. """


# signal: 특정 신호를 수신했을 때 사용자가 정의한 함수를 호출하도록 한다.


# json: "json데이터"를 쉽게 처리. pickle, shelve 등과 비슷한 일을 한다. 
""" 기본적으로 아스키 형태로 저장. 
딕셔너리, 리스트나 튜플 같은 자료형도 처리 가능.
 """


# base64: 바이너리 데이터를 문자열로 인코딩할 때 사용. 
""" 이때 인코딩한 문자열은 64개의 아스키 문자로 구성된다.(64진법) """


# binascii: 문자열을 16진수로, 변환할 16진수를 다시 문자열로 변환한다.


# quopri: quoted-printable 인코딩/디코딩을 할 때 사용하는 모듈.
# 영문과 숫자 등의 ASCII 7bit 문자는 그대로 두고 한글 등 8bit 문자만 인코딩.
""" quopri.decodestring('Python =EA=B3=B5=EB=B6=80').decode('utf-8') """


# uu: 바이너리를 텍스트로 변환하기 위한 인코딩 방법. 
# 1980년 메리 앤호튼이 개발. uu는 Unix-to-Unix를 뜻함. 
# 지금은 대부분 uuencode의 단점을 보완한 Base64와 같은 MIME 방식의 인코딩을 사용. 
# uu는 이러한 uuencode 인코딩을 위한 파이썬 모듈이다.(begin ~ end로 구성됨)
""" uu.encode('test.jpg', 'result.txt')
uu.decode('result.txt', 'test.jpg')
 """


# html: HTML문자를 이스케이프 처리할 때 사용.
""" "&lt;script&gt;Hello&lt;/script&gt;"
<script>Hello</script>
 """


# html.parser: HTML 문서를 파싱할 때 사용. 
""" 예를 들어 <strong></strong>태그의 문자열을 찾아서 출력. """


# xml.etree.ElementTree: XML 문서를 만들 때 사용.
# parse: XML 문서를 파싱하고 검색할 때도 사용.


# webbrowser: 파이썬 프로그램에서 시스템 브라우저를 호출할 때 사용.


# cgi: CGI 프로그램을 만드는 데 필요한 도구를 제공.


# cgitb: cgitb는 CGI 프로그램의 오류를 쉽게 파악하는 데 사용.


# wsgiref: wsgiref는 WSGI 프로그램을 만들 때 사용하는 모듈.
# 한마디로 웹 서버 응용 프로그램이다.
""" WSGI(Web Sever Gateway Interface)는 웹 서버 소프트웨어와 파이썬으로 
만든 웹 응용 프로그램 간의 표준 인터페이스이다. 쉽게 말해 
웹 서버가 클라이언트로부터 받은 요청을 파이썬 애플리케이션에 전달하여 실행하고, 
그 실행 결과를 돌려 받기 위한 약속이다. """


# urllib
# urllib은 URL을 읽고 분석할 때 사용하는 모듈.
# 웹 페이지를 저장할 수 있다.


# http.client
# http.client는 HTTP 프로토콜의 클라이언트 역할을 하는 모듈이다.
""" 웹 페이지를 저장하는 또 다른 방법이다. 하지만, 
http.client보다는 requests 모듈을 사용 하는 것이 좋다. """


# ftplib
# ftplib는 FTP 서버에 접속하여 파일을 내려받거나 올릴 때 사용하는 모듈.


# poplib
# poplib는 POP3 서버에 연결하여 받은 메일을 확인하는 데 사용하는 모듈.
""" POP3는 널리 사용하긴 했지만, 오래된 방식이다. 
메일 서버가 IMAP을 지원한다면 POP3 대신 IMAP을 사용하는 것이 좋다. """


# imaplib: 수신한 이메일을 IMAP4로 확인한다.
# imaplib은 IMAP4 서버에 연결하여 메일을 확인할 때 사용하는 모듈.


# nntplib: 최신 뉴스를 확인할 수 있다.
# nntplib는 뉴스 서버에 접속하여 뉴스 그룹의 글을 조회하거나 작성할 때 사용.


# smtplib: 이메일을 보낼 때 사용하는 모듈.
# 파일 첨부도 가능하다.


# telnetlib: 텔넷에 접속하여 작업 가능하다.
# 텔넷 서버에 접속하여 클라이언트 역할로 사용하는 모듈.


# uuid: 고유한 식별자
# 네트워크상에서 중복되지 않는 고유한 식별자인 UUID를 생성할 때 사용.
""" UUID(Universally Unique IDentifier)는 
네트워크상에서 고유성을 보장하는 ID를 만들기 위한 표준 규약이다. 
UUID는 다음과 같이 32개의 16진수로 구성되며 5개의 그룹으로 표시 되고 
각 그룹은 붙임표(-)로 구분한다. """
# 280a8a4d-a27f-4d01-b031-2a003cc4c039
""" 적어도 서기 3400년까지는 같은 UUID가 생성될 수 없다고 한다. 
이러한 이유로 UUID를 데이터베이스의 프라이버리 키로 종종 사용한다. """


# socketserver: 서버와 통신하는 게임을 만들 수 있다.
# 다양한 형태의 소켓 서버를 쉽게 구현하고자 할 때 사용하는 모듈.


# http.server: 테스트용 HTTP 서버를 만들 수 있다.
# 테스트 등의 용도로 사용할 간단한 HTTP 서버를 구현하고자 사용.


# xmlrpc
# xmlrpc는 HTTP를 통한 간단하고 이식성 높은 원격 프로시저 호출 방법이다.
""" 2대의 컴퓨터 A, B가 있다. A 컴퓨터는 인터넷에 연결되었지만, 
B 컴퓨터는 인터넷에 연결 되지 않았다고 한다. 하지만, 
2대의 컴퓨터는 내부 네트워크로 연결되어 있어서 
A 컴퓨터와 B 컴퓨터 간의 통신은 가능하다고 한다. 이때 A 컴퓨터를 이용하여 
B 컴퓨터의 위키독스 특정 페이지 내용을 얻어 올 수 있다. """


# imghdr: 어떤 유형의 이미지 파일인지를 판단할 수 있다.
""" >>> imghdr.what('C:/folder/file.png')
'png'
 """


# turtle: 터틀 그래픽으로 그림을 그린다.
""" turtle은 아이들에게 프로그래밍을 소개할 때 자주 사용하는 도구로, 
1967년 월리 푸르지그, 시모어 페이퍼트, 신시아 솔로몬이 개발한 
로고 프로그래밍 언어의 일부이다. """


# cmd: cmd는 사용자에게 익숙한 명령행 프로그램 작성을 돕는다.


# shlex: 문장 분석
# 인용이나 강조를 포함한 문장을 분석할 때 사용.
""" >>> shlex.split('this is "a test"', posix=False)
['this', 'is', '"a test"']
 """


# tkinter
# 파이썬에서 Tcl/Tk 툴킷을 사용하는 데 필요한 인터페이스 모듈.
# Tcl은 파이썬과 같은 스크립트 언어이고, Tk는 Tcl을 위한 GUI 툴킷이다.


# unittest: 작성한 코드를 단위 테스트할 때 사용.


# doctest
# 독스트링을(docstring)을 활용하여 예제를 간단하게 테스트하고자 사용.


# timeit
""" 함수의 실행 시간을 측정할 때 유용한 모듈.
>>> timeit.timeit("aFunction()", number=100, globals=globals())
>>> timeit.timeit("bFunction()", number=100, globals=globals())
 """


# pdb: 파이썬 코드를 디버깅할 때 사용하는 모듈.


""" import sys.argv
매개변수를 전달하여 실행.
파이썬 스크립트로 전달한 명령행 매개변수를 처리할 때 사용.
 """


# dataclasses: 객체를 출력하거나 비교.
# 데이터를 저장하는 용도의 데이터 클래스를 만들 때 사용하는 모듈.


# abc: 반드시 메서드를 구현하도록 함.
# abc는 추상 클래스를 정의할 때 사용.


# atexit: 프로그램 종료 시 특정 작업을 실행.
# atexit는 파이썬 프로그램을 종료할 때 특정 코드를 마지막으로 실행하고자 사용.


# traceback: 오류 위치와 그 원인을 알려준다.
# 발생한 오류를 추적하고자 할 때 사용.


# typing: 데이터 타입을 확인
# 다양한 타입 어노테이션을 위해 사용하는 모듈이다. 이 모듈은 3.5부터 사용 가능.


