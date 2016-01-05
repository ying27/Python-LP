#!/usr/bin/python
from events import Events
from transports import Transport
from transports import Transports


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

q = "'horta'"
w = "('taller',['musica','pintura'])"

e = "['peu','transport','bicing']"
#e = "['peu','bicing']"


d = Events()
k = d.getEvents("'musica'")
t = Transports(e)

aux = '<!DOCTYPE html>\n<html>\n<body>\n\n<table style="width:75%" border="1" align="center" cellpadding="10" >\n'

for i in k:
    aux = aux + '    <tr>\n'
    aux = aux + '        <td>'+i.tohtml()+'</td>\n'
    aux = aux + '        <td>'+(t.getTransports(i.lat,i.lon)).tohtml()+'</td>\n'

aux = aux + '    </tr>\n</table>'
aux = aux + '</body>\n</html>'

f = open('output.html','w')

f.write(aux)
f.close()
