import time
import textwrap
import re
import datetime
import calendar
import bisect
import enum
import math
import decimal
import fractions
import random
import statistics
import itertools
import functools
import operator


# re
def re_Test():
    data = '780314-1234567'
    temp = re.compile('(\d{6})[-](\d{7})') # (...): grouping
    print(temp.sub('\g<1>-*******', data))


# textwrap
def textwrap_Test():
    longStr = '''We are not now that strength which in old days 
    Moved earth and heaven; that which we are, we are; 
    One equal temper of heroic hearts, 
    Made weak by time and fate, but strong in will 
    To strive, to seek, to find, and not to yield.
    '''
    author = 'Alfred Lord Tennyson'
    shorten = textwrap.shorten(longStr, width=15, placeholder='...')
    wrapList = textwrap.wrap(longStr, width=30)
    wrapFill = textwrap.fill(longStr, width=45)
    print(wrapList)
    print(wrapFill)
    print(shorten)


# datetime
def datetime_Test():
    today = datetime.date.today()
    year = today.year
    mon = today.month
    day = today.day
    HJK = datetime.date(1978, 3, 14)
    SYR = datetime.date(1991, 4, 12)
    HSE = datetime.date(2020, 3, 30)
    WED = datetime.date(2018, 10, 28)
    THO = datetime.timedelta(days=1000)
    print(today)
    print(year)
    print(mon)
    print(day)
    print(today - HJK)
    print(today - SYR)
    print(today - HSE)
    print(today - WED)
    print(HSE + THO)


# calendar
def calendar_Test():
    curr = datetime.date.today()
    year = curr.year
    if calendar.isleap(year):
        msg = 'It\'s a leap year.'
    else:
        msg = 'It\'s not a leap year.'
    print(msg)


# bisect
def bisect_Test():
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


# enum
class Week(enum.IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


# math
# gcd(): 3개 이상의 최대공약수를 구하는 것은 파이썬 ver 3.9 에서 가능
# lcm(): 3개 이상의 최소공배수를 구하는 것은 파이썬 ver 3.9 에서 가능
def math_Test():
    gcd = math.gcd(60, 100)
    isc = math.isclose(0.1 * 3, 0.3)
    print(gcd)
    print(isc)


# decimal
def decimal_Test():
    mul = decimal.Decimal('0.1') * 3
    sum = decimal.Decimal('1.2') + decimal.Decimal('0.1')
    flt = float(sum)
    print(mul)
    print(sum)
    print(flt)
    # 아래와 같이 사용하면 안된다. 곱하는 수는 정수여야 함.
    # decimal.Decimal('0.1') * 3.0


# fractions
def fractions_Test():
    A = fractions.Fraction(1, 5)
    A = fractions.Fraction('1/5')
    B = fractions.Fraction(2, 5)
    print(A)
    print(B)
    print(A.numerator)
    print(A.denominator)
    print(A + B)
    print(float(A + B))


# random
def random_Test():
    numList = [1, 2, 3, 4, 5]
    a = random.randint(1, 45)
    b = random.shuffle(numList)
    c = random.choice(numList)
    print(a)
    print(numList)
    print(c)


# statistics
def statistics_Test():
    scoreList = [78, 93, 99, 95, 51, 71, 52, 43, 81, 78]
    A = statistics.mean(scoreList)
    B = statistics.median(scoreList)
    print(A)
    print(B)


# itertools
def itertools_Test():
    # cycle
    nameList = ['kim', 'lee', 'hong']
    cyl = itertools.cycle(nameList)
    print(next(cyl), next(cyl), next(cyl), next(cyl))
    # accumulate
    saleList = [
        1161, 1814, 1270, 2256, 1413, 1842, 
        2221, 2207, 2450, 2823, 2540, 2134
        ]
    result = itertools.accumulate(saleList)
    result = list(result)
    print(result)
    result = itertools.accumulate(saleList, max)
    result = list(result)
    print(result)
    # groupby
    # zip_longest
    student = ['kim', 'lee', 'hong', 'han', 'choi']
    rewards = ['candy', 'jelly', 'chocolate']
    result = zip(student, rewards)
    result = list(result)
    print(result)
    result = itertools.zip_longest(student, rewards, fillvalue='caramel')
    result = list(result)
    print(result)
    # permutatins
    numList = ['1', '2', '3']
    result = itertools.permutations(numList, 2)
    result = list(result)
    print(result)
    # combinations
    # result = len(list(itertools.combinations(range(1, 46), 6)))
    result = itertools.combinations(numList, 2)
    result = list(result)
    print(result)


# functools.lru_cache
# 함수의 반환 결과를 캐시하는 데코레이터이다.
# 사용법: @functools.lru_cache(maxsize=32)


# functools.partial
# 하나 또는 그 이상의 매개 변수를 포함한 채로 새로운 함수를 만든다.
class partial_Test():
    def __init__(self):
        self.usage()


    # Example functions
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


    # cal('add', 1, 2, 3) -> Use it like below.
    def usage(self):
        add = functools.partial(self.cal, 'add')
        mul = functools.partial(self.cal, 'mul')
        print(add(1, 2, 3))
        print(mul(4, 5, 6))
        print(add.func, add.args)
        print(mul.func, mul.args)


# functools.reduce
def reduce_Test():
    data = [1, 2, 3, 4, 5]
    result = functools.reduce(lambda x, y: x + y, data)
    # ((((1 + 2) + 3) + 4) + 5)
    print(result)


# functools.wraps
class wraps_Test():
    def __init__(self):
        result = self.add(1, 2)
        print(result)
        help(self.add)


    def elapsed(original_func):
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
    def add(self, num1, num2):
        '''Function that returns the sum.'''
        result = num1 + num2
        return result


# operator.itemgetter
def itemgetter_Test():
    '''sorted와 같은 함수의 key 매개변수에 적용'''
    students = [
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


# textwrap_Test()
# re_Test()
# datetime_Test()
# calendar_Test()
# bisect_Test()
# print(Week.MONDAY.name)
# print(Week.MONDAY.value)
# math_Test()
# decimal_Test()
# fractions_Test()
# random_Test()
# statistics_Test()
# itertools_Test()
# partial_Test()
# reduce_Test()
# wraps_Test()
# itemgetter_Test()


# 79 char line ================================================================
# 72 docstring or comments line ========================================


