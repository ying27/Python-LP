#!/usr/bin/python
import sys
from events import Events
from transports import Transport
from transports import Transports
import webbrowser

reload(sys)
sys.setdefaultencoding('utf-8')



if len(sys.argv) != 3:
    print 'Error passing arguments'
    print 'USAGE: pract.py "(' ')" "[\'peu\',\'transport\']"'
else:
    w = sys.argv[1]
    #e = "['peu','transport','bicing']"
    e = sys.argv[2]

    d = Events()
    print "Filtering events..."
    k = d.getEvents(w)
    if len(k) != 0:
        print "Getting nearest transport..."
        t = Transports(e)

        print "Generating the html file..."
        aux = '<!DOCTYPE html>\n<html>\n<body>\n\n<table style="width:75%" border="1" align="center" cellpadding="10" >\n'

        for i in k:
            aux = aux + '    <tr>\n'
            aux = aux + '        <td>'+i.tohtml()+'</td>\n'
            aux = aux + '        <td>'+(t.getTransports(i.lat,i.lon)).tohtml()+'</td>\n'

        aux = aux + '    </tr>\n</table>'
        aux = aux + '</body>\n</html>'

        f = open('output.html','w')

        f.write(aux)
        k = f.close()
        q = raw_input('Display the result in the browser? [Y/N]\n')
        if str(q).lower() == 'y': webbrowser.open('output.html')
    else: print 'No events found matching this request'
