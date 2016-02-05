# HTTP Metric transport for Graphite/Carbon

Python HTTP server that accept metric data via HTTP, and forwards it as raw data, to Graphite/Carbon (TCP port 2003).

Why to want send data via HTTP?
This method gives you some advantages over the RAW data sending:

* Send metric data via HTTP request (where netcat cant be used as client)
* Encryption (with HTTPS)
* Security ( Authentification *TODO)
* IP Restrictions on application level (*TODO)
* Anonymity (you see HTTP/HTTPS traffic and protocol)

#Requirements
* Python
* CherryPy

# usage:

First set the HOST/IP of the target carbon host in "carbon-http-srv.py"
RUN ./carbon-http-srv.py

Make HTTP GET request to feed carbon with metrics data.
Example: http://0.0.0.0:2008/feed/some-metrics/5/1444159516

RAW data are send to port 2003: as "some-metrics 5 1444159516"
If timestamp is not defined as part of URL, HTTP server uses the current local timestamp.

So you can feed the data without timestamp, like:
http://0.0.0.0:2008/feed/some-metrics/7

The example result is:
![example_result](https://raw.githubusercontent.com/ggtd/HTTP-Metric-transport-for-Graphite/master/img_for_readme/example_some-metric.png)


See also:
* http://graphite.wikidot.com/
* http://graphite.readthedocs.org/en/1.0/feeding-carbon.html

#Quit
ctrl+] Todo: (fix make normal quit)

#News

#ver 0.04 (5.2.2016)
New Feature: Can response with image. See (?output=img)

Updated: Proper usage of config HOST and PORT for HTTP

example: http://0.0.0.0:2008/tdiff/event_name/  ,Store time difference between two events(requests). Result metrics is in seconds.



#ver 0.03 (21.10.2015)
New Feature: Event Differential time
example: http://0.0.0.0:2008/tdiff/event_name/  ,Store time difference between two events(requests). Result metrics is in seconds.



#ver 0.02 (21.10.2015)
New Feature: Impulse counter (or Agregated conter)

Impulse Counter is a feature that let you count some event, rather then sending metric data value.
The counter will flush the counted(or agregated)  data values  and transport the metrics to Graphite/Carbon in preset time. (Default 60 seconds)

Example:
--------
Call this HTTP request 4x in a row.
http://0.0.0.0:2008/imp/counting_sheeps/1

Result:
-------
After a time period (default 1 minute) a metric called “counting_sheeps” with value 4 is pushed into Carbon. This way you can measure the number of events in a time frame, rather that store just metrics values.


Value Agregation Counter
It’s the same like “Impuse Counter”, but allows you also, to count/store agregated values from events.

Example:
-------
If you do two requests, within the same minute (period):

http://0.0.0.0:2008/imp/counting_sheeps/10

http://0.0.0.0:2008/imp/counting_sheeps/7

Result: On end of time period, the daemon sends counted/agregateda metric values to Carbon, called “counting_sheeps” with value 17.


Response with image:
--------------------
From Version 0.04, The server can response with blank GIF as HTTP response. This allows you to post metrics directly from HTML.
Adding and URL parameter ?output=img to HTTP request will make the server respond with 1x1 pixel GIF image.



#ver 0.00 - 0.01 (10.10.2015)
* Initial release
* HTTP Metric transport proxy for Carbon.


#TODO:
* To polish documentation and examples
* Authentification
* Re-think time preiod counting. Separate time for each object/event. ()
* API/GUI/Frontend Dashboard
* Verbosity options/settings or selection
* Add better login verbose/functions. Separate Loging to log files.
* Setting to ignore Zervo-Value impulse
* Self hosted usage-monitoring analys and graphing.


 
