#!/usr/bin/python
from events import Events
from transports import Transport
from transports import Transports


q = "'horta'"
w = "('taller',['musica','pintura'])"

e = "['peu','transport','bicing']"

d = Events()
k = d.getEvents(q)

t = Transports(e)



for i in k:
    print '*Event*'
    print i
    print '*Transport*'
    aux = t.getTransports(i.lat,i.lon)
    print aux
    print '*****************************************'
