#!/usr/bin/python
#######################################################
# Title: HTTP Metric transport for Graphite/Carbon
# Version: 0.02dev
# by : Tomas Dobrotka [ www.dobrotka.sk ]
# support: tomas@dobrotka.sk
#######################################################

############################################################
#  Uncoment and Change the SSL cert. Whenin real workd!    #
############################################################

#set the hostname and port of Carbon listener
HOST = '192.168.2.175'
PORT = 2003

IMPULSE_COUNTER_HOLDER={}

#set config for HTTP server
config = {
  'global' : {
    'server.socket_host' : '0.0.0.0',
    'server.socket_port' : 2008,
    'server.thread_pool' : 8,


#configure HTTPs
#    'server.ssl_module'            : 'pyopenssl',
#    'server.ssl_certificate'       : './ssl/server.crt',
#    'server.ssl_certificate_chain' : './ssl/server.pem',
#    'server.ssl_private_key'       : './ssl/server.key',
#    'request.error_response': 'return_error',
}
}

import cherrypy as http
import socket
import time
from threading import Thread
from time import sleep


class carbonhttp:

    @http.expose
    def feed(self,mpath="",mvalue="",mtimestamp=""):
	if mtimestamp=="":
	    mtimestamp=int(time.time())
	
	print "<<< [Metrics recieved] (mpath="+str(mpath)+",mvalue="+str(mvalue)+",mtimestamp="+str(mtimestamp)+") [host="+str(HOST)+",port="+str(PORT)+"]"

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	DATA=str(mpath)+" "+str(mvalue)+" "+str(mtimestamp)+"\n"
	s.send(DATA)
	s.close()
	
	return 'ok'


    @http.expose
    def imp(self,mpath="",mvalue=1):
	global IMPULSE_COUNTER_HOLDER
	try:
	    IMPULSE_COUNTER_HOLDER[str(mpath)]=IMPULSE_COUNTER_HOLDER[str(mpath)]+int(1)
	except KeyError:
	    IMPULSE_COUNTER_HOLDER[str(mpath)]=int(1)
	print "<<< [Impulse recieved] (mpath="+str(mpath)+",mvalue="+str(mvalue)+") "+"Value: "+mpath+"=" +str(IMPULSE_COUNTER_HOLDER[str(mpath)])

	return 'ok'

    @http.expose
    def index(self):
	return("")


def bacground_counter(period):
    tmp_period=period
    while 1:
	tmp_period=(int(tmp_period)-1)
	if (tmp_period==0):
	    tmp_period=period
    	    print ">>> [FLUSH Impulse Conuter Holders] ["+str(period)+" seconds]"
	    print "--------------"
	    for METRICS in IMPULSE_COUNTER_HOLDER:
		print str(METRICS)+"="+str(IMPULSE_COUNTER_HOLDER[METRICS])
	    print "--------------"
    	sleep(1)

if __name__ == "__main__":
    thread = Thread(target = bacground_counter, args = (10, ))
    thread.start()
#    thread.join()

#    http.config.update( {'server.socket_host':"0.0.0.0", 'server.socket_port':2008} )
    http.quickstart( carbonhttp(),'/',config)




