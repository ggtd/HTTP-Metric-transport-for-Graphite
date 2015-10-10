# HTTP Metric transport for Graphite/Carbon

Python HTTP server that accept metric data via HTTP, and forwards them as raw data, to Graphite/Carbon (TCP port 2003).

Why to want send data via HTTP?
This method gives you some advantages over the RAW data sending:

* Send metric data via HTTP request (where netcat cant be used as client)
* Encryption (with HTTPS)
* Security ( Authentification *TODO)
* IP Restrictions on application level (*TODO)
* Anonymity (you see HTTP/HTTPS traffic and protocol)

# usage:

Example HTTP GET Request takes 3 parametrs:

<metric path> <metric value> <metric timestamp>

Example: http://0.0.0.0:2008/feed/some-metrics/5/1444159516

RAW data are send to port 2003: as "some-metrics 5 1444159516"
If timestamp is not defined as part of URL, HTTP server uses the current local timestamp.

So you can feed the data without timestamp, like:
http://0.0.0.0:2008/feed/some-metrics/5



See also:
http://graphite.wikidot.com/
http://graphite.readthedocs.org/en/1.0/feeding-carbon.html
http://graphite.readthedocs.org/en/1.0/index.html

