#!/usr/bin/python
'''
BetRef Information Gathering Tool
-
R4MSOLO
'''
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from random import randint
import urllib.parse
import argparse
import os.path
import socket
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
\033[1;97m\n\t\t\t\t\tgithub.com/r4msolo\n[ ! ] Information Gathering\033[0;0m

'''

class BetRef():
	
	def randomAgent(self):

		#add more user-agent here
		useragent = [
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/83.0.4103.116 Safari/537.36',
		'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
		'Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
		'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
		'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
		'Mozilla/5.0 (X11; U; OpenBSD sparc64; en-CA; rv:1.8.0.2) Gecko/20060429 Firefox/1.5.0.2',
		]
		
		random = randint(0,len(useragent)-1)
		user = useragent[random]
		return user
	
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

			if count == 4:
				print('\n[!] No parameters found! Are you kidding me? usage: ./betref -h\n') 
			elif searchD[3]:
				self.filterResult('www.google.com/search?num={}&q={}'.format(args.num,dork),'Google',str(dork))
			else:
				if address:
					self.getDNS(address)
					self.getRobots(address)
				else:
					print('\033[1;90m[!] No URL found, skipping...\n\033[0;0m')
				self.searchDorks(search,address,extf)

		except KeyboardInterrupt:
			self.printOutput("leaving...\n",3)

	def printOutput(self,output,sig):
		self.printDebug("function printOutput()")
		self.printDebug('output: '+str(output)+' | sig: '+str(sig))
		if args.filename != None:
			filename = args.filename
			if not os.path.exists(filename):
				print("[+] Creating a new report file => "+filename)
				report = open(filename,'+a')
				report.write(output+'\n')

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

	def requests(self,request):
		self.printDebug("function requests()")
		
		if args.useragent:
			user = self.randomAgent()
			self.printDebug("[!] Using random User-Agent: {0}".format(user))
		else:
			user = 'betref'

		try:
			req = urlopen(Request('https://'+request,headers={'User-Agent': user}))
			return req
		
		except:
			print('[!] Error with SSL certificate\n[!] Trying without ssl...')
			req = urlopen(Request('http://'+request,headers={'User-Agent': user}))
			return req

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
		
		address = address+'/robots.txt'
		robot = self.requests(address)
		self.printOutput('======= ROBOTS =======\n'+address+'\n-\n',0)
		
		try:
			for l in robot.readlines():
				if 'sitemap.xml' in l.decode('utf-8'):
					self.printOutput("sitemap found",1)
					print('\033[1;32m[+]',l.decode('utf-8'),'\033[0;0m')
				self.printOutput(l.decode('utf-8'),0)
		except:
			self.printOutput('[!] robots.txt not found',3)
		
		self.printOutput('='*42+'\n',0)
			
	def searchDorks(self,search,site,extf):
		self.printDebug("function searchDorks()")
		#add more engine here in the dict
		search_engine = {'Google':'www.google.com/search?num={}&q='.format(args.num)}
		
		gdorklist = ['inurl:','intitle:','intext:','cache:']
		
		if site:
			site = 'site:'+site
		if extf:
			extf = ' ext:'+extf
		
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
					searchD.append(l)

			if len(listD) > 1:
				searchD = '+'.join(searchD)	

			self.printDebug("searchD: "+searchD)

			for d in dorklist:

				if not search:
					if not extf:
						dork = "{}{}".format(engine,site)
					else:
						dork = "{}{}{}".format(engine,site,extf)
					self.filterResult(dork,se,d)
					break

				elif d in searchD:
					dork = "{}{}".format(engine,searchD)
				
				else:	
					dork = "{}{}{}".format(engine,d,searchD)
				
				self.filterResult(dork,se,d)

				
	def filterResult(self,dork,se,d):
		print("\n\033[1;33m  Searching for\033[1;31m "+d+"\033[0;0m")
		req = self.requests(dork.replace(' ','+'))
		count = 0
		if se == 'Google':
			msg = str(req.read()).split(" ")
			for l in msg:
				if 'href="/url?q=' in l:
					link = l.replace('href="/url?q=','Link: ')
					link = link.split('&')[0]
					if re.search("http",link) and not re.search('ServiceLogin',link) and not re.search('preferences',link):
						link = urllib.parse.unquote(link)
						self.printOutput(link,2)
						count+=1

			if count == 0:
				print('    \033[1;90m[!] Not Found\033[0;0m')

	def parameters(self):
		global args
		parser = argparse.ArgumentParser()
		parser.add_argument("-u", dest="address",action="store", help="address of target")
		parser.add_argument("-s", dest="search",action="store", help="search keywords")
		parser.add_argument("-d", dest="dork",action="store", help="search dorks")
		parser.add_argument("-e", dest="extf",action="store", help="search for files containing specified extension")
		parser.add_argument("-n", dest="num", action="store", help="number of searches")
		parser.add_argument("-o", dest="filename",action="store", help="writes the output to a report file")
		parser.add_argument("--random-agent", dest="useragent", action="store_true",help="random user-agent")
		parser.add_argument("--debug", dest="debug", action="store_true")
		parser.set_defaults(useragent=False,debug=False,num=9)
		args = parser.parse_args()

if '__main__' == __name__:
	BetRef()
