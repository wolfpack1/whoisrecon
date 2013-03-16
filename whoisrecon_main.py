
"""

 _  _  _ _           _         ______                        
| || || | |         (_)       (_____ \                       
| || || | | _   ___  _  ___    _____) ) ____ ____ ___  ____  
| ||_|| | || \ / _ \| |/___)  (_____ ( / _  / ___/ _ \|  _ \ 
| |___| | | | | |_| | |___ |        | ( (/ ( (__| |_| | | | |
 \______|_| |_|\___/|_(___/         |_|\____\____\___/|_| |_|

    Copyright (C) 2013  Chris Hall chall@redskyalliance.org

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from xml.dom.minidom import parseString
from py2neo import neo4j, cypher
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
import re,sys
import socket, json
import urllib
from dnsdbclient import *
DEFAULT_DNSDB_SERVER = 'https://dnsdb-api.isc.org'
DEFAULT_LIMIT = 50

s = raw_input("Enter search term: ")
s = s.strip()
file = urllib2.urlopen('http://hexillion.com/rf/xml/1.0/whois/?username=%YOUR USERNAME%&password=%YOUR PASSWORD%&query='+ (s))
#file = open('yahoo.com.pro.xml', 'r')
data = file.read()
file.close()
dom = parseString(data)

conf = 'dns.conf'
cfg = parse_config(conf)
dns_server = DEFAULT_DNSDB_SERVER
limit = DEFAULT_LIMIT

if cfg.has_key('DNSDB_SERVER'):
    dns_server = cfg['DNSDB_SERVER']

if cfg.has_key('LIMIT'):
    limit = int(cfg['LIMIT'])


client = DnsdbClient(dns_server, cfg['APIKEY'],limit = limit, json = True)

try: # tries to get IP from domain
    e = socket.gethostbyname(s)
except socket.gaierror:
    e = 'exclude from list'

def search_is_domain(strg, search=re.compile(r"([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$", re.I).search):
    return bool(search(strg))

def search_is_IP(strg, search=re.compile(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", re.I).search):
    return bool(search(strg))

def find_email(searchtag, search = re.compile(r"(\b[a-z0-9]([a-z0-9\._%+\-]+)?(@|\[at\]|\[@\]|\(at\)|\(@\)|<at>|<@>)([a-zA-Z0-9][a-zA-Z0-9\-<>]+(\.|\[\.\]|\[dot\]|\(dot\)|\(\.\)|<dot>|<\.>))+((com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|(co\.uk))|(ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bl|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mf|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)|(ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bl|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mf|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)|(\[(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.|\[\.\]|\[dot\]|\(dot\)|\(\.\)|<dot>|<\.>)(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.|\[\.\]|\[dot\]|\(dot\)|\(\.\)|<dot>|<\.>)(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.|\[\.\]|\[dot\]|\(dot\)|\(\.\)|<dot>|<\.>)(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\]))\b)", re.I).search):
    m = search(searchtag)
    emailz = m.group()
    return emailz

def print_outgoing_relationships(node_list_value): #finds and prints OUTGOING relationships - limits results to 25
    i = whoisnodes[node_list_value]
    z = i.get_related_nodes(neo4j.Direction.OUTGOING, "links")
    rel_list = []
    for q in z:
        w = q.get_properties()
        whoisIDL = "{0}".format(w['whoisID'])
        rel_list.append(whoisIDL)
    if len(rel_list) > 25:
        print "======================================================================="
        print "{0}".format(i['whoisID'].upper()) + " has outgoing link(s) to the following nodes:"+"\n"
        amount_to_print = rel_list[:50]
        leftover = len(rel_list) - 50
        for item in amount_to_print:
            print item
        print 'There are %d more nodes in the database' % (leftover, )
    elif len(rel_list) == 1:
        pass
    elif len(rel_list) != 1:
        print "======================================================================="
        print "{0}".format(i['whoisID'].upper()) + " has outgoing link(s) to the following nodes:"+"\n"
        for item in rel_list:
            print item    


def print_incoming_relationships(node_list_value):# finds and prints INCOMING relationships - limits results to 25
    i = whoisnodes[node_list_value]
    z = i.get_related_nodes(neo4j.Direction.INCOMING, "links")
    rel_list = []
    for q in z:
        w = q.get_properties()
        whoisIDL = "{0}".format(w['whoisID'])
        rel_list.append(whoisIDL)
    if len(rel_list) > 50:
        print "======================================================================="
        print "{0}".format(i['whoisID'].upper()) + " has incoming link(s) to the following nodes:"+"\n"
        amount_to_print = rel_list[:50]
        leftover = len(rel_list) - 50
        for item in amount_to_print:
            print item
        print 'There are %d more nodes in the database' % (leftover, )
    elif len(rel_list) == 1:
        pass
    elif len(rel_list) != 1:
        print "======================================================================="
        print "{0}".format(i['whoisID'].upper()) + " has incoming link(s) to the following nodes:"+"\n"
        for item in rel_list:
            print item

def SearchGoogle(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  try:
      print 'Total results: %s' % data['cursor']['estimatedResultCount']
  except KeyError:
      pass
  hits = data['results']
  if len(hits) > 0:
      print 'Top %d hits:' % len(hits)
  else:
      print 'No hits found'
  for h in hits: print ' ', h['url']
  print 'For more results, see %s' % data['cursor']['moreResultsUrl']
  
        
def create_relationships_domainnode(domain_list): # Creates relationships from list of whois components - 7 is max list w/o IP, and 9 with IP
    if domain_list ==4 and e == 'exclude from list': #no IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)

    elif domain_list ==5 and e == 'exclude from list':#no IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        
    elif domain_list ==6 and e == 'exclude from list':#no IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)   

    elif domain_list ==7 and e == 'exclude from list':#no IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[0], "links", whoisnodes[6]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)   
        print_incoming_relationships(6)
        
    elif domain_list ==4 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[2], "links", whoisnodes[3]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)

    elif domain_list ==5 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[3], "links", whoisnodes[4]))  
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        
    elif domain_list ==6 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[4], "links", whoisnodes[5]))            
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)

    elif domain_list ==7 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[0], "links", whoisnodes[6]),
            (whoisnodes[5], "links", whoisnodes[6]))
            
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)
        print_incoming_relationships(6)

    elif domain_list ==8 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[0], "links", whoisnodes[6]),
            (whoisnodes[0], "links", whoisnodes[7]),
            (whoisnodes[6], "links", whoisnodes[7]))
            
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)
        print_incoming_relationships(6)
        print_incoming_relationships(7)

    elif domain_list ==8 and e == 'exclude from list': # no IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[0], "links", whoisnodes[6]),
            (whoisnodes[0], "links", whoisnodes[7]),
            (whoisnodes[6], "links", whoisnodes[7]))
            
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)
        print_incoming_relationships(6)
        print_incoming_relationships(7)

    elif domain_list ==9 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[0], "links", whoisnodes[6]),
            (whoisnodes[0], "links", whoisnodes[7]),
            (whoisnodes[0], "links", whoisnodes[8]),
            (whoisnodes[7], "links", whoisnodes[8]))
            
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)
        print_incoming_relationships(6)
        print_incoming_relationships(7)
        print_incoming_relationships(8)

    elif domain_list ==10 and e != 'exclude from list': # IP returned
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]),
            (whoisnodes[0], "links", whoisnodes[4]),
            (whoisnodes[0], "links", whoisnodes[5]),
            (whoisnodes[0], "links", whoisnodes[6]),
            (whoisnodes[0], "links", whoisnodes[7]),
            (whoisnodes[0], "links", whoisnodes[8]),
            (whoisnodes[0], "links", whoisnodes[9]),
            (whoisnodes[8], "links", whoisnodes[9]))
            
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)
        print_incoming_relationships(4)
        print_incoming_relationships(5)
        print_incoming_relationships(6)
        print_incoming_relationships(7)
        print_incoming_relationships(8)
        print_incoming_relationships(9)     

def create_relationships_ipnode(ip_list): # does the same thing as function create_relationships_domainnode except with IP data
    if ip_list ==2:
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
    elif ip_list ==3:
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
    elif ip_list ==4:
        rels1 = graph_db.get_or_create_relationships(
            (whoisnodes[0], "links", whoisnodes[1]),
            (whoisnodes[0], "links", whoisnodes[2]),
            (whoisnodes[0], "links", whoisnodes[3]))
        print_outgoing_relationships(0)
        print_incoming_relationships(1)
        print_incoming_relationships(2)
        print_incoming_relationships(3)

def build_nodeList_domain(data):# parses portions of whois records and appends to list for processing
    result = []
    result.append(s.lower())
    secondlevel = '.'.join(s.split('.')[-2:])
    subdomain = ()
    www = ()
    xmlEmail = ()
    if s != secondlevel:
        result.append(secondlevel.lower())
        subdomain = '.'.join(s.split('.')[:1])
        www = 'www'
    if subdomain != www:
        result.append(subdomain.lower())    
    if '</Name>' in data:
        xmlNameTag = dom.getElementsByTagName('Name')[0].toxml()
        xmlName=xmlNameTag.replace('<Name>','').replace('</Name>','')
        result.append(xmlName.lower())
    if '</NameServer>' in data:
        xmlNameServerTag = dom.getElementsByTagName('NameServer')[0].toxml()
        xmlNameServer=xmlNameServerTag.replace('<NameServer>','').replace('</NameServer>','')
        result.append(xmlNameServer.lower())    
    if '</Email>' in data:
        xmlEmailTag = dom.getElementsByTagName('Email')[0].toxml()
        xmlEmail=xmlEmailTag.replace('<Email>','').replace('</Email>','')
        if xmlEmail == '<Email/>' and '<RawText>' in data:
            xmlRawTag = dom.getElementsByTagName('RawText')[0].toxml()
            xmlRaw=xmlRawTag.replace('<RawText>','').replace('</RawText>','')
            xmlEmail = find_email(xmlRaw)
        result.append(xmlEmail.lower())
    if '</Email>' not in data and xmlEmail not in result:
        try:
            getemail = find_email(data)
            result.append(getemail)
        except AttributeError:
            pass        
    if '</Address>' in data:
        xmlAddressTag = dom.getElementsByTagName('Address')[0].toxml()
        xmlAddress = xmlAddressTag.replace('<Address>','').replace('</Address>','')
        result.append(xmlAddress.lower())
    if '<CreatedDate>' in data:
        xmlCreatedTag = dom.getElementsByTagName('CreatedDate')[0].toxml()
        xmlCreated = xmlCreatedTag.replace('<CreatedDate>','').replace('</CreatedDate>','')
        result.append(xmlCreated.lower()[:11])
    if e != 'exclude from list': #option to add IP and subnet if IP is returned
        result.append(e)
        subnetd= '.'.join(e.split('.')[:3]+['*'])
        result.append(subnetd)
    return result


def build_nodeList_IP(data): #Does same thing as function build_nodeList_domain -min list is 2, max is 4
    result = []
    result.append(s)
    subneti = '.'.join(s.split('.')[:3]+['*'])
    result.append(subneti)
    if '</Name>' in data:
        xmlNameTag = dom.getElementsByTagName('Name')[0].toxml()
        xmlName=xmlNameTag.replace('<Name>','').replace('</Name>','')
        result.append(xmlName.lower())
    if '</IPRange>' in data:
        IPRangeTag=dom.getElementsByTagName('IPRange')[0].toxml()
        IPRange=IPRangeTag.replace('<IPRange>','').replace('</IPRange>','')
        result.append(IPRange)    
    return result


def create_dnsdb_relations(node, node_list, is_incoming, extra_properties):
    
    
    whoisindex = graph_db.get_or_create_index(neo4j.Node, "whoisID")
    central_node = whoisindex.get_or_create("whoisID", node, {"whoisID": node})
    whoisnodes= []
    whoisnodes.append(central_node)            
    
    if is_incoming:
        for relation_node in node_list:                      
            rel_neo4j_node = whoisindex.get_or_create("whoisID", relation_node, {"whoisID": relation_node})
            for key,value in extra_properties.items():
                rel_neo4j_node[key] = value   
                         
            relation = graph_db.get_or_create_relationships(
                                                  (rel_neo4j_node,"links",central_node),
                                                 )
            whoisnodes.append(rel_neo4j_node)
    
    print_incoming_relationships(0)
    print "======================================================================="

if  '<RawText>' in data:
    xmlRawTag = dom.getElementsByTagName('RawText')[0].toxml()
    xmlRaw=xmlRawTag.replace('<RawText>','').replace('</RawText>','')
    print xmlRaw

if search_is_domain(s):
    nodez = build_nodeList_domain(data)
    nodezlength = len(nodez)
    whoisindex = graph_db.get_or_create_index(neo4j.Node, "whoisID")
    whoisnodes = []
    for word in nodez:
        whoisnodes.append(whoisindex.get_or_create("whoisID", word, {"whoisID": word}))
    create_relationships_domainnode(nodezlength)

elif search_is_IP(s):
    nodez = build_nodeList_IP(data)
    nodezlength = len(nodez)
    whoisindex = graph_db.get_or_create_index(neo4j.Node, "whoisID")
    whoisnodes = []
    for word in nodez:
        whoisnodes.append(whoisindex.get_or_create("whoisID", word, {"whoisID": word}))
    create_relationships_ipnode(nodezlength)
    
result = None
rdata = True
if search_is_domain(s):    
    result = client.query_rrset(s)    
elif search_is_IP(s):    
    result = client.query_rdata_ip(s)
    rdata = False
    
else:
    print "the input is not recognized as either a domain or an IP: " + str(s)
    sys.exit(1)

rlist = []


for r in result:
    data = json.loads(r)    
    if rdata:         
        result = data['rdata']
    else:    
        if data.has_key('rrtype') and data['rrtype'].upper() == 'A':               
            result = data['rrname'] # only capturing the A records            
    if isinstance(result,list): 
        rlist += result
    else:
        rlist.append(result)

rlist = list(set(rlist)) # to get the unique nodes for DNDDB data lists

prlist = []

for rword in rlist: #reformats items with period appended and makes sure IPs are added
    if rword.endswith("."):
        prlist.append(rword.rsplit('.', 1)[0])
    else:
        prlist.append(rword)
    if search_is_IP(rword):
        prlist.append(rword)


if rdata:
    extra_data = "DNSDB Rdata"
else:
    extra_data = "DNSDB RRset"
    
create_dnsdb_relations(s,prlist, True, {'extra': extra_data})

print "========================OPEN SOURCE HITS==============================="

qsearch = '"' + (s) + '"'
googsearch = (qsearch) + ' malware'

SearchGoogle((googsearch))


















