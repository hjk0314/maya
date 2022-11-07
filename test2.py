from xml.etree.ElementTree import Element, parse

# xml.etree.ElementTree는 XML 문서를 만들 때 사용.
# parse: XML 문서를 파싱하고 검색할 때도 사용.


import webbrowser
# 파이썬 프로그램에서 시스템 브라우저를 호출할 때 사용.


import cgi
# CGI 프로그램을 만드는 데 필요한 도구를 제공.


import cgitb
# cgitb는 CGI 프로그램의 오류를 쉽게 파악하는 데 사용.


import wsgiref
# wsgiref는 WSGI 프로그램을 만들 때 사용하는 모듈.
# 한마디로 웹 서버 응용 프로그램이다.
""" WSGI(Web Sever Gateway Interface)는 웹 서버 소프트웨어와 파이썬으로 
만든 웹 응용 프로그램 간의 표준 인터페이스이다. 쉽게 말해 
웹 서버가 클라이언트로부터 받은 요청을 파이썬 애플리케이션에 전달하여 실행하고, 
그 실행 결과를 돌려 받기 위한 약속이다. """


import urllib
# urllib은 URL을 읽고 분석할 때 사용하는 모듈.
# 웹 페이지를 저장할 수 있다.


import http.client
# http.client는 HTTP 프로토콜의 클라이언트 역할을 하는 모듈이다.
""" 웹 페이지를 저장하는 또 다른 방법이다. 하지만, 
http.client보다는 requests 모듈을 사용 하는 것이 좋다. """


import ftplib
# ftplib는 FTP 서버에 접속하여 파일을 내려받거나 올릴 때 사용하는 모듈.


import poplib
# poplib는 POP3 서버에 연결하여 받은 메일을 확인하는 데 사용하는 모듈.
""" POP3는 널리 사용하긴 했지만, 오래된 방식이다. 
메일 서버가 IMAP을 지원한다면 POP3 대신 IMAP을 사용하는 것이 좋다. """


import imaplib
# 수신한 이메일을 IMAP4로 확인한다.
# imaplib은 IMAP4 서버에 연결하여 메일을 확인할 때 사용하는 모듈.


import nntplib
# 최신 뉴스를 확인할 수 있다.
# nntplib는 뉴스 서버에 접속하여 뉴스 그룹의 글을 조회하거나 작성할 때 사용.


import smtplib
# 이메일을 보낼 때 사용하는 모듈.
# 파일 첨부도 가능하다.


import telnetlib
# 텔넷에 접속하여 작업 가능하다.
# 텔넷 서버에 접속하여 클라이언트 역할로 사용하는 모듈.


import uuid
# 고유한 식별자
# 네트워크상에서 중복되지 않는 고유한 식별자인 UUID를 생성할 때 사용.
""" UUID(Universally Unique IDentifier)는 
네트워크상에서 고유성을 보장하는 ID를 만들기 위한 표준 규약이다. 
UUID는 다음과 같이 32개의 16진수로 구성되며 5개의 그룹으로 표시 되고 
각 그룹은 붙임표(-)로 구분한다. """
# 280a8a4d-a27f-4d01-b031-2a003cc4c039
""" 적어도 서기 3400년까지는 같은 UUID가 생성될 수 없다고 한다. 
이러한 이유로 UUID를 데이터베이스의 프라이버리 키로 종종 사용한다. """


import socketserver
# 서버와 통신하는 게임을 만들 수 있다.
# 다양한 형태의 소켓 서버를 쉽게 구현하고자 할 때 사용하는 모듈.


import http.server
# 테스트용 HTTP 서버를 만들 수 있다.
# 테스트 등의 용도로 사용할 간단한 HTTP 서버를 구현하고자 사용.


import xmlrpc
# xmlrpc는 HTTP를 통한 간단하고 이식성 높은 원격 프로시저 호출 방법이다.
""" 2대의 컴퓨터 A, B가 있다. A 컴퓨터는 인터넷에 연결되었지만, 
B 컴퓨터는 인터넷에 연결 되지 않았다고 한다. 하지만, 
2대의 컴퓨터는 내부 네트워크로 연결되어 있어서 
A 컴퓨터와 B 컴퓨터 간의 통신은 가능하다고 한다. 이때 A 컴퓨터를 이용하여 
B 컴퓨터의 위키독스 특정 페이지 내용을 얻어 올 수 있다. """


import imghdr
# 어떤 유형의 이미지 파일인지를 판단할 수 있다.
""" >>> imghdr.what('C:/folder/file.png')
'png'
 """


import turtle
# 터틀 그래픽으로 그림을 그린다.
""" turtle은 아이들에게 프로그래밍을 소개할 때 자주 사용하는 도구로, 
1967년 월리 푸르지그, 시모어 페이퍼트, 신시아 솔로몬이 개발한 
로고 프로그래밍 언어의 일부이다. """


import cmd
# cmd는 사용자에게 익숙한 명령행 프로그램 작성을 돕는다.


import shlex
# 문장 분석
# 인용이나 강조를 포함한 문장을 분석할 때 사용.
""" >>> shlex.split('this is "a test"', posix=False)
['this', 'is', '"a test"']
 """


import tkinter
# 파이썬에서 Tcl/Tk 툴킷을 사용하는 데 필요한 인터페이스 모듈.
# Tcl은 파이썬과 같은 스크립트 언어이고, Tk는 Tcl을 위한 GUI 툴킷이다.


import unittest
# 작성한 코드를 단위 테스트할 때 사용.


import doctest
# 독스트링을(docstring)을 활용하여 예제를 간단하게 테스트하고자 사용.


import timeit
""" 함수의 실행 시간을 측정할 때 유용한 모듈.
>>> timeit.timeit("aFunction()", number=100, globals=globals())
>>> timeit.timeit("bFunction()", number=100, globals=globals())
 """


import pdb
# 파이썬 코드를 디버깅할 때 사용하는 모듈.


""" import sys.argv
매개변수를 전달하여 실행.
파이썬 스크립트로 전달한 명령행 매개변수를 처리할 때 사용.
 """


import dataclasses
# 객체를 출력하거나 비교.
# 데이터를 저장하는 용도의 데이터 클래스를 만들 때 사용하는 모듈.


import abc
# 반드시 메서드를 구현하도록 함.
# abc는 추상 클래스를 정의할 때 사용.


import atexit
# 프로그램 종료 시 특정 작업을 실행.
# atexit는 파이썬 프로그램을 종료할 때 특정 코드를 마지막으로 실행하고자 사용.


import traceback
# 오류 위치와 그 원인을 알려준다.
# 발생한 오류를 추적하고자 할 때 사용.


import typing
# 데이터 타입을 확인
# 다양한 타입 어노테이션을 위해 사용하는 모듈이다. 이 모듈은 3.5부터 사용 가능.


