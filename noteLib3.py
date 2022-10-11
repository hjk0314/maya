import csv
import configparser
import hashlib
import hmac
import secrets
import io
import argparse


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


# csv_Test()
# configparser_Test()
# hashlib_Test()
# hmac_Test()
# secrets_Test()
# io_Test()


# 79 char line ================================================================
# 72 docstring or comments line ========================================


