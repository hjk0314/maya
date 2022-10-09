import csv
import configparser
import hashlib


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


# csv_Test()
# configparser_Test()
# hashlib_Test()


# 79 char line ================================================================
# 72 docstring or comments line ========================================


