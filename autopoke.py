#!/usr/bin/

import urllib2, urllib
from bs4 import BeautifulSoup
import getpass
from cookielib import CookieJar
import time
import re

def getlsd(soup):
	return soup.find('input', {'name':'lsd'})['value']

def get_lgnrnd(soup):
	return soup.find('input', {'name':'lgnrnd'})['value']

def get_lgnjs(soup):
	return soup.find('input', {'id':'lgnjs'})['value']

def prepare_value():
	values = {
		'lsd': lsd,
		'lgnrnd':lgnrnd,
		'lgnjs':lgnjs,
		'email': email,
		'pass': pwd,
		'persistent':1,
		'default_persistent':1,
		'locale': 'en_US',
	}
	return values
if __name__ == "__main__":
	email = raw_input('FB Email: ')
	pwd = getpass.getpass()
	login_url = "https://www.facebook.com/login.php?login_attempt=1"

	cj = CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	
	response = opener.open(login_url)
	soup = BeautifulSoup(response.read())
	lsd = getlsd(soup)
	lgnrnd = get_lgnrnd(soup)
	lgnjs = get_lgnjs(soup)

	values = prepare_value()

	#print values #debugging

	print "\n\nStart login\n\n"
	
	params = urllib.urlencode(values)
	response = opener.open(login_url, params)
	soup = BeautifulSoup(response.read())
	div = soup.find('div', {'id':'pagelet_welcome_box'})
	if div != None:
		print "Login Success"

		#pollloop
		while True:
			print "start auto poking"
			poke_url = "https://www.facebook.com/pokes/"
			response = opener.open(poke_url)
			soup = BeautifulSoup(response.read())
			mls_all = soup.find_all('div', {'class':'mls'})
			for mls in mls_all:
				a = mls.find('a', {'class':'_42ft _4jy0 _4jy3 _4jy1 selected'})
				poke_action = a['ajaxify']
				regex = re.compile('suggestion_type')
				matcher = regex.search(poke_action)
				if matcher:
					print "suggestion, pass"
				else:
					base = "https://www.facebook.com"
					print "poking to action: " + base + poke_action
				
					opener.open(base + poke_action)
					print 'Done'
			print "All done, sleep"
			time.sleep(5)

	else:
		print "Login failed"
