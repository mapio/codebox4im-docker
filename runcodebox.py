#!/bin/bash

from urllib2 import urlopen, URLError
from webbrowser import open as wopen
from sys import exit

BASE_URL = 'http://localhost:5000/'

try:
	uid_signature = urlopen( BASE_URL ).read()
except URLError:
	print "Il sistema non risulta disponibile."
	exit( 1 )

wopen( BASE_URL + uid_signature, 1 )
