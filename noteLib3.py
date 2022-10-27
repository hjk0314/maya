import asyncio
import base64
import binascii
import csv
import configparser
import hashlib
import hmac
import html
import json
import multiprocessing
import quopri
import sched
import secrets
import io
import select
import selectors
import signal
import socket
import ssl
import subprocess
import uu
# import argparse
# import logging


# csv
# 엑셀 파일 안에 쉼표가 있을 경우 split(',') 이것 사용은 위험하다.
def csv_Test():
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


# configparser
# ini 파일은 프로그램 정보를 저장하는 텍스트 문서이다.
'''파일명: ftp.ini
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
def configparser_Test():
    config = configparser.ConfigParser()
    config.read('C:/folder/ftp.ini')
    ftp2_port = config['FTP2']['PORT']
    print(ftp2_port) # 22221 출력


# hashlib
# hashlib은 MD5, SHA256 등의 알고리즘으로 문자열을 해싱한다.
# 해싱은 단방향 암호화 알고리즘이므로 원래의 문자열을 복구할 수는 없다.
def hashlib_Test():
    m = hashlib.sha256()
    m.update('Life is too short'.encode('utf-8'))
    m.update(', you need python.'.encode('utf-8'))
    # digest(): 바이트 문자열을 반환
    byteStr = m.digest()
    # hexdigest(): 바이트 문자열을 16진수로 반환
    hexaStr = m.hexdigest()
    print(byteStr)
    print(hexaStr)


# hmac: 메시지 변조를 확인할 수 있다.
# 비밀키가 있어야 한다.
def hmac_Test():
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


# secrets: 안전한 난수 발생
def secrets_Test():
    # 1바이트는 2개의 16진수 문자열로 반환되므로 (16)은 32자리 난수가 된다.
    key = secrets.token_hex(16)
    print(key)


# io.StringIO
# 문자열을 파일 객체처럼 다룰 수 있도록 하는 클래스이다.
class io_Test():
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


# argparse: 파이썬 스크립트의 명령행 옵션을 파싱할 때 사용하는 모듈
# python module.py -a 1 2 3 4 5
# python module.py --add 1 2 3 4 5


# logging: 로그를 파일로 출력할 때 사용하는 모듈
# getpass: 비밀번호를 입력할 때 화면에 노출하지 않도록 한다.
# curses: 터미널 그래픽 애플리케이션을 만들 때 사용.
# platform: 시스템 정보를 확인할 때 사용.
# ctypes: C로 작성한 라이브러리를 파이썬에서 사용.
# threading: 스레드를 이용하여 한 프로세스에서 2가지 이상의 일을 실행.
# multiprocessing: 멀티 프로세스를 활용하여, 2가지 이상의 일을 동시에 실행.
# concurrent.futures: 같은 규칙으로 threading과 multiprocessing을 더 쉽게 사용.
'''subprocess: 시스템 명령을 수행.
with open(r"C:\Users\jkhong\Desktop\file.txt", 'wb') as txt:
    out = subprocess.run(['cmd', '/c', 'dir'], capture_output=True)
    txt.write(out.stdout)
'''
# sched: 지정된 시간에 원하는 이벤트를 실행하게 해주는 이벤트 스케줄러이다.
# asyncio: 단일 스레드 작업을 병렬로 처리.
# socket: TCP 서버/클라이언트 프로그램을 작성할 때 사용.
# ssl: socket 모듈로 작성한 서버/클라이언트에 공개키 암호화 방식을 적용.
# select: socket 프로그래밍에서 "I/O멀티플랙싱"을 가능하게 하는 모듈.
'''selectors: select를 확장하여 "고수준I/O멀티플랙싱"을 가능하도록 한 모듈로, 
select 대신 사용하도록 권장하는 모듈이다.
'''
# signal: 특정 신호를 수신했을 때 사용자가 정의한 함수를 호출하도록 한다.
'''json: "json데이터"를 쉽게 처리. pickle, shelve 등과 비슷한 일을 한다. 
기본적으로 아스키 형태로 저장. 딕셔너리, 리스트나 튜플 같은 자료형도 처리 가능.
'''
'''base64: 바이너리 데이터를 문자열로 인코딩할 때 사용. 
이때 인코딩한 문자열은 64개의 아스키 문자로 구성된다.(64진법)
'''
# binascii: 문자열을 16진수로, 변환할 16진수를 다시 문자열로 변환한다.
'''quopri: quoted-printable 인코딩/디코딩을 할 때 사용하는 모듈.
영문과 숫자 등의 ASCII 7bit 문자는 그대로 두고 한글 등 8bit 문자만 인코딩.
quopri.decodestring('Python =EA=B3=B5=EB=B6=80').decode('utf-8')
'''
'''uu: 바이너리를 텍스트로 변환하기 위한 인코딩 방법. 
1980년 메리 앤호튼이 개발. uu는 Unix-to-Unix를 뜻함. 
지금은 대부분 uuencode의 단점을 보완한 Base64와 같은 MIME 방식의 인코딩을 사용. 
uu는 이러한 uuencode 인코딩을 위한 파이썬 모듈이다.(begin ~ end로 구성됨)
uu.encode('test.jpg', 'result.txt')
uu.decode('result.txt', 'test.jpg')
'''
'''html: HTML문자를 이스케이프 처리할 때 사용.
"&lt;script&gt;Hello&lt;/script&gt;"
<script>Hello</script>
'''
'''html.parser: HTML 문서를 파싱할 때 사용. 
예를 들어 <strong></strong>태그의 문자열을 찾아서 출력.
'''
# 79 char line ================================================================
# 72 docstring or comments line ========================================


