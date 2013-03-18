whoisrecon
==========
"Whois RECON" leverages a Neo4j graph database in the expectation that the data will be visually rendered in a graph. In the current form, the program has the following capabilities:

1.Dynamically builds out a graph database based on user provided Whois searches or batch loaded searches

2.Dynamically creates relationships between database nodes based on shared Whois metadata and IP resolutions

3.Incorporates queries to the ISC DNSDB API (https://dnsdb-api.isc.org/)

4.Incorporates advanced Google searching for Open Source correlation

5.Renders the relationships via command line to the user for analytic correlation


Requirements:

1. Python 2.6/2.7

2. Neo4j Community Edition 1.8.1. If you would like to use our Remote database which is already populated with threat indicators, then please send a request to chall@wapacklabs.com. 

3. Py2neo (http://pypi.python.org/pypi/py2neo)

4. CentralOPS account for accessing Hexillion's Whois XML Web Service (http://centralops.net/co/?_body=order/). To use your account in the program just edit the following line in the file to include your username and password:

  file = urllib2.urlopen('http://hexillion.com/rf/xml/1.0/whois/?username=%YOUR USERNAME%&password=%YOUR PASSWORD%&query='+ (s))

  *Hexillion is recommended as the XML service. Other services use different formats and may not work correctly.

5. DNSDB API Key from ISC.org. To use your key, edit the dns.conf file:

  APIKEY=%YOUR KEY HERE%
  DNSDB_SERVER=https://dnsdb-api.isc.org
  LIMIT=50 
