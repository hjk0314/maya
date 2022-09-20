import textwrap
import re
import datetime
import calendar


# re
data = '780314-1234567'
temp = re.compile('(\d{6})[-](\d{7})') # (...): grouping
print(temp.sub('\g<1>-*******', data))


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
print(wrapList)
print(wrapFill)
print(shorten)


# datetime
today = datetime.date.today(); print(today)
year = today.year; print(year)
mon = today.month; print(mon)
day = today.day; print(day)
HJK = datetime.date(1978, 3, 14); print(today - HJK)
SYR = datetime.date(1991, 4, 12); print(today - SYR)
HSE = datetime.date(2020, 3, 30); print(today - HSE)
WED = datetime.date(2018, 10, 28); print(today - WED)
THO = datetime.timedelta(days=1000); print(HSE + THO)


# calendar
if calendar.isleap(year):
    print('It\'s a leap year.')
else:
    print('It\'s not a leap year.')


# 79 char line ================================================================
# 72 docstring or comments line ========================================


