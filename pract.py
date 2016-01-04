#!/usr/bin/python
# -*- coding: utf-8 -*-
from unicodedata import normalize
import unicodedata

#from events import Events

#d = Events()
#print str(type(d.getTree()))

def evalEntrada(entrada):
    ret = []
    if isinstance(entrada, list):
        #s'ha de complir alguna d'elles
        print entrada, "is a list"

        for i in entrada:
            evalEntrada(i)

    elif isinstance(entrada,tuple):
        #s'ha de complir tot
        print entrada, "is a tuple"

        for i in entrada:
            ret = evalEntrada(i)

            print ret

    else:
        #print entrada, "is a string"
        return ret.append(entrada)



def strip_accents(txt, codif='utf-8'):

    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

print strip_accents('Nadal als Museus: 'Mar de Nadal'')
