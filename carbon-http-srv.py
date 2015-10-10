#!/usr/bin/python
#######################################################
# Title: HTTP Metric transport for Graphite/Carbon
# Version: 0.01
# by : Tomas Dobrotka [ www.dobrotka.sk ]
# support: tomas@dobrotka.sk
#######################################################

#######################################################
#    Change the SSL cert. wher using in real workd!   #
#######################################################

#set the hostname and port of Carbon listener
HOST = '192.168.2.175'
PORT = 2003

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

class carbonhttp:

    @http.expose
    def feed(self,mpath="",mvalue="",mtimestamp=""):
	if mtimestamp=="":
	    mtimestamp=int(time.time())
	
	print "Request recieved. (mpath="+str(mpath)+",mvalue="+str(mvalue)+",mtimestamp="+str(mtimestamp)+") [host="+str(HOST)+",port="+str(PORT)+"]"

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	DATA=str(mpath)+" "+str(mvalue)+" "+str(mtimestamp)+"\n"
	s.send(DATA)
	s.close()
	
	return 'ok'


    @http.expose
    def index(self):
	return("")


if __name__ == "__main__":
#    http.config.update( {'server.socket_host':"0.0.0.0", 'server.socket_port':2008} )
    http.quickstart( carbonhttp(),'/',config)




