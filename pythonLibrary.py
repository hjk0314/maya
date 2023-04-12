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
import graphlib
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
import concurrent.futures
import subprocess
import sched
import asyncio
import aiohttp
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
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import parse
import webbrowser
import cgi
import cgitb
import wsgiref
from wsgiref.simple_server import make_server
import urllib.parse
import urllib.request
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
    g = graphlib.Graph()
    g.add_node('A')
    g.add_node('B')
    g.add_edge('A', 'B')
    

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


class logging_sample:
    """ logging은 파이썬에서 제공하는 모듈로, 
    애플리케이션의 로그 메시지를 기록하는 기능을 제공합니다. 
    로깅은 디버깅, 성능 향상, 오류 분석 등 다양한 목적으로 사용됩니다. 
    logging 모듈은 여러 개의 로깅 레벨을 제공하며, 
    이를 이용하여 어느 정도의 로그 메시지를 출력할지 결정할 수 있습니다. 
    로깅 레벨은 다음과 같습니다. DEBUG: 디버깅 목적으로 자세한 정보를 기록합니다. 

    
    INFO: 애플리케이션의 주요 이벤트를 기록합니다. 
    WARNING: 애플리케이션의 경고성 이벤트를 기록합니다. 
    ERROR: 애플리케이션의 오류 이벤트를 기록합니다. 
    CRITICAL: 심각한 오류가 발생한 경우 기록합니다. 

    
    logging 모듈은 다양한 로그 기록 방식을 제공합니다. 
    대표적인 방식은 다음과 같습니다. 

    
    StreamHandler: 터미널에 로그 메시지를 출력합니다.
    FileHandler: 파일에 로그 메시지를 출력합니다.
    RotatingFileHandler: 크기나 날짜 등을 기준으로 로그 파일을 자동으로 교체합니다.
    TimedRotatingFileHandler: 주기적으로 로그 파일을 자동으로 교체합니다.
    logging 모듈을 사용하면 로그 메시지를 기록하고 관리하는 것이 편리해집니다. 
    디버깅 및 애플리케이션 분석 시 유용한 정보를 제공하며, 
    오류 및 경고 사항을 적절하게 처리할 수 있습니다.
    """


    # 로그 레벨 설정
    logging.basicConfig(level=logging.DEBUG)


    # 로그 메시지 출력
    logging.debug('Debugging message')
    logging.info('Information message')
    logging.warning('Warning message')
    logging.error('Error message')
    logging.critical('Critical message')


class getpass_sample():
    """ getpass 모듈은 사용자로부터 비밀번호나 기타 민감한 정보를 입력받을 때, 
    터미널에서 입력한 내용이 화면에 표시되지 않도록 하는 기능을 제공합니다. 
    getpass 모듈의 기본 함수는 getpass() 입니다. 
    이 함수는 사용자로부터 입력받을 때, 입력한 내용을 터미널에 출력하지 않습니다. 
    즉, 입력한 비밀번호나 민감한 정보가 화면에 노출되지 않습니다. 
    아래는 getpass() 함수의 간단한 사용 예시입니다. 
     """


    password = getpass.getpass('Enter your password: ')
    print('Your password is:', password)


    """ 위 코드에서 getpass.getpass() 함수는 사용자로부터 입력받을 때, 
    입력한 내용을 터미널에 출력하지 않습니다. 
    대신 입력한 내용을 password 변수에 저장합니다. 
    그리고 print() 함수를 이용하여 password 변수에 저장된 내용을 출력합니다. 
    이처럼 getpass() 함수는 보안이 중요한 프로그램에서 사용자의 
    민감한 정보를 입력받을 때, 사용될 수 있습니다.
     """


class curses_sample:
    """ curses는 UNIX 및 UNIX-like 시스템의 터미널 환경에서 
    텍스트 기반 인터페이스를 만들기 위한 라이브러리입니다. 
    curses는 터미널에서 마우스 입력, 색상, 창 레이아웃 및 키보드 입력 등을 처리하며, 
    터미널에서 프로그램을 실행할 때 사용자와 상호 작용하는 
    인터페이스를 생성하는 데 사용됩니다.
    Python에서 curses 모듈은 터미널 UI를 만들기 위한 기능을 제공합니다. 
    이 모듈은 유닉스 계열 운영체제에서만 사용할 수 있으며, 
    터미널에서 실행할 수 있는 프로그램을 만드는 데 사용됩니다. 
    curses 모듈은 터미널에서 미리 정의된 화면 위치 및 색상을 사용하여 
    텍스트 인터페이스를 생성할 수 있습니다.
    curses 모듈의 주요 기능으로는 다음과 같은 것이 있습니다.
    

     - 유니코드를 지원하는 터미널 UI
     - 마우스 및 키보드 이벤트 처리
     - 다양한 색상과 스타일을 사용하여 텍스트 출력
     - 다중 창 및 패널 지원
     - 텍스트 애니메이션 및 유연한 레이아웃 제공


    다음은 curses 모듈을 사용하여 간단한 텍스트 인터페이스를 만드는 예시입니다.
     """


    # curses 초기화
    stdscr = curses.initscr()


    # 사용자 정의 색상 설정
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)


    # 메시지 출력
    stdscr.addstr(5, 10, "Hello, World!", curses.color_pair(1))


    # 키보드 입력 대기
    stdscr.getch()


    # curses 종료
    curses.endwin()


    """ 위 예시에서는 curses.initscr() 함수를 사용하여 curses를 초기화합니다. 
    그리고 curses.start_color() 함수를 사용하여 사용자 정의 색상을 설정합니다. 
    curses.init_pair() 함수를 사용하여 색상 쌍을 만들고, 
    curses.color_pair() 함수를 사용하여 해당 색상 쌍을 선택합니다.
    stdscr.addstr() 함수를 사용하여 메시지를 출력하고, 
    stdscr.getch() 함수를 사용하여 키보드 입력을 대기합니다. 
    마지막으로 curses.endwin() 함수를 사용하여 curses를 종료합니다.
     """



class platform_sample:
    """ platform 모듈은 
    파이썬에서 실행되는 시스템에 대한 정보를 제공하는 모듈입니다. 
    이 모듈은 운영 체제, 버전, 프로세서, 파이썬 버전 등의 정보를 가져올 수 있습니다. 
    platform 모듈을 사용하면 파이썬 코드를 운영 체제 또는 하드웨어와 관련된 
    특정 작업을 수행하는 데 사용할 수 있습니다. 
    예를 들어, 파이썬 코드를 특정 운영 체제에 맞게 조정하거나, 
    코드를 실행할 시스템의 하드웨어 자원에 따라 다른 실행 경로를 선택할 수 있습니다. 
    platform 모듈의 주요 함수와 속성으로는 다음과 같은 것들이 있습니다.

    
    1. platform.system(): 현재 시스템의 운영 체제를 반환합니다. 
     - 예를 들어, Windows, Linux, macOS 등이 반환됩니다.
    2. platform.release(): 현재 시스템의 운영 체제 버전을 반환합니다. 
     - 예를 들어, Windows 10, Ubuntu 20.04 LTS 등이 반환됩니다.
    3. platform.machine(): 현재 시스템의 프로세서 아키텍처를 반환합니다. 
     - 예를 들어, x86_64, armv7l 등이 반환됩니다.
    4. platform.processor(): 현재 시스템의 실제 프로세서 이름을 반환합니다. 
     - 예를 들어, Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz 등이 반환됩니다.
    5. platform.python_version(): 현재 파이썬 인터프리터의 버전을 반환합니다. 
     - 예를 들어, 3.9.4 등이 반환됩니다.
    6. platform.platform(): 현재 시스템의 전체 플랫폼 이름을 반환합니다. 
     - 예를 들어, Windows-10-10.0.19041-SP0 등이 반환됩니다.


    이처럼 platform 모듈은 파이썬 코드를 운영 체제와 관련된 작업을 
    수행하는 데 사용할 수 있습니다. 이 모듈은 파이썬 코드를 운영 체제에 맞게 
    조정하는 데 매우 유용합니다.
     """


    # 현재 시스템의 운영 체제를 출력합니다.
    print(f"Operating System: {platform.system()}")


    # 현재 시스템의 운영 체제 버전을 출력합니다.
    print(f"OS Version: {platform.release()}")


    # 현재 시스템의 프로세서 아키텍처를 출력합니다.
    print(f"Processor Architecture: {platform.machine()}")


    # 현재 시스템의 실제 프로세서 이름을 출력합니다.
    print(f"Processor Name: {platform.processor()}")


    # 현재 파이썬 인터프리터의 버전을 출력합니다.
    print(f"Python Version: {platform.python_version()}")


    # 현재 시스템의 전체 플랫폼 이름을 출력합니다.
    print(f"Platform Name: {platform.platform()}")


class ctypes:
    """ ctypes는 C 언어의 라이브러리 함수를 파이썬에서 사용할 수 있도록 
    해주는 모듈입니다. ctypes 모듈을 사용하면 파이썬 코드에서 C 함수를 직접 
    호출할 수 있으며, C 구조체 및 데이터 타입도 파이썬에서 사용할 수 있습니다.
    ctypes 모듈을 사용하여 C 함수를 호출할 때는, 
    해당 함수가 정의된 라이브러리 파일을 불러와야 합니다. 
    이를 위해 ctypes 모듈의 CDLL 함수를 사용합니다. 
    CDLL 함수는 라이브러리 파일의 경로를 인자로 받아 해당 라이브러리를 불러옵니다.
    ctypes 모듈은 다양한 데이터 타입을 지원합니다. 
    C의 데이터 타입과 대응하는 파이썬 데이터 타입으로는 다음과 같은 것들이 있습니다.


    c_char: char 타입과 대응
    c_short: short 타입과 대응
    c_int: int 타입과 대응
    c_long: long 타입과 대응
    c_longlong: long long 타입과 대응
    c_float: float 타입과 대응
    c_double: double 타입과 대응
    c_void_p: void 포인터 타입과 대응
     """


    # 라이브러리 파일을 불러옵니다.
    my_lib = ctypes.CDLL("my_library.so")


    # C 함수를 불러와 파이썬에서 호출합니다.
    result = my_lib.my_function(1, 2)


    # 결과를 출력합니다.
    print(result)


""" 위 코드에서 my_library.so는 C 언어로 작성된 라이브러리 파일입니다. 
my_function은 해당 라이브러리에 정의된 C 함수입니다. 
ctypes 모듈을 사용하여 이 함수를 불러와 파이썬에서 호출한 후, 결과를 출력합니다.
ctypes 모듈을 사용하여 C 구조체를 파이썬에서 사용하는 예제 코드는 다음과 같습니다.
 """


# C 구조체를 정의합니다.
class MyStruct(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


# 구조체를 생성합니다.
my_struct = MyStruct()


# 구조체 멤버에 값을 할당합니다.
my_struct.x = 1
my_struct.y = 2


# 구조체 멤버 값을 출력합니다.
print(my_struct.x)
print(my_struct.y)


class threading_sample:
    """ threading은 
    스레드를 이용하여 한 프로세스에서 2가지 이상의 일을 실행할 때 쓰인다.
    threading 모듈은 파이썬에서 스레드를 생성하고 관리하는 데 사용되는 모듈입니다. 
    스레드란, 동시에 여러 작업을 처리하기 위해 사용되는 실행 흐름입니다. 
    threading 모듈을 사용하여 여러 스레드를 생성하고 실행할 수 있습니다. 
    threading 모듈에서 가장 기본적인 클래스는 Thread 클래스입니다. 
    Thread 클래스는 스레드를 생성하고 실행하는 데 사용됩니다. 
    스레드를 생성하려면, Thread 클래스의 생성자에 실행할 함수를 전달합니다. 
    이후 start() 메서드를 호출하여 스레드를 실행합니다. 
    다음은 Thread 클래스를 사용하여 스레드를 생성하고 실행하는 예제 코드입니다.
     """


    # 스레드에서 실행할 함수를 정의합니다.
    def print_numbers():
        for i in range(1, 11):
            print(i)


    # 스레드를 생성합니다.
    my_thread = threading.Thread(target=print_numbers)


    # 스레드를 실행합니다.
    my_thread.start()


class multiprocessing_sample:
    """ multiprocessing은 
    멀티 프로세스를 활용하여, 2가지 이상의 일을 동시에 실행할 때 쓰인다.
    멀티프로세싱은 멀티코어 CPU를 사용하여 동시에 여러 작업을 처리하는 기술로, 
    멀티스레딩과 비교하여 더 많은 작업을 처리할 수 있습니다.
    multiprocessing 모듈은 threading 모듈과 유사한 인터페이스를 제공하며, 
    Process 클래스를 사용하여 프로세스를 생성하고 실행합니다. 
    Process 클래스는 스레드와 마찬가지로 target 인자에 실행할 함수를 전달하여 
    프로세스를 생성합니다. 그러나 Process 클래스는 start() 메서드를 호출하여 
    프로세스를 실행합니다.
    다음은 multiprocessing 모듈을 사용하여 
    프로세스를 생성하고 실행하는 예제 코드입니다.
     """


    # 프로세스에서 실행할 함수를 정의합니다.
    def print_numbers():
        for i in range(1, 11):
            print(i)


    # 프로세스를 생성합니다.
    my_process = multiprocessing.Process(target=print_numbers)


    # 프로세스를 실행합니다.
    my_process.start()


    """ 위 코드에서 print_numbers() 함수를 정의하고, 
    Process 클래스의 생성자에 해당 함수를 전달하여 
    my_process라는 프로세스 객체를 생성합니다. 
    이후 my_process.start()를 호출하여 프로세스를 실행합니다.
    multiprocessing 모듈에서는 스레드를 생성하고 관리하는 데에 
    유용한 다양한 클래스와 메서드를 제공합니다. 
    이 중 몇 가지를 살펴보겠습니다.

    
    1. Queue 클래스: 멀티프로세스 환경에서 프로세스 간 통신을 위해 사용됩니다. 
     - 큐에 데이터를 넣고 빼는 작업을 할 수 있습니다.

     
    2. Pool 클래스: 동시에 실행 가능한 프로세스의 개수를 제한하고, 
     - 작업을 분산하여 처리하는 데 사용됩니다.

     
    3. Manager 클래스: 멀티프로세스 환경에서 공유 자원을 관리하는 데 사용됩니다. 
     - Lock, 
     - Condition, 
     - Event, 
     - Semaphore, 
     - Value, 
     - Array, 
     - Namespace 
    등의 클래스와 메서드를 제공합니다.

    
    위 클래스와 메서드들은 multiprocessing 모듈에서 제공되는 
    몇 가지 중요한 기능 중 일부입니다. multiprocessing 모듈을 사용하면 
    멀티프로세싱 환경에서도 쉽게 프로그래밍할 수 있습니다.
     """


class concurrent_futures_sample:
    """ concurrent.futures는 
    threading과 multiprocessing을 더 쉽게 사용할 때 쓰인다.
    concurrent.futures 모듈은 threading 및 multiprocessing 모듈과 같은 
    멀티스레딩 및 멀티프로세싱에 대한 고수준의 추상화 계층을 제공하며, 
    작업 처리를 간단하게 하고 병렬화할 수 있습니다.
    concurrent.futures 모듈은 
    ThreadPoolExecutor 클래스와 ProcessPoolExecutor 클래스를 제공합니다. 
    ThreadPoolExecutor 클래스는 스레드 풀을 구현하고, 
    ProcessPoolExecutor 클래스는 프로세스 풀을 구현합니다. 
    두 클래스 모두 비동기식으로 작업을 실행하며, 
    submit() 메서드를 사용하여 실행할 함수와 인자를 전달합니다.
    다음은 concurrent.futures 모듈을 사용하여 
    스레드와 프로세스를 생성하고 실행하는 예제 코드입니다.
    """


    # 스레드에서 실행할 함수를 정의합니다.
    def countdown(n):
        while n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(1)


    # 프로세스에서 실행할 함수를 정의합니다.
    def countdown_proc(n):
        while n > 0:
            print('P-minus', n)
            n -= 1
            time.sleep(1)


    # ThreadPoolExecutor를 사용하여 스레드를 생성합니다.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 스레드에 실행할 함수와 인자를 전달합니다.
        future = executor.submit(countdown, 5)
        # 실행 결과를 출력합니다.
        print(future.result())


    # ProcessPoolExecutor를 사용하여 프로세스를 생성합니다.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # 프로세스에 실행할 함수와 인자를 전달합니다.
        future = executor.submit(countdown_proc, 5)
        # 실행 결과를 출력합니다.
        print(future.result())


    """ 위 코드에서 countdown() 함수와 countdown_proc() 함수를 정의하고, 
    ThreadPoolExecutor 클래스와 ProcessPoolExecutor 클래스를 사용하여 
    각각의 스레드와 프로세스를 생성합니다. 
    submit() 메서드를 사용하여 실행할 함수와 인자를 전달하고, 
    future.result()를 사용하여 실행 결과를 출력합니다.
    concurrent.futures 모듈은 
    as_completed() 함수와 wait() 함수 등의 기능도 제공합니다. 
    이들 함수를 사용하면 작업의 실행 순서나 실행 결과를 제어하는 데 유용합니다. 
    이 모듈은 멀티스레딩 및 멀티프로세싱 작업을 처리하는 데에 있어서 간단하고 
    효율적인 방법을 제공합니다.
    """


class subprocess_sample:
    """ subprocess 모듈은 파이썬에서 외부 프로그램을 실행하고 
    상호작용하는 데 사용되는 모듈입니다. 이 모듈은 새로운 프로세스를 생성하고, 
    표준 입력, 표준 출력 및 표준 오류를 처리하며, 
    시스템 호출을 수행하는 다양한 메서드를 제공합니다.
     """
    

    with open(r"C:\Users\jkhong\Desktop\file.txt", 'wb') as txt:
        out = subprocess.run(['cmd', '/c', 'dir'], capture_output=True)
        txt.write(out.stdout)


    """ subprocess 모듈은 시스템 호출을 수행하고 
    외부 프로그램과 상호작용하는 데 유용한 도구입니다. 
    그러나 보안상의 이유로 사용자 입력을 처리하는 경우 주의해야 합니다. 
    사용자 입력을 외부 프로그램의 인자로 사용하는 경우, 
    보안상의 이유로 인해 subprocess 모듈을 사용하는 것을 피하는 것이 좋습니다. 
    이 경우 shlex 모듈을 사용하여 사용자 입력을 처리하는 것이 더 안전합니다.
     """


class sched_sample:
    """ sched는 지정된 시간에 원하는 이벤트를 실행하게 해주는 이벤트 스케줄러이다.
    이 모듈은 일정한 시간 간격으로 함수를 실행하거나, 
    일정한 시간 후에 함수를 실행하도록 예약하는 등의 작업을 수행할 수 있습니다.
    sched 모듈에서 사용되는 핵심 객체는 scheduler입니다. 
    scheduler 객체는 이벤트를 예약하고 실행하는데 사용됩니다. 
    scheduler 객체를 만든 후, enter() 메서드를 사용하여 이벤트를 예약합니다. 
    enter() 메서드에는 이벤트를 실행할 시간과 실행할 함수를 인자로 전달합니다. 
    scheduler 객체는 run() 메서드를 사용하여 예약된 이벤트를 실행합니다.
    다음은 sched 모듈을 사용하여 3초 후에 "Hello, world!"를 출력하는 예제 코드입니다.
     """


    def say_hello():
        print("Hello, world!")


    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(3, 1, say_hello, ())
    scheduler.run()


    """ 위 코드에서 sched.scheduler() 함수를 사용하여 scheduler 객체를 생성합니다. 
    이 객체를 사용하여 enter() 메서드를 사용하여 3초 후에 
    say_hello() 함수를 실행하도록 예약합니다. 
    scheduler.run() 메서드를 사용하여 예약된 이벤트를 실행합니다.
    sched 모듈은 스레드를 사용하여 여러 이벤트를 병렬로 예약하고 실행할 수도 있습니다. 
    예를 들어, threading.Timer와 함께 사용하여 반복적인 작업을 수행할 수 있습니다. 
    그러나, 고정된 타임스케줄링에서는 sched 모듈이 더 적합합니다.
     """


class asyncio_sample:
    """ asyncio는 Python에서 비동기 I/O 작업을 처리하기 위한 라이브러리입니다. 
    이를 사용하면 동시에 여러 작업을 처리할 수 있으며, 
    이러한 작업은 비동기 함수와 coroutine으로 구현됩니다. 
    asyncio는 기본적으로 이벤트 루프를 사용하여 작동합니다. 
    이벤트 루프는 비동기 I/O 작업을 처리하고 작업이 완료되면 
    해당 이벤트에 대한 콜백 함수를 실행합니다. 
    이러한 콜백 함수는 일반적으로 coroutine으로 작성되어 비동기적으로 실행됩니다.
    asyncio는 다양한 네트워크 및 웹 프레임워크와 호환되며, 
    Python 3.4 이상에서 사용할 수 있습니다. asyncio를 사용하면 
    네트워크 연결, 파일 I/O 및 다른 비동기 작업을 처리하는 것이 더 쉬워집니다.
    예를 들어, asyncio를 사용하여 비동기 HTTP 클라이언트를 작성할 수 있으며, 
    이를 통해 여러 웹 사이트로 동시에 요청을 보낼 수 있습니다. 
    또한 asyncio를 사용하여 비동기 파일 I/O를 처리하고, 
    이를 통해 여러 파일에 동시에 작성할 수 있습니다.
    마지막으로, asyncio는 매우 빠르고 확장성이 높은 라이브러리이며, 
    대규모 애플리케이션에서도 잘 작동합니다. 
    하지만, asyncio는 비동기 프로그래밍 개념을 이해해야하며, 
    초보자에게는 어려울 수도 있습니다.
     """


    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()


    async def main(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, 'https://www.example.com')
            print(html)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


    """ 이 예제에서는 aiohttp 라이브러리를 사용하여 
    비동기 HTTP 클라이언트를 작성하고 있습니다. 
    fetch 함수는 비동기 함수이며, session.get() 메서드를 사용하여 
    HTTP GET 요청을 보내고 응답을 받아들입니다. 
    그런 다음 응답을 텍스트로 변환하여 반환합니다.
    main 함수는 coroutine으로 작성되어 있으며, 
    ClientSession 클래스를 사용하여 비동기 HTTP 클라이언트 세션을 만듭니다. 
    fetch 함수를 사용하여 웹 페이지의 HTML을 가져온 다음 출력합니다.
    마지막으로, 이 예제에서는 
    asyncio 라이브러리의 get_event_loop() 함수를 사용하여 
    이벤트 루프를 가져온 다음 run_until_complete() 메서드를 사용하여 
    main 함수를 실행합니다. 이러한 방식으로 
    asyncio를 사용하여 비동기 프로그래밍을 수행할 수 있습니다.
     """


""" socket은 TCP 서버/클라이언트 프로그램을 작성할 때 사용.
파이썬에서는 socket 모듈을 제공하여 소켓 프로그래밍을 수행할 수 있습니다. 
이 모듈은 TCP 및 UDP 소켓 프로그래밍을 지원합니다.
socket 모듈에서 가장 중요한 클래스는 socket 클래스입니다. 
이 클래스는 TCP 소켓과 UDP 소켓 모두를 만들 수 있으며, 
 - bind(), 
 - listen(), 
 - accept(), 
 - connect(), 
 - send(), 
 - recv(), 
등의 메서드를 지원합니다.
다음은 간단한 TCP 서버와 클라이언트 예제입니다.
 """


# server.py
# import socket
HOST = ''   # 모든 인터페이스에서 연결을 수신합니다.
PORT = 8888 # 사용할 포트 번호입니다.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


# client.py
# import socket
HOST = 'localhost'  # 서버 호스트 이름입니다.
PORT = 8888        # 서버 포트 번호입니다.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))


""" 서버는 클라이언트의 연결을 수신하고, 
데이터를 수신하면 다시 클라이언트에게 보냅니다. 
클라이언트는 서버에 연결하고, 데이터를 보내고, 서버로부터 데이터를 수신합니다.
이것은 매우 간단한 예제이지만, socket 모듈을 사용하여 
TCP 및 UDP 프로토콜을 사용하는 다양한 네트워크 프로그램을 작성할 수 있습니다.
 """


""" ssl은 socket 모듈로 작성한 서버/클라이언트에 공개키 암호화 방식을 적용.
파이썬에서는 ssl 모듈을 사용하여 SSL/TLS 프로토콜을 사용하는 
보안 연결을 만들 수 있습니다. ssl 모듈은 내장 socket 모듈과 함께 사용할 수 있으며, 
wrap_socket() 함수를 사용하여 일반 소켓을 SSL/TLS 소켓으로 래핑할 수 있습니다.
다음은 간단한 SSL/TLS 서버와 클라이언트 예제입니다.
 """


# server.py
# import ssl
# import socket
HOST = ''   # 모든 인터페이스에서 연결을 수신합니다.
PORT = 8443 # 사용할 포트 번호입니다.
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


# client.py
# import ssl
# import socket
HOST = 'localhost'  # 서버 호스트 이름입니다.
PORT = 8443        # 서버 포트 번호입니다.
context = ssl.create_default_context()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        ssock.connect((HOST, PORT))
        ssock.sendall(b'Hello, world')
        data = ssock.recv(1024)
print('Received', repr(data))


""" 서버는 클라이언트의 연결을 수신하고, 
데이터를 수신하면 다시 클라이언트에게 보냅니다. 
클라이언트는 서버에 연결하고, 데이터를 보내고, 서버로부터 데이터를 수신합니다. 
이 예제에서는 서버에서 SSL/TLS 인증서를 사용하여 클라이언트와의 보안 연결을 설정합니다.
ssl 모듈을 사용하여 다양한 SSL/TLS 프로토콜을 사용하는 
다른 네트워크 프로그램을 작성할 수 있습니다.
 """


# import select
# import socket
class select_sample:
    """ select는 socket 프로그래밍에서 "I/O멀티플랙싱"을 가능하게 하는 모듈이다.
    select는 Unix 계열 운영체제에서 사용하는 다중 I/O 모델 중 하나로, 
    네트워크 프로그래밍에서 I/O 다중화를 구현하는 기술입니다. 
    파이썬에서는 select 모듈을 사용하여 다중 I/O를 구현할 수 있습니다.
    select 모듈은 다음과 같은 함수를 제공합니다.
    select.select(rlist, wlist, xlist[, timeout]): 
    지정된 소켓 리스트에서 읽기, 쓰기, 예외 처리 가능한 소켓을 선택합니다.
    select.poll(): poll() 객체를 만듭니다. 
    이 객체를 사용하여 다중 I/O를 구현할 수 있습니다.
    select.epoll(): epoll() 객체를 만듭니다. 
    이 객체는 poll() 객체보다 더 높은 성능을 제공합니다.
    select 모듈을 사용하여 간단한 에코 서버를 만들어 보겠습니다.
    """

    HOST = '' # 모든 인터페이스에서 연결을 수신합니다.
    PORT = 5000 # 사용할 포트 번호입니다.


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()


    sockets = [server_socket]
    readable = []
    writable = []
    for i in range(1000):
        readable, writable, exceptional = select.select(sockets, [], [])
        for s in readable:
            if s is server_socket:
                # 새로운 클라이언트 연결 요청을 수신합니다.
                client_socket, addr = server_socket.accept()
                sockets.append(client_socket)
            else:
                # 클라이언트로부터 데이터를 수신합니다.
                data = s.recv(1024)
                if not data:
                    # 클라이언트가 연결을 끊었습니다.
                    sockets.remove(s)
                    s.close()
                else:
                    # 클라이언트로부터 수신한 데이터를 다시 클라이언트에게 보냅니다.
                    writable.append(s)
        for s in writable:
            s.sendall(data)
            writable.remove(s)


    """ 이 예제에서는 select.select() 함수를 사용하여 읽기 가능한 소켓을 선택하고, 
    선택된 소켓에서 데이터를 수신합니다. 
    수신한 데이터를 다시 클라이언트에게 보내기 위해 쓰기 가능한 소켓을 선택하고, 
    sendall() 함수를 사용하여 데이터를 보냅니다.
    """


""" selectors 모듈은 파이썬 3.4부터 추가된 모듈로, 
select 모듈과 비슷한 기능을 제공하지만 
select를 확장하여 "고수준I/O멀티플랙싱"을 가능하도록 하고, 
더 직관적이고 간단하게 다중 I/O를 구현할 수 있도록 도와줍니다. 
selectors 모듈은 select 모듈과 달리 객체 지향적인 API를 제공합니다.
selectors 모듈은 다음과 같은 클래스를 제공합니다.


1. selectors.DefaultSelector: 
 - 시스템 기본 I/O 모델을 사용하는 Selector 객체를 생성합니다.
2. selectors.SelectSelector: 
 - select() 시스템 호출을 사용하는 Selector 객체를 생성합니다.
3. selectors.PollSelector: 
 - poll() 시스템 호출을 사용하는 Selector 객체를 생성합니다.
4. selectors.EpollSelector: 
 - epoll() 시스템 호출을 사용하는 Selector 객체를 생성합니다. 
 - 이 객체는 poll() 객체보다 더 높은 성능을 제공합니다.
5. selectors.DevpollSelector: 
 - /dev/poll 인터페이스를 사용하는 Selector 객체를 생성합니다. 
 - 이 객체는 Solaris에서 사용됩니다.
6. selectors.KqueueSelector: 
 - kqueue() 시스템 호출을 사용하는 Selector 객체를 생성합니다. 
 - 이 객체는 FreeBSD와 macOS에서 사용됩니다.
 """


# import signal
# import time
class signal_sapmle:
    """ signal 라이브러리는 파이썬에서 시그널(signal) 처리를 위해 제공되는 모듈입니다. 
    시그널은 프로그램 내부 또는 외부에서 발생한 이벤트를 의미하며, 
    예를 들어 Ctrl+C 키를 눌러서 프로그램을 강제 종료하는 것도 시그널 중 하나입니다.
    signal 라이브러리는 시그널 처리를 위한 다양한 함수와 상수를 제공합니다. 
    이를 통해 파이썬 프로그램에서 시그널을 처리하거나, 
    시그널을 보내는 등의 작업을 수행할 수 있습니다. 
    주요 함수로는 signal.signal(), signal.SIGINT 등이 있습니다.
    signal 라이브러리는 다양한 운영 체제에서 사용할 수 있으며, 
    특히 UNIX 계열 운영 체제에서 많이 사용됩니다. 
    이 라이브러리를 사용하면 프로그램이 예기치 않게 종료되는 상황을 예방하고, 
    프로그램이 안전하게 종료될 수 있도록 처리할 수 있습니다.
    """


    # 시그널 핸들러 함수 정의
    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        exit(0)


    # SIGINT 시그널에 대한 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)


    # 무한루프 실행
    for i in range(1000):
        print('Press Ctrl+C to exit...')
        time.sleep(1)


    """ 위 코드는 Ctrl+C를 눌러 프로그램을 종료하는 동작을 구현한 예제입니다. 
    signal_handler 함수는 Ctrl+C를 누르면 실행되는 함수로, 
    이 함수에서는 메시지를 출력하고 exit(0) 함수를 호출하여 프로그램을 종료합니다. 
    signal.signal 함수를 사용하여 SIGINT 시그널에 대한 핸들러 함수를 등록하고, 
    while 문 안에서 프로그램을 계속 실행합니다.
    프로그램을 실행하고 Ctrl+C를 누르면 "You pressed Ctrl+C!" 메시지가 출력되며 프로그램이 종료됩니다.
     """


class json_sample:
    """ json 라이브러리는 
    파이썬에서 JSON(JavaScript Object Notation) 데이터를 다룰 때 
    사용하는 라이브러리입니다. JSON은 데이터를 저장하거나 교환할 때 
    자주 사용되는 형식 중 하나로, 경량화되어 있어서 가벼우면서도 
    구조화된 데이터를 표현하기에 적합합니다.
    json 라이브러리는 다양한 함수와 클래스를 제공하며, 
    이를 사용하여 JSON 데이터를 파이썬 객체로 변환하거나, 
    파이썬 객체를 JSON 데이터로 변환하는 등의 작업을 수행할 수 있습니다. 
    주요 함수와 클래스로는 
    json.dumps(), 
    json.loads(), 
    json.dump(), 
    json.load() 등이 있습니다.
    간단한 예제를 통해 json 라이브러리의 사용법을 살펴보겠습니다.
    """


    # JSON 데이터
    json_data = '{"name": "John", "age": 30, "city": "New York"}'


    # JSON 데이터를 파이썬 객체로 변환
    python_obj = json.loads(json_data)


    # 파이썬 객체를 JSON 데이터로 변환
    json_str = json.dumps(python_obj)


    # 출력
    print(python_obj['name'])  # 'John'
    print(json_str)  # '{"name": "John", "age": 30, "city": "New York"}'


    """ 위 코드에서는 json_data 변수에 JSON 형식의 문자열을 저장하고, 
    json.loads 함수를 사용하여 파이썬 객체로 변환합니다. 
    이렇게 변환된 파이썬 객체는 딕셔너리 타입으로 저장되어 있으며, 
    키를 이용하여 값을 출력할 수 있습니다.
    그 다음에는 json.dumps 함수를 사용하여 파이썬 객체를 다시 
    JSON 형식의 문자열로 변환합니다. 이렇게 변환된 문자열은 json_str 변수에 저장되며, 
    이 문자열은 다시 파일에 저장하거나, 네트워크로 전송하는 등의 용도로 
    사용될 수 있습니다. 기본적으로 아스키 형태로 저장됩니다.
    json은 pickle, shelve 등과 비슷한 일을 하지만,
    딕셔너리, 리스트나 튜플 같은 자료형도 처리 가능합니다.
    """


class base64_sample:
    """ base64 라이브러리는 
    바이너리 데이터를 문자열 형태로 인코딩하거나, 
    (이때 인코딩한 문자열은 64개의 아스키 문자로 구성된다.(64진법))
    인코딩된 문자열을 다시 디코딩하는 기능을 제공하는 파이썬 내장 라이브러리입니다.
    base64 인코딩은 8비트 이상의 바이너리 데이터를 7비트 이하의 
    ASCII 문자로 변환하는 것을 의미합니다. 이를 통해 바이너리 데이터를 
    전자메일이나 HTTP 요청 등에서 전송하기 용이한 문자열 형태로 변환할 수 있습니다.
    base64 라이브러리는 다양한 함수를 제공합니다. 
    가장 많이 사용되는 함수는 
    base64.b64encode()와 base64.b64decode()입니다. 
    base64.b64encode() 함수는 바이너리 데이터를 base64 인코딩된 문자열로 변환하며, 
    base64.b64decode() 함수는 base64 인코딩된 문자열을 디코딩하여 
    원래의 바이너리 데이터로 변환합니다.
    간단한 예제를 통해 base64 라이브러리의 사용법을 살펴보겠습니다.
    """


    # 바이너리 데이터
    binary_data = b'Hello, World!'


    # base64 인코딩
    encoded_data = base64.b64encode(binary_data)


    # base64 디코딩
    decoded_data = base64.b64decode(encoded_data)


    # 출력
    print(encoded_data)  # b'SGVsbG8sIFdvcmxkIQ=='
    print(decoded_data)  # b'Hello, World!'


    """ 위 코드에서는 base64.b64encode() 함수를 사용하여 
    바이너리 데이터를 base64 인코딩된 문자열로 변환하고, 
    base64.b64decode() 함수를 사용하여 다시 디코딩하여 
    원래의 바이너리 데이터로 변환합니다. base64 인코딩된 문자열은 
    바이너리 데이터를 문자열 형태로 변환한 결과이므로, 
    이를 다른 곳에서 사용할 때는 다시 바이너리 데이터로 디코딩해야 합니다.
     """


class binascii_sample:
    """ binascii 라이브러리는 
    바이너리 데이터를 다양한 인코딩 형식으로 변환하는 기능을 제공하는 
    파이썬 내장 라이브러리입니다. 주요 기능으로는 
    16진수(hex), Base64, Uuencode, Binhex 등의 인코딩과 디코딩 함수가 있습니다.
    binascii 라이브러리는 다양한 함수를 제공합니다. 
    가장 많이 사용되는 함수로는 
    binascii.hexlify()와 binascii.unhexlify()가 있습니다. 
    binascii.hexlify() 함수는 바이너리 데이터를 16진수(hex) 문자열로 변환하며, 
    binascii.unhexlify() 함수는 16진수(hex) 문자열을 바이너리 데이터로 변환합니다.
    간단한 예제를 통해 binascii 라이브러리의 사용법을 살펴보겠습니다.
    """


    # 바이너리 데이터
    binary_data = b'Hello, World!'


    # 16진수(hex) 인코딩
    encoded_data = binascii.hexlify(binary_data)


    # 16진수(hex) 디코딩
    decoded_data = binascii.unhexlify(encoded_data)


    # 출력
    print(encoded_data)  # b'48656c6c6f2c20576f726c6421'
    print(decoded_data)  # b'Hello, World!'


    """ 위 코드에서는 binascii.hexlify() 함수를 사용하여 
    바이너리 데이터를 16진수(hex) 문자열로 변환하고, 
    binascii.unhexlify() 함수를 사용하여 다시 디코딩하여 
    원래의 바이너리 데이터로 변환합니다.
    16진수(hex) 문자열은 바이너리 데이터를 16진수 형태의 문자열로 변환한 결과이므로, 
    이를 다른 곳에서 사용할 때는 다시 바이너리 데이터로 디코딩해야 합니다.
    """


class quopri_sample:
    """ quopri 라이브러리는 
    인코딩된 문자열을 디코딩하거나, 문자열을 
    quoted-printable 형식으로 인코딩하는 기능을 제공하는 파이썬 내장 라이브러리입니다.
    Quoted-printable은 바이너리 데이터를 ASCII 문자로 변환하여 
    전송하기 위한 방법 중 하나입니다. 이 방법은 7비트 ASCII 문자만 사용 가능한 
    이메일 등에서 바이너리 데이터를 전송하기 위해 주로 사용됩니다. 
    이 방법은 ASCII 범위 내에 있는 문자는 그대로 사용하고, 
    범위를 벗어나는 문자는 '=' 기호와 16진수(hex) 형태로 변환하여 사용합니다.
    영문과 숫자 등의 ASCII 7bit 문자는 그대로 두고 한글 등 8bit 문자만 인코딩 합니다.
    quopri 라이브러리는 다양한 함수를 제공합니다. 
    가장 많이 사용되는 함수로는 
    quopri.encode()와 quopri.decode()가 있습니다. 
    quopri.encode() 함수는 문자열을 quoted-printable 형식으로 인코딩하며, 
    quopri.decode() 함수는 quoted-printable 형식의 문자열을 디코딩하여 
    원래의 문자열로 변환합니다.
    간단한 예제를 통해 quopri 라이브러리의 사용법을 살펴보겠습니다.
    """


    # 인코딩할 문자열
    string = '안녕하세요, 파이썬!'


    # quoted-printable 인코딩
    encoded_string = quopri.encodestring(string.encode()).decode()


    # quoted-printable 디코딩
    decoded_string = quopri.decodestring(encoded_string.encode()).decode()


    # 출력
    print(encoded_string)
    print(decoded_string)


    """ 위 코드에서는 quopri.encodestring() 함수를 사용하여 
    문자열을 quoted-printable 형식으로 인코딩하고, 
    quopri.decodestring() 함수를 사용하여 다시 디코딩하여 원래의 문자열로 변환합니다.
    quoted-printable 인코딩된 문자열은 문자열을 quoted-printable 형식으로 
    인코딩한 결과이므로, 이를 다른 곳에서 사용할 때는 다시 디코딩해야 합니다.
    """


class uu_sample:
    """ uu 라이브러리는 Unix to Unix 인코딩이라는 
    바이너리 데이터 인코딩 방식을 구현하는 파이썬 내장 라이브러리입니다. 
    이 방식은 이메일 등에서 바이너리 데이터를 전송하기 위해 주로 사용되었습니다. 
    uu 인코딩 방식은 바이너리 데이터를 ASCII 문자로 변환하고 이를 인코딩합니다. 
    uu 인코딩 방식은 Base64 인코딩 방식과 마찬가지로 바이너리 데이터를 
    ASCII 문자로 변환하는 방식입니다.
    1980년 메리 앤호튼이 개발. 지금은 대부분 uuencode의 단점을 보완한 
    Base64와 같은 MIME 방식의 인코딩을 사용합니다. 
    uu는 이러한 uuencode 인코딩을 위한 파이썬 모듈입니다.(begin ~ end로 구성됨)
    uu 라이브러리는 다양한 함수를 제공합니다. 
    가장 많이 사용되는 함수로는 uu.encode()와 uu.decode()가 있습니다. 
    uu.encode() 함수는 바이너리 데이터를 uu 인코딩 방식으로 인코딩하며, 
    uu.decode() 함수는 uu 인코딩 방식의 문자열을 디코딩하여 
    원래의 바이너리 데이터로 변환합니다.
    간단한 예제를 통해 uu 라이브러리의 사용법을 살펴보겠습니다.
    """


    # 인코딩할 파일
    filename = 'example.txt'


    # uu 인코딩
    with open(filename, 'rb') as f:
        encoded_data = uu.encode(f, filename)


    # uu 디코딩
    decoded_data = uu.decode(encoded_data)


    # 디코딩한 데이터를 파일로 저장
    with open('decoded_' + filename, 'wb') as f:
        f.write(decoded_data)


    # 출력
    print(encoded_data)


    """ 위 코드에서는 uu.encode() 함수를 사용하여 파일을 
    uu 인코딩 방식으로 인코딩하고, uu.decode() 함수를 사용하여 
    다시 디코딩하여 원래의 바이너리 데이터로 변환합니다. 
    마지막으로, 디코딩한 데이터를 파일로 저장합니다.
    uu 인코딩된 문자열은 바이너리 데이터를 uu 인코딩 방식으로 인코딩한 결과이므로, 
    이를 다른 곳에서 사용할 때는 다시 디코딩해야 합니다.
     """


""" html 라이브러리는 
HTML 문서를 파싱하고 생성하기 위한 파이썬 내장 라이브러리입니다. 
이 라이브러리를 사용하여 HTML 문서를 파싱하면 HTML 태그들을 객체로 표현하고, 
이를 이용하여 HTML 문서를 수정하거나 새로운 HTML 문서를 생성할 수 있습니다.
html 라이브러리는 다양한 함수와 클래스를 제공합니다. 
이 중에서도 가장 많이 사용되는 클래스는 HTMLParser 클래스입니다. 
이 클래스는 HTML 문서를 파싱하여 태그들을 객체로 생성합니다. 
이 클래스는 다음과 같은 메서드를 제공합니다.
handle_starttag(tag, attrs): 시작 태그를 처리하는 메서드
handle_endtag(tag): 끝 태그를 처리하는 메서드
handle_data(data): 데이터를 처리하는 메서드
간단한 예제를 통해 html 라이브러리의 사용법을 살펴보겠습니다.
"""


# HTML 문서
html_doc = """
<html>
    <head>
        <title>Test HTML</title>
    </head>
    <body>
        <h1>Test Heading</h1>
        <p>Test Paragraph.</p>
    </body>
</html>
"""


# HTML 파서 클래스
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("    attr:", attr)
    def handle_endtag(self, tag):
        print("End tag :", tag)
    def handle_data(self, data):
        print("Data    :", data)


# 파서 생성
parser = MyHTMLParser()


# HTML 문서 파싱
parser.feed(html_doc)


""" 위 코드에서는 HTML 문서를 파싱하는 MyHTMLParser 클래스를 만들고, 
이를 이용하여 HTML 문서를 파싱합니다. MyHTMLParser 클래스는 
HTMLParser 클래스를 상속받아 시작 태그, 끝 태그, 데이터를 처리하는 
메서드를 재정의합니다. 파서 생성 후, feed() 메서드를 호출하여 HTML 문서를 파싱합니다.
이 코드를 실행하면 HTML 문서에서 태그들을 파싱한 결과가 출력됩니다. 
이처럼 html 라이브러리를 사용하여 HTML 문서를 파싱하면 
HTML 태그들을 객체로 표현하고, 이를 이용하여 HTML 문서를 수정하거나 
새로운 HTML 문서를 생성할 수 있습니다.
"""


class xml_sample:
    """ xml.etree.ElementTree 라이브러리는 
    XML 문서를 파싱하고 생성하기 위한 파이썬 내장 라이브러리입니다. 
    이 라이브러리를 사용하여 XML 문서를 파싱하면 XML 요소들을 객체로 표현하고, 
    이를 이용하여 XML 문서를 수정하거나 새로운 XML 문서를 생성할 수 있습니다.
    xml.etree.ElementTree 라이브러리는 ElementTree 모듈과 
    Element 모듈로 구성되어 있습니다. ElementTree 모듈은 
    XML 문서를 읽고 쓰는데 사용되는 함수와 클래스를 제공하며, 
    Element 모듈은 XML 요소를 나타내는 클래스입니다.
    간단한 예제를 통해 xml.etree.ElementTree 라이브러리의 사용법을 살펴보겠습니다.
    """


    def __init__(self):
        # XML 문서
        self.xml_doc = """
        <catalog>
        <book id="bk001">
            <author>Writer</author>
            <title>The First Book</title>
            <genre>Fiction</genre>
            <price>44.95</price>
            <publish_date>2000-10-01</publish_date>
            <description>The first book in the catalog</description>
        </book>
        <book id="bk002">
            <author>Writer</author>
            <title>The Second Book</title>
            <genre>Non-Fiction</genre>
            <price>55.95</price>
            <publish_date>2001-09-15</publish_date>
            <description>The second book in the catalog</description>
        </book>
        </catalog>
        """


    def main(self):
        # XML 문서 파싱
        root = ET.fromstring(self.xml_doc)
        # XML 요소 탐색
        for book in root.findall('book'):
            book_id = book.get('id')
            author = book.find('author').text
            title = book.find('title').text
            genre = book.find('genre').text
            price = book.find('price').text
            publish_date = book.find('publish_date').text
            description = book.find('description').text
            # XML 요소 출력
            print(f"Book ID: {book_id}")
            print(f"Author: {author}")
            print(f"Title: {title}")
            print(f"Genre: {genre}")
            print(f"Price: {price}")
            print(f"Publish Date: {publish_date}")
            print(f"Description: {description}")


    """ 위 코드에서는 XML 문서를 파싱하여 ElementTree 객체를 생성합니다. 
    그리고, root.findall() 메서드를 이용하여 XML 문서에서 'book' 요소들을 찾아내고, 
    각 'book' 요소의 속성과 하위 요소들을 찾아내어 출력합니다.
    이처럼 xml.etree.ElementTree 라이브러리를 사용하여 XML 문서를 파싱하면 
    XML 요소들을 객체로 표현하고, 이를 이용하여 XML 문서를 수정하거나 
    새로운 XML 문서를 생성할 수 있습니다.
    """


def parse_sample():
    """ parse 라이브러리는 
    파이썬에서 문자열을 다룰 때 유용한 라이브러리 중 하나입니다. 
    parse 라이브러리를 사용하면 문자열에서 원하는 데이터를 추출하는 작업을 
    간단하게 수행할 수 있습니다. parse 라이브러리는 
    C언어의 scanf 함수와 유사한 방법으로 문자열을 해석하며, 
    중괄호({})를 사용하여 값을 추출합니다.
    간단한 예제를 통해 parse 라이브러리의 사용법을 살펴보겠습니다.
     """


    # 문자열
    string = 'Hello, World!'


    # 문자열 해석
    result = parse('{greeting}, {name}!', string)


    # 결과 출력
    print(result['greeting'])  # 'Hello'
    print(result['name'])  # 'World'


    """ 위 코드에서는 parse 함수를 사용하여 문자열에서 
    greeting과 name 값을 추출하였습니다. parse 함수의 
    첫 번째 인자는 추출하려는 값을 중괄호({})로 표시한 문자열, 
    두 번째 인자는 추출 대상이 되는 문자열입니다. 
    parse 함수는 문자열을 해석하여 추출한 값을 딕셔너리로 반환합니다.
    parse 라이브러리는 문자열의 패턴을 미리 정의해 놓은 템플릿을 사용하여 
    문자열을 해석할 수도 있습니다. 예를 들어, 날짜 형식의 문자열에서 
    연도, 월, 일을 추출하는 경우에는 다음과 같이 템플릿을 사용할 수 있습니다. """


    # 문자열
    string = '2023-04-11'


    # 템플릿
    template = '{year:d}-{month:d}-{day:d}'


    # 문자열 해석
    result = parse(template, string)


    # 결과 출력
    print(result['year'])  # 2023
    print(result['month'])  # 4
    print(result['day'])  # 11


    """ 위 코드에서는 parse 함수에 템플릿과 문자열을 전달하여 
    연도, 월, 일을 추출하였습니다. :d는 숫자를 의미하는 포맷 코드입니다. 
    parse 함수는 추출한 값을 딕셔너리로 반환합니다.
    parse 라이브러리를 사용하면 문자열에서 원하는 데이터를 쉽게 추출할 수 있으며, 
    템플릿을 사용하면 추출 대상의 패턴을 미리 정의하여 더욱 정확하게 추출할 수 있습니다.
     """



def webbrowser_sample():
    """ webbrowser 라이브러리는 
    파이썬에서 웹 브라우저를 제어하는 기능을 제공합니다. 
    이 라이브러리를 사용하면 파이썬 코드에서 웹 페이지를 열거나, 
    웹 페이지 검색 결과를 열거나, 웹 페이지를 새 창이나 새 탭으로 열거나, 
    현재 웹 브라우저를 제어하는 등의 작업을 수행할 수 있습니다.
    다음은 webbrowser 라이브러리의 간단한 예제입니다. 
    이 예제는 파이썬으로 구글 검색 결과를 새 창으로 열어주는 코드입니다.
    """


    search_query = 'python webbrowser'
    url = f'https://www.google.com/search?q={search_query}'
    webbrowser.open_new_tab(url)


    """ 이 예제에서 webbrowser.open_new_tab() 메서드를 사용하여 
    검색 결과를 새 창으로 엽니다. 이 메서드는 새 창 대신 새 탭을 열고 싶다면 
    webbrowser.open_new() 메서드를 사용할 수도 있습니다. 
    또한, 이 예제에서는 f-string을 사용하여 문자열을 조합하였습니다. 
    이를 사용하려면 파이썬 3.6 이상의 버전이 필요합니다.
     """


def cgi_sample():
    """ cgi 라이브러리는 
    파이썬에서 CGI(Common Gateway Interface) 프로그래밍을 할 때 사용되는 기능을 
    제공하는 라이브러리입니다. CGI는 웹 서버와 웹 애플리케이션 사이에서 
    정보를 주고받기 위한 표준 인터페이스입니다. 이를 이용해 파이썬으로 작성된 
    웹 애플리케이션을 웹 서버와 연동하여 동적인 웹 페이지를 생성할 수 있습니다.
    cgi 라이브러리를 사용하면 웹 서버에서 전달된 HTTP 요청을 파싱하고, 
    파라미터를 추출하며, HTML 문서를 생성하는 등의 작업을 수행할 수 있습니다.
    다음은 cgi 라이브러리를 사용한 간단한 예제입니다. 
    이 예제는 웹 페이지에 "Hello, World!"를 출력하는 간단한 CGI 스크립트입니다.
    """


    #!/usr/bin/env python
    print("Content-type: text/html")
    print("<html>")
    print("<head>")
    print("<title>Hello, World!</title>")
    print("</head>")
    print("<body>")
    print("<h1>Hello, World!</h1>")
    print("</body>")
    print("</html>")


    """ 위 코드에서 print("Content-type: text/html")는 
    HTTP 응답 헤더를 출력하고, print()는 HTTP 응답 헤더와 
    본문을 구분하는 빈 줄을 출력합니다. 이후에는 HTML 코드를 출력하여 
    "Hello, World!"를 출력하는 간단한 웹 페이지를 생성합니다.
    이 스크립트를 웹 서버에서 실행하면, 웹 서버가 클라이언트로부터 
    HTTP 요청을 받으면 이 스크립트를 실행하고, 출력한 결과를 
    HTTP 응답으로 전송합니다. 이를 통해 동적인 웹 페이지를 생성할 수 있습니다.
    """


def cgitb_sample():
    """ cgitb 라이브러리는 
    CGI 프로그램의 오류를 쉽게 파악하는 데 사용 합니다.
    파이썬에서 CGI(Common Gateway Interface) 프로그래밍을 할 때 발생하는 
    예외(Exception) 정보를 웹 브라우저에 표시하는 기능을 제공하는 라이브러리입니다. 
    예외가 발생하면 이를 처리하고, 웹 페이지에 디버그 정보를 
    표시하는 등의 작업을 수행할 수 있습니다.
    cgitb 라이브러리를 사용하면 웹 서버에서 발생한 예외 정보를 
    웹 페이지에 표시할 수 있습니다. 이를 통해 디버그 과정에서 예외 정보를 
    더 쉽게 확인하고, 문제를 해결할 수 있습니다.
    다음은 cgitb 라이브러리를 사용한 간단한 예제입니다. 
    이 예제는 cgitb 라이브러리를 사용하여 예외 정보를 웹 페이지에 
    출력하는 CGI 스크립트입니다.
    """


    #!/usr/bin/env python
    cgitb.enable()
    print("Content-type: text/html")
    print("<html>")
    print("<head>")
    print("<title>CGI Debugging Example</title>")
    print("</head>")
    print("<body>")
    try:
        raise Exception("Example exception")
    except Exception as e:
        cgitb.handler()
    print("</body>")
    print("</html>")


    """ 위 코드에서 cgitb.enable() 함수를 호출하여 cgitb 라이브러리를 활성화합니다. 
    그리고 try/except 구문을 사용하여 예외를 발생시키고, 
    cgitb.handler() 함수를 호출하여 예외 정보를 웹 페이지에 출력합니다. 
    이후에는 HTML 코드를 출력하여 웹 페이지를 생성합니다.
    이 스크립트를 웹 서버에서 실행하면, 예외가 발생하면 
    cgitb.handler() 함수가 호출되어 예외 정보를 웹 페이지에 출력합니다. 
    이를 통해 디버그 과정에서 예외 정보를 더 쉽게 확인할 수 있습니다.
     """


""" WSGI(Web Sever Gateway Interface)는 
웹 서버 소프트웨어와 파이썬으로 만든 웹 응용 프로그램 간의 
표준 인터페이스이다. 쉽게 말해 웹 서버가 클라이언트로부터 받은 요청을 
파이썬 애플리케이션에 전달하여 실행하고, 그 실행 결과를 돌려 받기 위한 약속이다.
 """


#!/usr/bin/env python
def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    result = [
        b"""<html><head><title>Hello, World!</title></head>
        <body><h1>Hello, World!</h1></body></html>"""
        ]
    return result
httpd = make_server('', 8000, app)
print("Serving on port 8000...")
httpd.serve_forever()


""" 위 코드에서 make_server 함수를 사용하여 웹 서버를 생성합니다. 
그리고 app 함수를 작성하여 WSGI 애플리케이션을 정의합니다. app 함수는 
environ과 start_response 매개변수를 받아 HTTP 요청 정보를 처리하고, 
HTTP 응답 정보를 생성합니다. 이후에는 make_server 함수를 사용하여 
웹 서버를 시작합니다. 이 스크립트를 실행하면, 웹 서버가 8000번 포트에서 실행되고, 
클라이언트가 HTTP 요청을 보내면 app 함수가 이를 처리하고, 
HTTP 응답을 생성하여 클라이언트에게 전송합니다. 
이를 통해 동적인 웹 페이지를 생성할 수 있습니다.
 """


def urllib_sample():
    """ urllib 라이브러리는 
    Python에서 URL을 다루기 위한 라이브러리입니다. 이 라이브러리를 사용하면 
    HTTP, FTP 등의 프로토콜을 사용하여 데이터를 가져올 수 있습니다. 
    urllib 라이브러리에는 다음과 같은 모듈이 있습니다.


    urllib.request : URL을 열고 데이터를 가져올 수 있습니다.
    urllib.parse : URL 문자열을 분석하고 조작할 수 있습니다.
    urllib.error : urllib.request 모듈에서 발생한 예외를 처리합니다.
    urllib.robotparser : robots.txt 파일을 파싱하여 웹사이트 접근 규칙을 확인.
    urllib.request 모듈을 사용하면 다음과 같은 작업을 할 수 있습니다.


    URL 열기 : urlopen() 함수를 사용하여 URL을 열고 데이터를 가져올 수 있습니다.
    URL 다운로드 : urlretrieve() 함수를 사용하여 URL에서 파일을 다운로드할 수 있습니다.
    HTTP 요청 메서드 지정 : 
    - Request 클래스를 사용하여 HTTP 요청 메서드
    - (GET, POST, PUT, DELETE 등)를 지정할 수 있습니다.
    HTTP 요청 헤더 추가 : Request 클래스를 사용하여 HTTP 요청 헤더를 추가할 수 있습니다.
    POST 요청 보내기 : 
    - urlencode() 함수를 사용하여 POST 요청 본문 데이터를 인코딩하고, 
    - Request 클래스에서 data 매개변수로 전달하여 POST 요청을 보낼 수 있습니다.
    """


    url = 'https://www.example.com'
    response = urllib.request.urlopen(url)
    data = response.read()
    print(data)


    """ 위 예제에서는 urllib.request.urlopen() 함수를 사용하여 
    url에 해당하는 웹 페이지를 열고, response 객체를 반환합니다. 
    이후에 response.read() 함수를 사용하여 웹 페이지에서 읽어온 데이터를 
    data 변수에 저장하고 출력합니다.
    다음은 urllib.request 모듈을 사용하여 POST 요청을 보내는 예제입니다.
    """


    url = 'https://www.example.com'
    data = {'username': 'myusername', 'password': 'mypassword'}
    data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)


    """ 위 예제에서는 urllib.parse.urlencode() 함수를 사용하여 
    data 변수에 저장된 POST 요청 본문 데이터를 인코딩합니다. 
    이후에 urllib.request.Request() 함수를 사용하여 
    url에 POST 요청을 보내는 req 객체를 생성하고, 
    urllib.request.urlopen() 함수를 사용하여 req 객체에 
    해당하는 POST 요청을 보냅니다. 마지막으로 response.read() 함수를 사용하여 
    POST 요청에 대한 응답 데이터를 읽어옵니다.
     """


class http_client_sample:
    """ http.client는 웹 페이지를 저장하는 또 다른 방법이다. 
    하지만, http.client보다는 requests 모듈을 사용 하는 것이 좋다.
    이 라이브러리를 사용하면 HTTP 요청을 생성하고, 서버에 전송하고, 
    서버로부터 응답을 받을 수 있습니다.
    http.client 라이브러리에는 다음과 같은 클래스와 함수가 있습니다.

    
    1. http.client.HTTPConnection : HTTP 연결을 생성합니다.
    2. http.client.HTTPSConnection : HTTPS 연결을 생성합니다.
    3. http.client.HTTPResponse : HTTP 응답을 다룹니다.
    4. http.client.HTTPException : HTTP 예외를 처리합니다.
    5. http.client.HTTPMessage : HTTP 메시지를 다룹니다.
    6. http.client.parse_headers : HTTP 헤더를 파싱합니다.
    7. http.client.parse_keqv_list : 키-값 쌍으로 이루어진 리스트를 파싱합니다.
    8. http.client.responses : HTTP 상태 코드와 메시지를 매핑한 딕셔너리입니다.


    다음은 HTTP GET 요청을 보내고 응답을 받는 예제입니다.
     """
    

    def http_client_get_sample(self):
        conn = http.client.HTTPSConnection("www.example.com")
        conn.request("GET", "/")
        response = conn.getresponse()
        data = response.read()
        print(data.decode())
        conn.close()


    """ 위 예제에서는 http.client.HTTPSConnection() 함수를 사용하여 
    www.example.com에 HTTPS 연결을 생성합니다. 
    이후에 conn.request() 함수를 사용하여 GET 요청을 생성하고, 
    conn.getresponse() 함수를 사용하여 서버로부터의 응답을 받습니다. 
    응답 데이터는 response.read() 함수를 사용하여 읽어옵니다. 
    마지막으로 conn.close() 함수를 사용하여 연결을 닫습니다.


    다음은 HTTP POST 요청을 보내는 예제입니다.
    """


    def http_client_post_sample(self):
        data = {'username': 'myusername', 'password': 'mypassword'}
        data = json.dumps(data)

        headers = {'Content-type': 'application/json'}

        conn = http.client.HTTPSConnection("www.example.com")
        conn.request("POST", "/", data, headers)
        response = conn.getresponse()
        data = response.read()
        print(data.decode())
        conn.close()


    """ 위 예제에서는 json.dumps() 함수를 사용하여 
    POST 요청 본문 데이터를 JSON 형식으로 인코딩합니다. 
    이후에 headers 변수를 사용하여 Content-type을 application/json으로 설정하고, 
    conn.request() 함수를 사용하여 POST 요청을 생성합니다. 
    마지막으로 response.read() 함수를 사용하여 서버로부터의 응답을 읽어옵니다.
    """



def ftplib_sample():
    """ ftplib는 
    Python에서 FTP(파일 전송 프로토콜) 클라이언트를 구현하는 데 사용되는 
    표준 라이브러리입니다. 이 라이브러리는 FTP 서버와 상호 작용하여 
    파일을 전송하고 관리하는 기능을 제공합니다.
    ftplib는 FTP 서버와 통신하는 데 사용되는 기본적인 명령어를 지원하며, 
    이를 통해 파일을 업로드하거나 다운로드할 수 있습니다. 
    또한 디렉토리를 생성하고 삭제하거나 파일의 퍼미션(permission)을 변경하는 등의 
    작업도 수행할 수 있습니다.
    ftplib는 Python의 내장 라이브러리로 제공되므로 별도의 설치가 필요하지 않습니다. 
    FTP 클라이언트를 작성할 때 매우 유용한 도구입니다. 
    사용 방법에 대해서는 Python 공식 문서를 참고하시면 됩니다.
    """


    # FTP 서버에 로그인
    ftp = ftplib.FTP('ftp.example.com')
    ftp.login('username', 'password')


    # 업로드할 파일 경로
    local_path = '/path/to/local/file.txt'
    remote_path = '/path/to/remote/file.txt'


    # 파일 업로드
    with open(local_path, 'rb') as f:
        ftp.storbinary(f'STOR {remote_path}', f)


    # FTP 서버와 연결 종료
    ftp.quit()


    """ 위의 예제에서는 ftplib.FTP 클래스를 사용하여 FTP 서버에 로그인하고, 
    storbinary 메서드를 사용하여 지정한 로컬 파일을 원격지의 경로로 업로드합니다.
    with open 구문은 로컬 파일을 바이너리 모드로 열어 
    storbinary 메서드로 전달하는데 사용됩니다. 업로드 작업이 완료되면 
    ftp.quit() 메서드를 사용하여 FTP 서버와의 연결을 종료합니다.
    이 예제는 파일 업로드에 대한 기본적인 개념을 보여주는 것이며, 
    더 복잡한 작업을 수행하려면 더 많은 코드와 로직이 필요할 수 있습니다.
    """


def poplib_sample():
    """ poplib는 POP3 서버에 연결하여 받은 메일을 확인하는 데 사용하는 모듈.
    POP3는 널리 사용하긴 했지만, 오래된 방식이다. 
    메일 서버가 IMAP을 지원한다면 POP3 대신 IMAP을 사용하는 것이 좋다.
    poplib는 Python에서 POP3(프로토콜3) 이메일 서버에 접속하여 
    이메일을 가져오는 데 사용되는 표준 라이브러리입니다. 
    poplib를 사용하면 이메일 서버와 통신하고 이메일을 검색하고 다운로드할 수 있습니다.
    poplib를 사용하면 이메일을 다음과 같은 방식으로 다운로드할 수 있습니다.


    1. POP3 서버에 연결합니다.
    2. 사용자 이름과 비밀번호를 제공하여 로그인합니다.
    3. 이메일함을 선택합니다.
    4. 메일 개수를 가져옵니다.
    5. 개별 메일을 다운로드하고, 이를 원하는 형식으로 파싱합니다.
    6. POP3 서버와의 연결을 종료합니다.


    poplib는 Python의 내장 라이브러리로 제공되므로 별도의 설치가 필요하지 않습니다. 
    poplib를 사용하여 이메일을 가져오는 방법에 대해서는 Python 공식 문서를 참고.
    """


    # POP3 서버에 연결
    pop_conn = poplib.POP3_SSL('pop.example.com')
    pop_conn.user('username')
    pop_conn.pass_('password')


    # 이메일함 선택
    pop_conn.list()
    # 최신 이메일 가져오기
    mail = pop_conn.retr(1)


    # 이메일 파싱
    body = b'\n'.join(mail[1]).decode('utf-8')
    print(body)


    # POP3 서버와 연결 종료
    pop_conn.quit()


    """ 위의 예제에서는 poplib.POP3_SSL 클래스를 사용하여 
    POP3 서버에 SSL을 사용하여 연결하고, 
    user와 pass_ 메서드를 사용하여 사용자 이름과 비밀번호를 인증합니다.
    이어서 list 메서드를 사용하여 사용 가능한 이메일 리스트를 가져옵니다. 
    그 다음 retr 메서드를 사용하여 첫 번째 이메일을 다운로드하고, 
    가져온 이메일을 원하는 형식으로 파싱합니다.
    위 예제는 이메일을 가져오는 과정을 보여주는 간단한 예제이며, 
    이메일 헤더, 본문, 첨부 파일 등을 처리하려면 더 많은 코드와 로직이 필요할 수 있습니다.
    """



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


