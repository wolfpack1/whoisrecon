from xml.dom.minidom import parseString
from py2neo import neo4j, cypher
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

search = raw_input("Search Database: ")

whoisindex = graph_db.get_or_create_index(neo4j.Node, "whoisID")
allnodes = whoisindex.query("whoisID:*")

if len(search) < 3:
        print 'Please be more specific!'

else:#matches the search result and returns 25 matches
        sresults =[]
        for i in allnodes:
                try:
                        value1 = "{0}".format(i['whoisID'])
                except UnicodeEncodeError:
                        pass
                if search in value1:
                        sresults.append(value1)
        if len(sresults) > 25:
                list_to_print = sresults[:25]
                leftover = len(sresults) - 25
                for item in list_to_print:
                        print item
                print 'There are %d more matches in the database' % (leftover, )
        else:
                for item in sresults:
                        print item
