#!/usr/bin/python
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
