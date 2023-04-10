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
# import graphlib
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


def textwrap_sample():
    """ textwrap.shorten: 문자열을 원하는 길이에 맞게 줄여 표시(...)
    textwrap.wrap: 긴 문자열을 원하는 길이로 줄 바꿈.
    textwrap.fill: wrap과 같은 기능이지만 조금 더 간편하다.
      """
    longStr = '''We are not now that strength which in old days 
    Moved earth and heaven; that which we are, we are; 
    One equal temper of heroic hearts, 
    Made weak by time and fate, but strong in will 
    To strive, to seek, to find, and not to yield. - Alfred Lord Tennyson
    '''
    result1 = textwrap.shorten(longStr, width=15, placeholder='...')
    result2 = textwrap.wrap(longStr, width=30)
    result3 = textwrap.fill(longStr, width=45)
    print(f"result1 -> {result1}")
    print(f"result2 -> {result2}")
    print(f"result3 -> {result3}")


def re_sample():
    """ re: 정규표현식. 다양한 표현 방법이 있음 """
    # 주민등록번호 샘플
    data = '780314-1234567'
    temp = re.compile('(\d{6})[-](\d{7})')
    print(temp.sub('\g<1>-*******', data))
    # 마야에서 Deformed 글자 search
    attr = "pCylinderShape1Deformed.aiSubdivType"
    tmp = re.search('((.*)Deformed)(.*)', attr)
    org = tmp.group(1) # -> pCylinderShape1Deformed
    new = tmp.group(2) # -> pCylinderShape1
    mod = tmp.group(3) # -> .aiSubdivType
    print(f"tmp -> {tmp}")
    print(f"tmp -> {org}")
    print(f"tmp -> {new}")
    print(f"tmp -> {mod}")


def struct_sample():
    """ struct: C언어로 만든 구조체 이진 데이터를 처리할 때 활요하는 모듈. """
    originalDoc = struct.__doc__
    result = "C구조체로 만들어진 파일을 읽거나, "
    result += "네트워크로 전달되는 C구조체 이진 데이터를 "
    result += "파이썬에서 처리할 때 사용."
    print(originalDoc)
    print(result)


def datetime_sample():
    """ datetime.date: 년, 월, 일로 날짜를 표현.
    datetime.timedelta: 두 날짜의 차이를 계산할 때 사용.
     """
    today = datetime.date.today()
    year = today.year
    mon = today.month
    day = today.day
    HJK = datetime.date(1978, 3, 14)
    SYR = datetime.date(1991, 4, 12)
    HSE = datetime.date(2020, 3, 30)
    WEDDING_DAY = datetime.date(2018, 10, 28)
    THOUSAND_DAY = datetime.timedelta(days=1000)
    print(f"today -> {today}")
    print(f"year -> {year}")
    print(f"mon -> {mon}")
    print(f"day -> {day}")
    print(f"HJK -> {HJK}")
    print(f"SYR -> {SYR}")
    print(f"HSE -> {HSE}")
    print(f"WEDDING_DAY -> {WEDDING_DAY}")
    print(f"THOUSAND_DAY -> {THOUSAND_DAY}")


def calendar_sample():
    """ calendar.isleap: 인수로 입력한 연도가 윤년인지를 확인할 때 사용. """
    curr = datetime.date.today()
    year = curr.year
    if calendar.isleap(year):
        print('It\'s a leap year.')
    else:
        print('It\'s not a leap year.')
   

def deque_sample():
    """ collections.deque: 양방향 자료형. "데크"라 읽는다.
    스택(stack)처럼 써도 되고, 큐(queue)처럼 써도 된다.
    [1, 2, 3, 4, 5]이 다이얼을 오른쪽으로 2칸 돌려 [4, 5, 1, 2, 3]으로 바꾼다.
     """
    sampleList = [1, 2, 3, 4, 5]
    dequed = collections.deque(sampleList)
    dequed.rotate(2) # 음수 가능
    result = list(dequed)
    print(f"sampleList -> {sampleList}")
    print(f"dequedList -> {result}")
   

def nametuple_sample():
    """ collections.nametuple: 튜플은 인덱스를 통해서만 데이터에 접근할 수 있지만, 
    네임드튜플은 인덱스뿐만 아니라 키(key)로도 데이터에 접근할 수 있다.
    namedtuple 함수는 두 개의 인자를 받습니다. 
    첫 번째 인자는 생성될 클래스 이름입니다. 
    두 번째 인자는 공백으로 구분된 필드명의 문자열이나 문자열 리스트입니다.
     """
    # Point 클래스 생성
    Point = collections.namedtuple('Point', ['x', 'y'])
    # Point 클래스 객체 생성
    p = Point(1, 2)
    # 필드명으로 값에 접근
    print(p.x)  # 1
    print(p.y)  # 2
    # 인덱스로도 접근 가능
    print(p[0])  # 1
    print(p[1])  # 2


def counter_sample():
    """ collections.Counter: 리스트나 문자열등을 비교.
    리스트가 갖고 있는 요소들을 카운트해주는 함수인데, 
    순서는 고려하지 않고 비교를 한다.
    같은 요소가 몇 개인지 비교할 때 사용하는 클래스이다.
     """
    arr1 = [1, 2, 3]
    arr2 = [3, 2, 1]
    arr3 = [3, 2, 1, 0]
    if collections.Counter(arr1) == collections.Counter(arr2):
        print("arr1 == arr2")
    if collections.Counter(arr1) != collections.Counter(arr3):
        print("arr1 != arr3")
   

def defaultdict_sample():
    """ collections.defaultdict는 값에 초깃값을 지정하여 딕셔너리를 생성한다.
    아래 예제에서 d는 defaultdict 객체입니다. 
    int 타입의 디폴트 값으로 초기화되었습니다. 
    d['apple'] += 1과 같이 딕셔너리 값 추가를 할 때, 
    d가 int 타입 디폴트 값을 가진 defaultdict이기 때문에 
    d['apple']이 처음 등장하는 경우, 디폴트 값인 0이 할당된 뒤 1이 더해집니다. 
    따라서 print(d)를 호출하면 {'apple': 1, 'banana': 2, 'cherry': 3}와 같은 
    딕셔너리가 출력됩니다. 또한, 존재하지 않는 키인 'durian'을 참조할 경우, 
    자동으로 디폴트 값인 0이 할당되어 출력됩니다.
     """
    # defaultdict 생성
    d = collections.defaultdict(int)  # int 타입의 디폴트 값
    # 딕셔너리 값 추가
    d['apple'] += 1
    d['banana'] += 2
    d['cherry'] += 3
    # 딕셔너리 출력
    print(d)  # defaultdict(<class 'int'>, {'apple': 1, 'banana': 2, 'cherry': 3})
    # 존재하지 않는 키 참조
    print(d['durian'])  # 0 (int 타입의 디폴트 값이 할당됨)


def heapq_saple():
    """ heapq: 순위가 가장 높은 자료를 가장 먼저 꺼내는 "우선순위 큐" 모듈이다. 
    힙은 일종의 이진트리(binary tree) 자료구조로서, 
    각 노드의 값이 그 자식 노드의 값보다 작은 최소 힙(min-heap)과 
    각 노드의 값이 그 자식 노드의 값보다 큰 최대 힙(max-heap)으로 나눌 수 있습니다. 
    heapq 모듈은 최소 힙(min-heap)만을 다룹니다.
    이러한 과정을 리스트를 사용하여 직접 구현하기 어렵지 않지만, 
    이런 작업에 최적화된 heapq를 사용해보는 것도 나쁘지 않다.
     """
    # 리스트를 힙으로 변환
    lst = [5, 3, 1, 7, 4]
    heapq.heapify(lst)
    print(lst)  # [1, 3, 5, 7, 4]
    # 힙에 원소 추가
    heapq.heappush(lst, 2)
    print(lst)  # [1, 2, 5, 7, 4, 3]
    # 최소값 삭제 및 반환
    min_value = heapq.heappop(lst)
    print(min_value)  # 1
    print(lst)  # [2, 3, 5, 7, 4]
    # 원소 추가 및 최소값 삭제 및 반환
    min_value = heapq.heappushpop(lst, 6)
    print(min_value)  # 2
    print(lst)  # [3, 4, 5, 7, 6]


def pprint_sample():
    """ pprint: 데이터를 보기 좋게 출력하는 Pretty Printer(PPrint)를 제공합니다.
    이 함수는 다음과 같은 인자를 받습니다.
     - object: 출력하고자 하는 객체
     - stream: 출력할 스트림(stream)을 지정합니다. 기본값은 sys.stdout입니다.
     - indent: 들여쓰기(indentation)할 너비를 지정합니다. 기본값은 1입니다.
     - width: 출력할 줄의 최대 너비를 지정합니다. 기본값은 80입니다.
     - depth: 출력할 객체의 중첩 깊이를 제한합니다. 기본값은 None입니다.
     """
    data = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "phone_numbers": ["010-1234-5678", "02-9876-5432"],
        "address": {
            "city": "Seoul",
            "country": "South Korea"
        }
    }
    pprint.pprint(data)
    # 결과값: 
    """ {'address': {'city': 'Seoul', 'country': 'South Korea'},
    'age': 30,
    'email': 'johndoe@example.com',
    'name': 'John Doe',
    'phone_numbers': ['010-1234-5678', '02-9876-5432']}
     """


def bisect_sample():
    """ bisect는 이진 탐색 알고리즘을 구현한 모듈로, 
    bisect.bisect() 함수는 정렬된 리스트에 값을 삽입할 때 정렬을 유지할 수 있는 
    인덱스를 반환한다. bisect 라이브러리에서 가장 많이 사용되는 함수는 
    bisect_left()와 bisect_right()입니다. 
    이 함수들은 새로운 요소를 삽입할 위치를 찾아내는 함수로, 
    리스트가 정렬된 상태를 유지할 수 있도록 도와줍니다. 
    bisect_left() 함수는 새로운 요소가 삽입될 위치를 왼쪽부터 찾아냅니다. 
    반면 bisect_right() 함수는 오른쪽부터 찾아냅니다.
     """
    result = []
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


class Week(enum.IntEnum):
    """ enum: 서로 관련이 있는 여러 개의 상수 집합을 정의할 때 사용. """
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


def graphlib_sample():
    """ graphlib는 파이썬 3.9에서 추가된 그래프 처리를 위한 표준 라이브러리입니다. 
    이 라이브러리는 유향 그래프와 무향 그래프 모두를 다룰 수 있으며, 
    다양한 그래프 알고리즘을 제공합니다. 
    graphlib에서 가장 많이 사용되는 클래스는 Graph 클래스입니다. 
    이 클래스는 무향 그래프를 나타내는 클래스로, 
    그래프의 노드와 엣지를 추가, 제거, 수정하는 등의 작업을 수행할 수 있습니다. 
    Digraph 클래스는 유향 그래프를 다루는 클래스이며, 
    TopologicalSorter 클래스는 위상 정렬(topological sort)을 수행하는 클래스입니다. 
    이 외에도 다양한 그래프 알고리즘을 제공하므로, 
    그래프 처리를 위한 작업을 할 때 유용하게 사용할 수 있습니다.
    Graph 클래스의 객체를 생성하는 예제는 아래와 같지만 3.9서 사용 가능.
     """
    # g = graphlib.Graph()
    # g.add_node('A')
    # g.add_node('B')
    # g.add_edge('A', 'B')
    

def gcdLcm_sample():
    """ math.gcd: 최대공약수
    math.lcm: 최소공배수
    gcd(): 3개 이상의 최대공약수를 구하는 것은 파이썬 ver 3.9 에서 가능
    lcm(): 3개 이상의 최소공배수를 구하는 것은 파이썬 ver 3.9 에서 가능
     """
    math.gcd(60, 100)
    # math.lcm(60, 100)
    math.isclose(0.1 * 3, 0.3)


def decimal_sample():
    """ decimal: 정확한 소숫점 자리를 표현할 때 사용.
    파이썬은 float 연산이 가끔씩 미세한 오차가 발생한다.
    decimal.Decimal('0.1') * 3.0 -> error: 곱하는 수는 정수여야 함.
     """
    decimal.Decimal('0.1') * 3
    decimal.Decimal('1.2') + decimal.Decimal('0.1')
    

def fraction_sample():
    """ fractions: 유리수를 계산할 때 사용하는 모듈. """
    A = fractions.Fraction(1, 5)
    A = fractions.Fraction('1/5')
    B = fractions.Fraction(2, 5)
    print(A)
    print(B)
    print(A.numerator)
    print(A.denominator)
    print(A + B)
    print(float(A + B))
   

def random_sample():
    """ random: 난수 생성. """
    numList = [1, 2, 3, 4, 5]
    a = random.randint(1, 45)
    b = random.shuffle(numList)
    c = random.choice(numList)
    print(a)
    print(b)
    print(c)
   

def statistics_sample():
    """ statistics: 평균값과 중앙값을 구할 때 사용. """
    scoreList = [78, 93, 99, 95, 51, 71, 52, 43, 81, 78]
    A = statistics.mean(scoreList)
    B = statistics.median(scoreList)
    print(A, B)


def cycle_sample():
    """ itertools.cycle(반복 객체): 반복 가능한 객체를 무한히 반복하도록 함.
    이터레이터란 next() 함수 호출시 계속 그 다음 값을 반환.
     """
    nameList = ['kim', 'lee', 'hong']
    cyl = itertools.cycle(nameList)
    print(next(cyl), next(cyl), next(cyl), next(cyl))


def accumulate_sample():
    """ itertools.accumulate: 리스트 안에 요소들의 합계를 구한다. """
    saleList = [
        1161, 1814, 1270, 2256, 1413, 1842, 
        2221, 2207, 2450, 2823, 2540, 2134, 
        ]
    result = itertools.accumulate(saleList)
    result = list(result)
    result = itertools.accumulate(saleList, max)
    result = list(result)
   

def groupby_sample():
    """ itertools.groupby: 키 값으로 분류하고 그 결과를 반환.
    이 함수는 iterable 객체(리스트, 튜플 등)를 입력으로 받아, 
    연속된 그룹들을 묶어주는 역할을 합니다. 
    보통 groupby 함수는 sorted나 sorted의 key 인자와 함께 사용됩니다. 
    key 인자를 사용하면 groupby 함수가 그룹을 나눌 기준을 지정할 수 있습니다. 
    groupby 함수는 그룹을 구분하는 기준으로 key 함수의 반환값이 같은 원소들을 
    하나의 그룹으로 묶어줍니다.
    """
    # 문자열 리스트 정렬 후, 첫 번째 글자를 기준으로 그룹화
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
    words_sorted = sorted(words, key=lambda x: x[0])
    for key, group in itertools.groupby(words_sorted, key=lambda x: x[0]):
        print(key, list(group))
    """ 결과값: 
    >>> a ['apple']
    >>> b ['banana']
    >>> c ['cherry']
    >>> d ['date']
    >>> e ['elderberry']
    >>> f ['fig']
    >>> g ['grape']
     """


def zip_longest_sapmple():
    """ itertools.zip_longest(*iterables, fillvalue=None)는
    같은 개수의 자료형을 묶는 파이썬 내장 함수인 zip()과 똑같이 동작한다. 
    하지만 itertools.zip_longest는 객체의 길이가 다르다면 
    긴 것을 기준으로 빠진 값은 fillvalue에 설정한 값으로 채운다. """
    student = ['kim', 'lee', 'hong', 'han', 'choi']
    rewards = ['candy', 'jelly', 'chocolate']
    result = zip(student, rewards)
    result = list(result)
    print(result)
    result = itertools.zip_longest(student, rewards, fillvalue='caramel')
    result = list(result)
    print(result)


def permutatins_sample():
    """ itertools.permutatins(iterable, r=None): 객체 중에서 r개를 선택하는 순열.
     """
    numList = ['1', '2', '3']
    result = itertools.permutations(numList, 2)
    result = list(result)
    print(result)
    """ 
    >>> [('1', '2'), ('1', '3'), ('2', '1'), ('2', '3'), ('3', '1'), ('3', '2')]
     """


def combinations_sample():
    """ itertools.combinations(iterable, r): 객체 중에서 r개를 선택하는 조합.
    로또 = len(list(itertools.combinations(range(1, 46), 6))) """
    numList = ['1', '2', '3']
    result = itertools.combinations(numList, 2)
    result = list(result)
    print(result)
    """ 
    >>> [('1', '2'), ('1', '3'), ('2', '3')]
     """


class cmp_to_key_sample:
    """ functools.cmp_to_key: sorted()와 같은 정렬 함수의 key 매개변수에 
    함수를 전달할 때 사용하는 함수이다. 단 func() 한수는 두 개의 인수를 입력하여 
    첫 번째 인수를 기준으로 그 둘을 비교하고 작으면 음수, 같으면 0, 
    크면 양수를 반환하는 비교 함수여야 한다. """


    def my_cmp(x, y):
        # x가 y보다 작으면 -1, 같으면 0, 크면 1 반환
        if x < y:
            return -1
        elif x > y:
            return 1
        else:
            return 0


    # 문자열 리스트를 my_cmp 함수를 이용해 정렬
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
    words_sorted = sorted(words, key=functools.cmp_to_key(my_cmp))
    print(words_sorted)


    """ 위 코드에서 my_cmp 함수는 두 개의 인자를 비교하여, 
    작으면 -1, 같으면 0, 크면 1을 반환합니다. 그리고 cmp_to_key 함수를 사용하여 
    my_cmp 함수를 key 함수로 변환한 뒤, sorted 함수에 이를 인자로 전달합니다. 
    이때, key 함수는 각 원소에 대해 값을 계산하여 정렬에 사용하는 함수입니다. 
    따라서, 위 코드에서 words_sorted 리스트는 my_cmp 함수를 이용하여 
    정렬된 결과를 담고 있습니다.
    >>> ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
     """


class lru_cache_sample:
    """ lru_cache는 파이썬 3에서 제공하는 데코레이터(decorator) 함수 중 하나로, 
    함수의 호출 결과를 캐싱하여 이전에 같은 인자로 호출됐을 때 
    캐시된 결과를 반환하여 실행 시간을 단축시키는 기능을 제공합니다. 
    lru_cache는 "Least Recently Used"의 약자로, 
    가장 최근에 사용하지 않은(가장 오래된) 결과를 캐시에서 삭제하고 
    새로운 결과를 캐싱합니다. 이를 통해 캐시 크기를 유지하면서 
    자주 사용되는 결과를 메모리에 캐싱하여 더 빠른 실행 속도를 제공할 수 있습니다. 
    lru_cache는 다음과 같은 인자를 받습니다. 
    maxsize: 캐시 크기를 지정합니다. 기본값은 None으로, 캐시 크기를 제한하지 않습니다. 
    0보다 큰 값을 지정하면, 지정한 값 이상의 결과는 캐시되지 않습니다. 
    typed: 기본값은 False이며, True로 지정하면 인자의 타입까지 구분하여 캐시합니다. 
    lru_cache를 사용하려면, 먼저 해당 함수를 정의한 뒤, 
    함수에 @lru_cache 데코레이터를 추가하면 됩니다. 
    예를 들어, 아래 코드는 lru_cache를 사용하여 
    fibonacci 함수의 실행 시간을 단축시키는 예시입니다.
     """


    @functools.lru_cache(maxsize=128)
    def fibonacci(self, n):
        if n <= 1:
            return n
        else:
            return self.fibonacci(n-1) + self.fibonacci(n-2)
    

    """ 위 코드에서 fibonacci 함수는 재귀적으로 호출되며, 호출 결과를 캐싱합니다. 
    이를 위해 @lru_cache 데코레이터를 함수에 추가하고, 
    maxsize 인자를 이용하여 캐시 크기를 제한하였습니다. 
    이제 fibonacci 함수를 호출할 때마다 캐시된 결과를 확인하여 
    중복된 계산을 하지 않아 실행 시간을 단축시킬 수 있습니다.
     """


class partial_sample():
    """ functools.partial: 인수가 이미 채워진, 새 버전의 함수를 만들 때 사용.
    cal('add', 1, 2, 3) -> Use it like below.
     """
    def cal(self, typ: str, *args) -> float:
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


    def usage(self):
        add = functools.partial(self.cal, 'add')
        mul = functools.partial(self.cal, 'mul')
        print(add(1, 2, 3))
        print(mul(4, 5, 6))
        print(add.func, add.args)
        print(mul.func, mul.args)


def reduce_sample():
    """ functools.reduce(function, iterable)은 
    function을 반복 가능한 객체에 차례대로(왼쪽에서 오른쪽으로) 
    누적 적용하여 값을 줄이는 함수.
     """
    data = [1, 2, 3, 4, 5]
    result = functools.reduce(lambda x, y: x + y, data)
    # ((((1 + 2) + 3) + 4) + 5)
    print(result)
    """ >>> 15 """
   

class wraps_sample:
    """ functools.wraps는 
    파이썬에서 함수 데코레이터(decorator)를 작성할 때 사용되는 유틸리티입니다. 
    데코레이터를 사용하면 기존 함수의 동작을 확장하거나 수정할 수 있습니다. 
    하지만 기존 함수의 메타데이터(metadata) 정보들이 새로운 함수로 복사되지 
    않을 수 있습니다. 이러한 경우 functools.wraps 데코레이터를 사용하여 
    기존 함수의 메타데이터 정보들을 새로운 함수로 복사할 수 있습니다.
     """
    def my_decorator(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("Before the function is called.")
            result = func(*args, **kwargs)
            print("After the function is called.")
            return result
        return wrapper


    @my_decorator
    def my_function(self):
        """This is my function."""
        print("Hello, world!")


    print(my_function.__name__)
    print(my_function.__doc__)


    """ 이 코드에서 my_decorator 함수는 my_function 함수를 데코레이팅 합니다. 
    my_decorator 함수는 functools.wraps 데코레이터를 사용하여 
    wrapper 함수가 my_function 함수의 메타데이터 정보들을 가져올 수 있도록 해줍니다. 
    my_function 함수의 __name__ 속성과 __doc__ 속성은 
    my_decorator 함수에서 생성된 wrapper 함수로 복사됩니다.

    >>> This is my function.

    즉, functools.wraps를 사용하여 메타데이터 정보를 복사하면 
    데코레이터를 사용하더라도 원래 함수의 메타데이터 정보를 유지할 수 있습니다.
     """


def itemgetter_sample():
    """ operator.itemgetter는 주로 sorted와 같은 함수의 
    key 매개변수에 적용하여 다양한 기준으로 정렬할 수 있도록 하는 모듈.
     """
    students = [
        ('jane', 22, 'A'), 
        ('dave', 32, 'B'), 
        ('sally', 17, 'B'), 
    ]
    result = sorted(students, key=operator.itemgetter(1))
    print(result)
    """ 
    >>> [('sally', 17, 'B'), ('jane', 22, 'A'), ('dave', 32, 'B')]
     """
    students = [
        {'name': 'jane', 'age': 22, 'grade': 'A'}, 
        {'name': 'dave', 'age': 32, 'grade': 'B'}, 
        {'name': 'sally', 'age': 17, 'grade': 'B'}, 
    ]
    result = sorted(students, key=operator.itemgetter('age'))
    print(result)
    """ 
    >>> [{'name': 'sally', 'age': 17, 'grade': 'B'}, 
    >>> {'name': 'jane', 'age': 22, 'grade': 'A'}, 
    >>> {'name': 'dave', 'age': 32, 'grade': 'B'}, ]
    클래스의 객체인 경우 attrgetter 사용
    result = sorted(students, key=operator.attrgetter('age'))
     """


def pathlib_sample():
    """ pathlib: 파일 시스템 경로를 문자열이 아닌 객체로 취급한다. """
    # 예제1
    path0 = 'C:/users/jkhong/Desktop'
    path1 = pathlib.Path.home()/'Desktop'
    path2 = pathlib.Path('C:/users/jkhong/Desktop')
    print(path0)
    print(path1)
    print(path2)
    """ 
    >>> C:/users/jkhong/Desktop
    >>> C:\Users\jkhong\Documents\Desktop
    >>> C:\users\jkhong\Desktop
     """
    # 예제2
    files = path2.glob('*.*')
    for i in files:
        new = i.parent.joinpath('newDir', i.name)
        print(new)
        """ 
        >>> 'C:\users\jkhong\Desktop\newDir\desktop.ini'

        replace는 shutil.move와 같음.
         """
    # 예제3
    ext = collections.Counter([i.suffix for i in path2.iterdir()])
    print(ext)
    """ 
    suffix는 .을 포함한 파일 확장자를 뜻함.
    pathlib.Path.cwd().iterdir() 이런식으로도 사용
    >>> Counter({'': 9, '.lnk': 6, '.ini': 1, '.bat': 1})
     """
   

def fileinput_sample():
    """ fileinput: 여러 개의 파일을 한꺼번에 처리.
    한글이 포함된 txt인 경우 cp949에러가 발생할 수 있다. 
    아래 예제는 바탕화면에 있는 모든 txt 파일에 있는 글자를 프린트 해준다.
     """
    path1 = glob.glob('C:/users/jkhong/Desktop/*.txt')
    with fileinput.input(path1) as txt:
        for line in txt:
            print(line)


def filecmp_sample():
    """ filecmp: 파일이나 디렉터리 두 곳을 비교 """
    A = r"C:\Users\jkhong\Desktop\git\maya"
    B = r"C:\Users\jkhong\Desktop\git\mmp"
    result = filecmp.dircmp(A, B)
    print(result.left_only) # A에는 있는데, B에는 없는 파일 출력.
    print(result.right_only) # B에는 있는데, A에는 없는 파일 출력.
    print(result.diff_files) # A와 B에 모두 있으나, 파일이 서로 다름.
    result.report() # 위의 내용을 한꺼번에 볼 수 있다.


def tempfile_sample():
    """ tempfile: 임시 파일을 만드는 모듈 """
    _tempFile = tempfile.TemporaryFile(mode='w+')
    for i in range(10):
        _tempFile.write(str(i))
        _tempFile.write('\n')
    _tempFile.seek(0)
    _tempFile.close()
    """ seek(0)을 수행하여 파일을 처음부터 읽을 수 있도록 한다.
    close()가 실행되거나, 프로세스가 종료되면 임시 파일은 삭제된다. """
   

def glob_sample():
    """ glob: 패턴(유닉스 셸이 사용하는 규칙)으로 파일을 검색하는 모듈 """
    for fileName in glob.glob("**/*.txt", recursive=True):
        print(fileName)


def fnmatch_sample():
    """ fnmatch는 특정 패턴과 일치하는 파일을 검색하는 모듈이다.
    1. 파일명은 a로 시작한다.
    2. 확장자는 .py이다.
    3. 확장자를 제외한 파일명의 길이는 5이다.
    4. 파일명의 마지막 5번째 문자는 숫자이다.
     """
    filtering = "a???[0-9].py"
    for i in pathlib.Path(".").rglob("*.py"):
        if fnmatch.fnmatch(i, filtering):
            print(i)


def linecache_sample():
    """ linecache는 파일에서 원하는 줄의 값을 읽을 때, 
    캐시를 사용하여 내부적으로 최적화.
    checkcache, clearcache, getline과 getlines 등이 있다.
     """
    num = 1
    tmp = linecache.getline(r"C:\Users\jkhong\Desktop\test.txt", num)
    print(tmp)
   

def pickle_sample():
    """ pickle은 자료형을 변환 없이 그대로 파일로 저장 """
    data = {}
    data[1] = {"name": "HONGJINKI", "age": 45, "tall": "171cm"}
    with open(r"C:\Users\hjk03\Desktop\data.p", "wb") as pic:
        pickle.dump(data, pic)
    with open(r"C:\Users\hjk03\Desktop\data.p", "rb") as pic:
        temp = pickle.load(pic)
        print(temp)



""" copyreg는 Python의 내장 모듈 중 하나로, 
객체 직렬화와 역직렬화를 지원하는 pickle 모듈의 기능을 확장하기 위한 도구입니다. 
pickle 모듈은 객체를 이진 형식으로 직렬화하여 저장하거나, 
저장된 이진 데이터를 역직렬화하여 객체로 복원하는 기능을 제공합니다. 
하지만 pickle 모듈은 모든 객체를 자동으로 직렬화할 수는 없습니다. 
예를 들어, 내장 자료형 외의 사용자 정의 객체나 외부 라이브러리의 객체를 직렬화할 때 
문제가 발생할 수 있습니다. 이때 copyreg 모듈을 사용하면, 
pickle 모듈이 객체를 직렬화할 때 특정 함수를 호출하도록 등록할 수 있습니다. 
이 함수는 해당 객체를 직렬화할 때 사용됩니다. 
이를 통해 사용자 정의 객체나 외부 라이브러리의 객체도 
pickle 모듈로 직렬화할 수 있습니다. 예를 들어, copyreg 모듈을 사용하여 
사용자 정의 클래스 Person을 pickle 모듈로 직렬화할 수 있습니다. 
Person 클래스는 name과 age라는 두 개의 속성을 가진 클래스입니다.
 """


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def pickle_person(person):
    return Person, (person.name, person.age)


copyreg.pickle(Person, pickle_person)
person = Person("Alice", 25)
person_data = pickle.dumps(person)


""" 이 예제에서는 pickle_person 함수를 Person 클래스로 직렬화하기 위해 
copyreg.pickle 함수를 사용하였습니다. 이제 person 객체를 pickle 모듈로 직렬화하여 
person_data 변수에 저장할 수 있습니다. 
역직렬화할 때는 pickle 모듈을 사용하여 person_data를 다시 객체로 변환할 수 있습니다.
 """


class shelve_sample():
    """ shelve는 딕셔너리를 파일로 저장할 때 사용하는 모듈
    shelve는 딕셔너리만을 처리하지만, pickle은 모든 객체를 다룬다.
     """
    def __init__(self):
        self.main()


    def main(self):
        self.save("number", [1, 2, 3, 4, 5])
        print(self.get("number"))


    # 바탕화면에 .dat파일을 만든다.
    def save(self, key, value):
        with shelve.open(r"C:\Users\hjk03\Desktop\data.dat") as shlv:
            shlv[key] = value


    # 저장된 .dat파일에서 key값으로 value값을 불러온다.
    def get(self, key):
        with shelve.open(r"C:\Users\hjk03\Desktop\data.dat") as shlv:
            return shlv[key]


""" sqlite3: SQLite 데이터베이스를 사용하는 데 필요한 인터페이스 모듈.
https://sqlitebrowser.org/dl/ """


# DB와 연결
conn = sqlite3.connect('blog.db')


# 쿼리문을 실행하려면 cursor()가 필요함
curs = conn.cursor()


# 테이블 만들기
createTable = """ CREATE TABLE blog 
(id integer PRIMARY KEY, subject text, content text, date text) """
curs.execute(createTable)


# 데이터 입력하기
# 방법1: 보안에 취약. SQL injection 공격
insertValue = """ INSERT INTO blog VALUES 
(1, "My First Blog.", "This is a First Content.", "20221008") """
curs.execute(insertValue)


# 방법2: 보안에 취약. 사용자가 악의적인 쿼리를 던질 수도 있음
_id = 2
subject = 'My Second Blog.'
content = 'Second content.'
date = '20221009'
insertValue = """ INSERT INTO blog VALUES 
(%d, "%s", "%s", "%s") """ % (_id, subject, content, date)
curs.execute(insertValue)


# 방법3: 물음표 스타일. 보안에 그나마 괜찮음.
_id = 3
subject = 'My Third Blog.'
content = 'Third content.'
date = '20221010'
insertValue = """ INSERT INTO blog VALUES 
(?, ?, ?, ?) """, (_id, subject, content, date)
curs.execute(insertValue)


# 방법4: 딕셔너리 사용. 보안에 그나마 괜찮음.
dic = {
    "id": 4, 
    "subject": "My Fourth Blog.", 
    "content": "Fourth content.", 
    "date": "20221011"
}
insertValue = """ INSERT INTO blog VALUES 
(:id, :subject, :content, :date) """, dic
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


def zlib_sample():
    """ zlib는 문자열을 압축하고 해제할 수 있다. """
    data = "Life is too short, You need python." * 10000
    compress_data = zlib.compress(data.encode(encoding='utf-8'))
    print(len(compress_data))
    """ >>> 1077 """


    org_data = zlib.decompress(compress_data).decode(encoding='utf-8')
    print(len(org_data))
    """ >>> 350000 """


def gzip_sample():
    """ gzip는 파일을 압축할 수 있다. 내부적으로 zlib를 사용. """
    data = "Life is too short, You need python.\n" * 10000
    with gzip.open('C:/Users/jkhong/Desktop/data.txt.gz', 'wb') as File:
        File.write(data.encode('utf-8'))
    with gzip.open('C:/Users/jkhong/Desktop/data.txt.gz', 'rb') as File:
        read_data = File.read().decode('utf-8')
    print(len(read_data))
    """ >>> 360000 """


def bz2_sample():
    # bz2: 문자열을 압축할 수 있다. 스레드 환경에서 안전함.
    data = "Life is too short, You need python." * 10000
    compress_data = bz2.compress(data.encode(encoding='utf-8'))
    print(len(compress_data))
    """ >>> 163 """
    org_data = bz2.decompress(compress_data).decode(encoding='utf-8')
    print(len(org_data))
    """ >>> 350000 """


    # 파일도 압축, 해제 할 수 있다.
    data = "Life is too short, You need python.\n" * 10000
    with bz2.open('C:/Users/jkhong/Desktop/data.txt.bz2', 'wb') as File:
        File.write(data.encode('utf-8'))
    with bz2.open('C:/Users/jkhong/Desktop/data.txt.bz2', 'rb') as File:
        read_data = File.read().decode('utf-8')
    print(len(read_data))
    """ >>> 360000 """


def lzma_sample():
    # lzma는 문자열을 압축할 수 있다. 스레드 환경에서 안전하지 않음.
    data = "Life is too short, You need python." * 10000
    compress_data = lzma.compress(data.encode(encoding='utf-8'))
    print(len(compress_data))
    """ >>> 220 """
    org_data = lzma.decompress(compress_data).decode(encoding='utf-8')
    print(len(org_data))
    """ >>> 350000 """


    # 파일도 압축, 해제 할 수 있다.
    data = "Life is too short, You need python.\n" * 10000
    with lzma.open('C:/Users/jkhong/Desktop/data.txt.xz', 'wb') as File:
        File.write(data.encode('utf-8'))
    with lzma.open('C:/Users/jkhong/Desktop/data.txt.xz', 'rb') as File:
        read_data = File.read().decode('utf-8')
    print(len(read_data))
    """ >>> 360000 """


def zipfile_sample():
    # zipfile: 여러개의 파일을 zip형식으로 합치거나 해제할 수 있다.
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


def tarfile_sample():
    # tarfile: 여러개의 파일을 tar형식으로 합치거나 해제할 수 있다.
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


def csv_sample():
    """ csv는 csv 파일을 읽고 쓸 때 사용.
    엑셀 파일 안에 쉼표가 있을 경우 split(',') 이것 사용은 위험하다.
     """
    result = []
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
   

def configparser_sample():
    """ configparser: ini 파일은 프로그램 정보를 저장하는 텍스트 문서로
    섹션과 그 섹션에 해당하는 "키 = 값"으로 구성된다. 
    configparser는 이러한 형식의 ini 파일을 처리할 때 사용하는 모듈이다.
    파일명: ftp.ini


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
     """
    

    config = configparser.ConfigParser()
    config.read('C:/folder/ftp.ini')
    ftp2_port = config['FTP2']['PORT']
    print(ftp2_port)
    """ >>> 22221 """
   

def hashlib_sample():
    """ hashlib: MD5, SHA256 등의 알고리즘으로 문자열을 해싱한다.
    해싱은 단방향 암호화 알고리즘이므로 원래의 문자열을 복구할 수는 없다.
     """
    m = hashlib.sha256()
    m.update('Life is too short'.encode('utf-8'))
    m.update(', you need python.'.encode('utf-8'))


    # digest(): 바이트 문자열을 반환
    byteStr = m.digest()


    # hexdigest(): 바이트 문자열을 16진수로 반환
    hexaStr = m.hexdigest()
    print(byteStr)
    print(hexaStr)


def hmac_sample():
    """ hmac: 메시지 변조를 확인할 수 있다. 단, 비밀키가 있어야 한다. """
    SECRET = 'password'
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


def secrets_sample():
    """ secrets: 안전한 난수 발생
    1바이트는 2개의 16진수 문자열로 반환되므로 (16)은 32자리 난수가 된다.
     """
    key = secrets.token_hex(16)
    print(key)
    """ >>> 9ebc02692b6fdd124a5af3e7ffd97781 """


class io_StringIO_sample():
    """ io.StringIO: 문자열을 파일 객체처럼 다룰 수 있도록 하는 클래스이다. """
    # csv 파일의 내용을 아래처럼 간단하게 문자열로 만든다.
    def __init__(self):
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


class argparse_sample():
    """ argparse는 파이썬 표준 라이브러리의 모듈 중 하나로, 
    명령줄 인자를 파싱하기 위한 도구입니다. 즉, argparse를 사용하면 
    스크립트에 전달된 인자를 쉽게 처리할 수 있습니다. 
    argparse를 사용하면 스크립트 실행 시 명령줄 인자를 정의하고, 
    사용자가 그에 맞는 값을 입력할 때마다 해당 인자를 파싱하여 쉽게 사용할 수 있습니다. 
    argparse는 많은 기능을 제공하며, 예를 들어 다음과 같은 기능을 제공합니다.
    1. 인자의 유효성 검사
    2. 인자의 타입 변환
    3. 인자의 기본값 설정
    4. 인자의 도움말 출력
    argparse를 사용하기 위해서는 먼저 argparse 모듈을 임포트하고, 
    ArgumentParser 클래스를 인스턴스화해야 합니다. 
    ArgumentParser 클래스의 인스턴스를 생성한 후, 
    add_argument() 메서드를 사용하여 인자를 추가할 수 있습니다. 
    이 메서드는 인자의 이름, 인자의 타입, 인자의 도움말 등을 지정할 수 있습니다. 
    다음은 간단한 예시 코드입니다.
     """


    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='이름을 입력하세요')
    parser.add_argument('--age', type=int, default=20, help='나이를 입력하세요')
    args = parser.parse_args()
    print(f'이름: {args.name}')
    print(f'나이: {args.age}')


    """ 위 코드는 --name과 --age라는 두 개의 인자를 정의하고, 
    사용자가 이를 입력할 수 있도록 합니다. 
    --name은 문자열 타입이며, 도움말에는 이름을 입력하세요라는 문구가 출력됩니다. 
    --age는 정수 타입이며, 기본값은 20입니다. 
    도움말에는 나이를 입력하세요라는 문구가 출력됩니다. 
    이제 이 스크립트를 실행할 때 다음과 같이 인자를 전달할 수 있습니다.
    """
    # python script.py --name 'Alice' --age 25
    """ 이렇게 전달된 인자는 argparse가 파싱하여 args 변수에 저장되며, 
    이후에는 이를 자유롭게 사용할 수 있습니다. 
    위 예시 코드에서는 args.name과 args.age를 출력하는 방식으로 
    사용자가 전달한 인자를 출력합니다.
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


