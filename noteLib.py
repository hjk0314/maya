import textwrap
import re
import datetime
import calendar
import bisect
import enum
import math
import decimal


# re
data = '780314-1234567'
temp = re.compile('(\d{6})[-](\d{7})') # (...): grouping
# print(temp.sub('\g<1>-*******', data))


# textwrap
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
# print(wrapList)
# print(wrapFill)
# print(shorten)


# datetime
today = datetime.date.today()
year = today.year
mon = today.month
day = today.day
HJK = datetime.date(1978, 3, 14)
SYR = datetime.date(1991, 4, 12)
HSE = datetime.date(2020, 3, 30)
WED = datetime.date(2018, 10, 28)
THO = datetime.timedelta(days=1000)
# print(today)
# print(year)
# print(mon)
# print(day)
# print(today - HJK)
# print(today - SYR)
# print(today - HSE)
# print(today - WED)
# print(HSE + THO)


# calendar
if calendar.isleap(year):
    msg = 'It\'s a leap year.'
else:
    msg = 'It\'s not a leap year.'
# print(msg)


# bisect
result = []
scoreList = [33, 99, 77, 70, 89, 90, 100]
gradeList = [60, 70, 80, 90]
for i in scoreList:
    # bisect.bisect_left()
    idx = bisect.bisect(gradeList, i)
    # print(f'idx: {idx}')
    grade = 'FDCBA'[idx]
    result.append(grade)
bisect.insort(gradeList, 85) # insort()
# print(gradeList)
# print(result)


# enum
class Week(enum.IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
# print(Week.MONDAY.name)
# print(Week.MONDAY.value)


# math: gcd(), lcm()
# math: lcm() -> # python --ver 3.9
gcd = math.gcd(60, 100) # More than 3 parameters available in ver 3.9
isc = math.isclose(0.1 * 3, 0.3)
# print(gcd)
# print(isc)


# decimal
mul = decimal.Decimal('0.1') * 3
sum = decimal.Decimal('1.2') + decimal.Decimal('0.1')
flt = float(sum)
# print(mul)
# print(sum)
# print(flt)
# Don't use like below.
# decimal.Decimal('0.1') * 3.0


# 79 char line ================================================================
# 72 docstring or comments line ========================================




