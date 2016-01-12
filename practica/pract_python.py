#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata
from unicodedata import normalize
from sets import Set
import requests
import xml.etree.ElementTree as ET
import csv
from math import radians, cos, sin, asin, sqrt
import sys
import webbrowser

reload(sys)
sys.setdefaultencoding('utf-8')

####Events related classes####

class Event:

    def plain(self,txt):
        i = txt.encode("utf-8")
        return normalize('NFKD', i.decode('utf-8')).encode('ASCII','ignore')

    def iden(self,i):
        if i is None:
            return ""
        return i

    def __init__(self, nom, lloc, barri, carrer, data,lon,lat):

        aux = nom + " " + lloc + " " + barri
        self.index = self.plain(aux.lower())
        self.nom = self.iden(nom)
        self.carrer = self.iden(carrer)
        self.data = self.iden(data)
        self.lon = self.iden(lon)
        self.lat = self.iden(lat)

    def itmatch(self,n):
        return (n in self.index)

    def tohtml(self):
        ret = '<b>Event:</b><br/>'
        ret = ret + self.plain(self.nom)
        ret = ret + '<br/><b>Carrer: </b>' + self.carrer
        ret = ret + '<br/><b>Data: </b>' +  self.data
        return ret

    def __str__(self):
        return self.plain(self.nom) + '\n['+self.lat+', '+self.lon+']'


class ParseEvents:
    __src = "http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199"

    def __xml2obj(self, act):
        nom = act.find('nom').text
        carrer = str(act.find('lloc_simple/adreca_simple/carrer').text) + ', ' + str(act.find('lloc_simple/adreca_simple/numero').text)
        data = act.find('data/data_proper_acte').text
        lloc = act.find('lloc_simple/nom').text
        barri = act.find('lloc_simple/adreca_simple/barri').text

        lat = act.find('lloc_simple/adreca_simple/coordenades/googleMaps').get('lat')
        lon = act.find('lloc_simple/adreca_simple/coordenades/googleMaps').get('lon')
        #print nom
        return Event(nom,lloc,barri,carrer,data,lon,lat)

    def __init__(self):
        self.events = Set()

        resp = requests.get(self.__src)
        msg = resp.content
        root = ET.fromstring(msg)
        #tree = ET.parse('bcn.xml')
        #root = tree.getroot()

        for act in root.findall('body/resultat/actes/acte'):
            lat = act.find('lloc_simple/adreca_simple/coordenades/googleMaps').get('lat')
            lon = act.find('lloc_simple/adreca_simple/coordenades/googleMaps').get('lon')
            if lat != ' ' and lon != ' ':
                self.events.add(self.__xml2obj(act))

    def filterEvents(self,n):
        l = Set(filter(lambda x: x.itmatch(n),self.events))
        #for i in l:
        #    print i
        return l

    def showEvents(self, n = None):
        if n is None:
            n = self.events

        for k in n:
            print k.tostring()


class Events:

    def __init__(self):
        self.pe = ParseEvents()

    def __evalEntrada(self,entrada):
        if isinstance(entrada, list):
            #s'ha de complir alguna d'elles
            ret = self.__evalEntrada(entrada[0])
            for i in entrada[1:]:
                ret = ret | self.__evalEntrada(i)
            return ret

        elif isinstance(entrada,tuple):
            #s'ha de complir tot
            ret = self.__evalEntrada(entrada[0])
            for i in entrada[1:]:
                ret = ret & self.__evalEntrada(i)
            return ret

        else:
            ret = self.pe.filterEvents(entrada)
            return ret

    def getEvents(self,entrada):
        h = self.__evalEntrada(eval(entrada))
        #self.pe.showEvents(h)
        return h

####Public transport stations related classes####

class Station:

    dist = 500

    def __init__(self, nom, lat, lon, linies, tipus):
        self.nom = nom
        self.lat = lat
        self.lon = lon
        self.linies = linies
        self.tipus = tipus

    def __str__(self):
        aux = self.linies
        ret = '[' + aux[0]
        for i in aux[1:]:
            ret = ret + ',' + str(i)
        ret = ret + ']'
        return '['+self.tipus+']'+ret+" "+ self.nom + '     ['+self.lat+', '+self.lon+']'

    def tostring(self):
        aux = self.linies
        ret = '[' + aux[0]
        for i in aux[1:]:
            ret = ret + ',' + str(i)
        ret = ret + ']'
        return '['+self.tipus+']'+ret+" "+ self.nom #+ '     ['+self.lat+', '+self.lon+']'

    def tohtml(self):
        aux = self.linies
        ret = '[<b>' + aux[0]
        for i in aux[1:]:
            ret = ret + ',' + str(i)
        ret = ret + '</b>]'
        if self.nom == 'BUS':
            return '[<b>'+self.tipus+'</b>]'+ret+" "+ self.nom + ' ' + '(Lat: '+self.lat+', Lon: '+self.lon+')'

        return '[<b>'+self.tipus+'</b>]'+ret+" "+ self.nom

    def __haversine(self, lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return abs(km*1000)

    def getDist(self,lon,lat):
        lat = float(lat)
        lon = float(lon)
        return self.__haversine(lon, lat, float(self.lon), float(self.lat))

    def isNear(self,lon,lat):
        lat = float(lat)
        lon = float(lon)
        return self.getDist(lon,lat) <= float(Station.dist)



class TransportTMB:
    filetrans = 'TRANSPORTS.csv'
    filebus = 'ESTACIONS_BUS.csv'

    def __readFromFile(self,filename):
        ifile  = open(filename, "rb")
        return csv.reader(ifile, delimiter=';')

    def __init__(self):
        self.fgc = []
        self.metro = []
        self.tram = []
        self.busd = []
        self.busn = []

        #parsing fgc, metro and tram
        reader = (self.__readFromFile(self.filetrans))
        next(reader)
        for row in reader:
            self.__addStation(row)

        #parsing day bus and night bus
        reader = (self.__readFromFile(self.filebus))
        next(reader)
        for row in reader:
            self.__addStation(row)

    def __addStation(self, st):

        if 'fgc' in st[6].lower():
            self.fgc.append(self.__parseTrans(st,'FGC'))

        elif 'metro' in st[6].lower():
            self.metro.append(self.__parseTrans(st,'Metro'))

        elif 'tramvia' in st[6].lower():
            self.tram.append(self.__parseTrans(st,'Tramvia'))

        elif 'Day buses' in st[3]:
            self.busd.append(self.__parseBus(st,'Bus Diurn'))

        elif 'Night buses' in st[3]:
            self.busn.append(self.__parseBus(st,'Bus Nocturn'))

    def __parseTrans(self, st, tipus):
        infl = st[6]
        if st[7] != '':
            infl = infl+','+st[7]
            if st[8] != '':
                infl = infl+','+st[8]

        sp = infl.split("-")
        if '(' in sp[0]:
            linies = sp[0]
            linies = linies[linies.index("(") + 1:linies.rindex(")")]
            linies = linies.split(",")
        else: linies = [sp[0]]

        return Station(sp[1].strip(), st[4], st[5], map(lambda x: x.strip(), linies), tipus)

    def __parseBus(self, st, tipus):
        infl = st[6]
        linies = infl.split("-")
        del linies[-2:]
        return Station('BUS', st[4], st[5], linies[1:], tipus)

    def __getNearestStations(self, aux, lat, lon):
        aux.sort(key=lambda tup: tup.getDist(lon,lat))

        ret = []
        linies = []

        for i in range(6):
            if len(aux) == 0: break
            linies = linies + aux[0].linies
            ret.append(aux[0])
            aux = filter(lambda x: any(g not in linies for g in x.linies), aux)

        return ret

    def __getNearFGC(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.fgc)
        return self.__getNearestStations(aux, lat, lon)

    def __getNearMetro(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.metro)
        return self.__getNearestStations(aux, lat, lon)

    def __getNearTram(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.tram)
        return self.__getNearestStations(aux, lat, lon)

    def __getNearBusDia(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.busd)
        return self.__getNearestStations(aux, lat, lon)

    def __getNearBusNit(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.busn)
        return self.__getNearestStations(aux, lat, lon)

    def getTransports(self, lat, lon):
        fgc = self.__getNearFGC(lat, lon)
        metro = self.__getNearMetro(lat,lon)
        tram = self.__getNearTram(lat,lon)
        busd = self.__getNearBusDia(lat,lon)
        busn = self.__getNearBusNit(lat,lon)

        ret = []
        i = 0
        while len(ret) < 6 and i < 6:
            if len(fgc) > i:
                ret.append(fgc[i])
            if len(metro) > i:
                ret.append(metro[i])
            if len(tram) > i:
                ret.append(tram[i])
            if len(busd) > i:
                ret.append(busd[i])
            if len(busn) > i:
                ret.append(busn[i])

            i = i + 1

        ret = ret[:6]
        ret.sort(key=lambda tup: tup.getDist(lon,lat))

        return ret

####Bicing related classes####

class Bicingst:
    dist = 500

    def __init__(self, carrer, lon, lat, slots, bikes):
        self.carrer = carrer
        self.lon = lon
        self.lat = lat
        self.slots = slots
        self.bikes = bikes

    def __str__(self):
        return self.carrer #+ '  ['+self.lat+', '+self.lon+']'

    def tostring(self):
        return self.carrer + '  ['+self.lat+', '+self.lon+']'

    def tohtml(self):
        return self.carrer


    def __haversine(self, lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return abs(km*1000)

    def getDist(self,lon,lat):
        lat = float(lat)
        lon = float(lon)
        return self.__haversine(lon, lat, float(self.lon), float(self.lat))

    def isNear(self,lon,lat):
        lat = float(lat)
        lon = float(lon)
        return self.getDist(lon,lat) <= float(Bicingst.dist)

    def hasBikes(self):
        return self.bikes > 0

    def hasSlots(self):
        return self.slots > 0


class Bicing:
    __src = "http://wservice.viabicing.cat/v1/getstations.php?v=1"

    def __xml2obj(self, act):
        lat = act.find('lat').text
        lon = act.find('long').text
        carrer = act.find('street').text
        slots = act.find('slots').text #lloc lliures
        bikes = act.find('bikes').text # bicis disponibles

        return Bicingst(carrer,lon,lat,slots,bikes)

    def __init__(self):
        self.stations = []
        resp = requests.get(self.__src)
        msg = resp.content
        root = ET.fromstring(msg)
        #tree = ET.parse('bicing.php')
        #root = tree.getroot()

        for act in root.findall('station'):
            self.stations.append(self.__xml2obj(act))


    def getNearBikes(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat) and x.hasBikes(), self.stations)
        aux.sort(key=lambda tup: tup.getDist(lon,lat))
        #for i in aux[:5]: print i
        return aux[:5]

    def getNearSlots(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat) and x.hasSlots(), self.stations)
        aux.sort(key=lambda tup: tup.getDist(lon,lat))
        #for i in aux[:5]: print i
        return aux[:5]

####Transports class####

class Transport:
    def __init__(self):
        self.bicingBikes = []
        self.bicingSlots = []
        self.tmb = []

    def hasBicing(self):
        return len(self.bicingBikes) != 0

    def hasTmb(self):
        return len(self.tmb) != 0

    def tohtml(self):
        ret = ""
        if self.hasBicing():
            ret = ret + 'BICING:<br/><b>Bikes:</b><br/>'
            for i in self.bicingBikes:
                ret = ret + '&nbsp;&nbsp;&nbsp;&nbsp;' + i.tohtml() + '<br/>'
            ret = ret + '<b>Slots:</b><br/>'
            for i in self.bicingSlots:
                ret = ret + '&nbsp;&nbsp;&nbsp;&nbsp;' + i.tohtml() + '<br/>'
        elif self.hasTmb():
            ret = ret + 'TMB:'
            for i in self.tmb:
                ret = ret + '<br/>' + i.tohtml()
        return ret

    def __str__(self):
        ret = ""
        if self.hasBicing():
            ret = ret + 'BICING:\nBikes:\n'
            for i in self.bicingBikes:
                ret = ret + '   ' + i.tostring() + '\n'
            ret = ret + 'Slots:\n'
            for i in self.bicingSlots:
                ret = ret + '   ' + i.tostring() + '\n'
        elif self.hasTmb():
            ret = ret + 'TMB:\n'
            for i in self.tmb:
                ret = ret + '   ' + i.tostring() + '\n'
        return ret

class Transports:

    def __init__(self, entrada):
        self.tmb = TransportTMB()
        self.bicing = Bicing()
        self.pref = eval(entrada)

    def getTransports(self, lat, lon):
        ret = Transport()

        for i in self.pref:
            if i != 'peu':
                if i == 'bicing':
                    ret.bicingBikes = self.bicing.getNearBikes(lat, lon)
                    ret.bicingSlots = self.bicing.getNearSlots(lat, lon)
                    if ret.hasBicing(): break
                else:
                    ret.tmb = self.tmb.getTransports(lat,lon)
                    if ret.hasTmb(): break
        return ret

####Main####

if len(sys.argv) != 3:
    print 'Error passing arguments'
    print 'USAGE: python pract_python.py "(\'musica\')" "[\'peu\',\'transport\']"'
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
