#!/usr/bin/python
'''
BetRef Information Gathering Tool
-
Igor M. Martins (r4msolo)
'''
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from random import randint
import urllib.parse
import argparse
import os.path
import socket
import time
import re

banner = '''\033[1;32m49 6E 66 6F 72 6D 61 74 69 6F 6E 47 61 74 68 65 72 69 6E 67 
\n
\t\033[1;32m██████╗ ███████╗████████╗\033[1;31m██████╗ ███████╗███████╗
\t\033[1;32m██╔══██╗██╔════╝╚══██╔══╝\033[1;31m██╔══██╗██╔════╝██╔════╝
\t\033[1;32m██████╔╝█████╗     ██║   \033[1;31m██████╔╝█████╗  █████╗  
\t\033[1;32m██╔══██╗██╔══╝     ██║   \033[1;31m██╔══██╗██╔══╝  ██╔══╝  
\t\033[1;32m██████╔╝███████╗   ██║   \033[1;31m██║  ██║███████╗██║     
\t\033[1;32m╚═════╝ ╚══════╝   ╚═╝   \033[1;31m╚═╝  ╚═╝╚══════╝╚═╝     

49 6E 66 6F 72 6D 61 74 69 6F 6E 47 61 74 68 65 72 69 6E 67 
\033[1;97m\n\t\t\t\t\tR4MSOLO\n[ ! ] Information Gathering\033[0;0m

'''

class BetRef():

	def requests(self,request):
		self.printDebug("function requests()")
		self.printDebug('REQUEST: '+request)

		user = 'betref'

		req = urlopen(Request('https://'+request,headers={'User-Agent': user}))
		return req

	def __init__(self):
		try:
			print(banner)
			self.parameters()
			address = args.address
			search = args.search
			extf = args.extf
			dork = args.dork

			if address and 'http' in address:
				address = address.replace('https://','')
				address = address.replace('http://','')
				if '/' in address:
					address = address[:-1]

			searchD = [address,search,extf,dork]
			
			count = 0
			for l in searchD:
				if not l:
					l = None
					count+=1

			if count == len(searchD):
				print('\n[!] No parameters found! Are you kidding me? usage: ./betref -h\n') 
			
			elif dork:
				dork = ' '.join(dork)
				self.filterResult('www.google.com/search?num={}&q={}'.format(args.num,dork.replace(' ','+')),'Google',str(dork))
			else:
				if address:
					self.getDNS(address)
					self.getRobots(address)
				if not address:
					print('\n\033[1;90m[!] No URL found, skipping...\033[0;0m')
				elif search:
					search = ' '.join(search)
				self.searchDorks(search,address,extf)

		except socket.gaierror:
			print("[!] No Connection")
			quit()
		except KeyboardInterrupt:
			self.printOutput("leaving applications...\n",3)

	def printOutput(self,output,sig):
		self.printDebug("function printOutput()")
		self.printDebug('output: '+str(output)+' | sig: '+str(sig))
		if args.filename != None:
			filename = args.filename
			if not os.path.exists(filename):
				print("[+] Creating a new report file => "+filename)
				report = open(filename,'+a')
				report.write(output+'\n')
				report.close()
			else:
				report = open(filename,'+a')
				report.write(output+'\n')
				report.close()
		
		if sig == 0:
			self.printDebug('sig 0: void')
		if sig == 1:
			self.printDebug("sig 1: green")
			print('\033[1;32m[+]',output,'\033[0;0m')
		elif sig == 2:
			self.printDebug("sig 2: links")
			print('	\033[1;36m',output,'\033[0;0m')
		elif sig == 3:
			self.printDebug("sig 3: errors")
			print('	\033[1;31m',output,'\033[0;0m')

	def printDebug(self,debug):
		if args.debug:
			print("DEBUG:",debug)

	def getDNS(self,address):
		self.printDebug("function getDNS()")
		try:
			ip = int(address.replace('.',''))
			address = address
			self.printDebug("[!] IPV4 Address")
			domain = socket.gethostbyaddr(str(address))
			result = str(address)+' <=> '+str(domain)

		except ValueError:
			self.printDebug("[!] IPV6 Address or Domain name")
			domain = socket.gethostbyname(address)
			result = str(address)+' <=> '+str(domain)
			self.domain = domain
		
		self.printDebug(result)
		self.printOutput(result,1)
	
	def getRobots(self,address):
		self.printDebug("function getRobots()")
		print('\033[1;33mGet robots.txt from\033[1;31m',address,'\033[0;0m')
		self.printDebug('[ROBOTS.TXT] '+address)
		
		try:
			validation = self.requests(f'www.google.com/search?q=site:{address}+inurl:robots.txt')
			address = address+'/robots.txt'
			validation = str(validation.readlines())
			if address in validation.split('href="/url?q=')[1].split('&')[0]:
				choice = input('\n\033[1;31mRobots file found by search engine, do you want to open it? Note: This action will create log on the server (y/N): \033[0;0m')
				if choice.upper() == 'N':
					return 0

			robot = self.requests(address)
			self.printOutput('======= ROBOTS =======\n'+address+'\n-\n',0)
			for l in robot.readlines():
				if 'sitemap.xml' in l.decode('utf-8'):
					print('\033[1;32m[+] Found',l.decode('utf-8'),'\033[0;0m')
				if 'Disallow: ' in l.decode('utf-8') and l.decode('utf-8').split('Disallow: ')[1] != '\n':
					self.printOutput(l.decode('utf-8').split('Disallow: ')[1],3)
				self.printOutput(l.decode('utf-8'),0)
			self.printOutput('='*42+'\n',0)
		
		except:
			self.printOutput('\n[!] robots.txt not found',3)

	def searchDorks(self,search,site,extf):
		self.printDebug("function searchDorks()")

		#add more engine here in the dict
		search_engine = {'Google':'www.google.com/search?num={}&q='.format(args.num)}
		gdorklist = ['inurl:','intitle:','intext:','cache:']
		
		if site:
			site = 'site:'+site
		if extf:
			extf = 'ext:'+extf
		
		for se in list(search_engine.keys()):
			
			engine = search_engine[se]

			print("\n\033[1;33m{0} Hacking:\n\033[0;0m".format(se))
			
			if se == 'Google':
				dorklist = gdorklist
				self.printDebug(dorklist)
			
			listD = [search,site,extf]
			searchD = list()
			for l in listD:
				if l != None:
					if l == listD[0]:
						l = '"'+str(l).replace(' ','+')+'"'
					searchD.append(l)

			if len(searchD) > 1:
				searchD = '+'.join(searchD)
				searchD = searchD.replace(' ','')

			self.printDebug("searchD: "+str(searchD))

			for d in dorklist:
				if search:
					dork = "{}{}{}".format(engine,d,searchD)
					self.filterResult(dork,se,d)
				else:
					dork = engine+''.join(searchD)
					self.filterResult(dork,se,d)
					break

	def filterResult(self,dork,se,d):
		print("\n\033[1;33m  Searching for\033[1;31m "+d+"\033[0;0m")
		req = self.requests(dork)
		count = 0
		if se == 'Google':
			try:
				msg = str(req.read()).split(" ")
				for l in msg:
					if 'href="/url?q=' in l:
						link = l.replace('href="/url?q=','Link: ')
						link = link.split('&')[0]
						if re.search("http",link) and not re.search('ServiceLogin',link) and not re.search('google',link):
							link = urllib.parse.unquote(link)
							self.printOutput(link,2)
							count+=1

				if count == 0:
					print('    \033[1;90m[!] Not Found\033[0;0m')
			except:
				print('[!] No response')

	def parameters(self):
		global args
		parser = argparse.ArgumentParser()
		parser.add_argument("-u", dest="address",action="store", help="domain address")
		parser.add_argument("-s", dest="search",nargs="+",action="store", help="search for keyword")
		parser.add_argument("-d", dest="dork",action="store",nargs="+", help="search for dorks")
		parser.add_argument("-e", dest="extf",action="store", help="search for files containing specified extension")
		parser.add_argument("-n", dest="num", action="store", help="number of searches")
		parser.add_argument("-o", dest="filename",action="store", help="writes the output to a report file")
		parser.add_argument("--debug", dest="debug", action="store_true")
		parser.set_defaults(proxy=None,debug=False,num=9)
		args = parser.parse_args()

if '__main__' == __name__:
	BetRef()
