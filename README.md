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

#News



#ver.02dev (21.10.2015)
New Feature: Impulse counter (or Agregated conter)

Impulse Counter is a feature that let you count some event, rather then sending metric data value.
The counter will flush the counted(or agregated)  data values  and transport the metrics to Graphite/Carbon in preset time. (Default 60 seconds)

Example:
Call this HTTP request 4x each minute.
http://127.0.0.1:2008/imp/counting_sheeps/1

Result:
Each minute a metric called “counting_sheeps” with value 4 is pushed into Carbon. This way you can measure the number of events in a time frame, rather that store just metrics values.


Value Agregation Counter
It’s the same like “Impuse Counter”, but allows you also to, count agregated values from events.

Example:
If you do thous two requests, within the same minute (period):
http://127.0.0.1:2008/imp/counting_sheeps/10
http://127.0.0.1:2008/imp/counting_sheeps/7

At the time HH:mm:00 time the daemon sends a metric to Carbon, called “counting_sheeps” with value 17.




