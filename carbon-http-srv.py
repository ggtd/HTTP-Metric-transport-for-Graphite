#!/usr/bin/python
#######################################################
# Title: HTTP Metric transport for Graphite/Carbon
# Version: 0.03
# by : Tomas Dobrotka [ www.dobrotka.sk ]
# support: tomas@dobrotka.sk
#######################################################

############################################################
#  Uncoment and Change the SSL cert. Whenin real workd!    #
############################################################

#set the hostname and port of Carbon listener
HOST = '0.0.0.0'
PORT = 3088

IMPULSE_COUNTER_HOLDER={}
TIME_DIFF_HOLDER={}


GIF_IMG_SOURCE='R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


#set config for HTTP server
config = {
  'global' : {
    'server.socket_host' : HOST,
    'server.socket_port' : PORT,
    'server.thread_pool' : 8,


    #configure HTTPs
    'server.ssl_module'            : 'pyopenssl',
    'server.ssl_certificate'       : './ssl/server.crt',
    'server.ssl_certificate_chain' : './ssl/server.pem',
    'server.ssl_private_key'       : './ssl/server.key',
    'request.error_response': 'return_error',
}
}

import cherrypy as http
import socket
import time
from threading import Thread
from time import sleep


def write_raw_metric(mpath,mvalue,mtimestamp):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	DATA=str(mpath)+" "+str(mvalue)+" "+str(mtimestamp)+"\n"
	s.send(DATA)
	s.close()
	print bcolors.OKGREEN+">>> [Metrics stored]"+bcolors.ENDC+" (mpath="+str(mpath)+",mvalue="+str(mvalue)+",mtimestamp="+str(mtimestamp)+") [host="+str(HOST)+",port="+str(PORT)+"]"
    

class carbonhttp:

    @http.expose
    def feed(self,mpath="",mvalue="",mtimestamp="",output=""):
	if mtimestamp=="":
	    mtimestamp=int(time.time())
	
	print "<<< [Metrics recieved] (mpath="+str(mpath)+",mvalue="+str(mvalue)+",mtimestamp="+str(mtimestamp)+")"
	write_raw_metric(mpath,mvalue,mtimestamp)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	DATA=str(mpath)+" "+str(mvalue)+" "+str(mtimestamp)+"\n"
	s.send(DATA)
	s.close()
	
	if output=="img":
	    http.response.headers['Content-Type'] = "image/gif"
	    return GIF_IMG_SOURCE.decode('base64')
	else:
	    return 'ok'


    @http.expose
    def imp(self,mpath="",mvalue=1,output=""):
	mtimestamp=int(time.time())
	global IMPULSE_COUNTER_HOLDER
	try:
	    IMPULSE_COUNTER_HOLDER[str(mpath)]=IMPULSE_COUNTER_HOLDER[str(mpath)]+int(1)
	except KeyError:
	    IMPULSE_COUNTER_HOLDER[str(mpath)]=int(1)
	print "\033[92m<<< [Impulse recieved] \033[0m (mpath="+str(mpath)+",mvalue="+str(mvalue)+") "+"Value: "+mpath+"=" +str(IMPULSE_COUNTER_HOLDER[str(mpath)])

	if output=="img":
	    http.response.headers['Content-Type'] = "image/gif"
	    return GIF_IMG_SOURCE.decode('base64')
	else:
	    return 'ok'

    @http.expose
    def tdiff(self,mpath="",output=""):
	mtimestamp=int(time.time())
	global TIME_DIFF_HOLDER
	try:
	    if TIME_DIFF_HOLDER[str(mpath)]<>"":
		DIFF=time.time()-TIME_DIFF_HOLDER[str(mpath)]
		TIME_DIFF_HOLDER[str(mpath)]=time.time()
		print "\033[92m<<< [Time Different event] \033[0m (mpath="+str(mpath)+",differential="+str(DIFF)+") "
		write_raw_metric(mpath,DIFF,mtimestamp)
	except KeyError:
	    TIME_DIFF_HOLDER[str(mpath)]=time.time()
	    print "\033[92m<<< [Time Different event] \033[0m (mpath="+str(mpath)+" - FIRST CHECKOPINT) "
	if output=="img":
	    http.response.headers['Content-Type'] = "image/gif"
	    return GIF_IMG_SOURCE.decode('base64')
	else:
	    return 'ok'


    @http.expose
    def index(self):
	return("")


def http_server():
    http.quickstart( carbonhttp(),'/',config)


def bacground_counter(period):
    tmp_period=period
    while 1:
	tmp_period=(int(tmp_period)-1)
	if (tmp_period==0):
	    tmp_period=period
	    mtimestamp=int(time.time())
	    print bcolors.OKGREEN+">>> --- Flushing Counters into Carbon host -----"+bcolors.ENDC
	    for METRICS in IMPULSE_COUNTER_HOLDER:
		write_raw_metric(METRICS,IMPULSE_COUNTER_HOLDER[METRICS],mtimestamp)
		IMPULSE_COUNTER_HOLDER[METRICS]=0
	    print bcolors.OKGREEN+"------------------------------------------------"+bcolors.ENDC
    	sleep(1)

if __name__ == "__main__":

    thread_counter = Thread(target = bacground_counter, args = (60, ))
    thread_counter.start()
    thread_http = Thread(target = http_server)
    thread_http.start()



