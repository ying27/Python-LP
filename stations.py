#!/usr/bin/python
import csv
from math import radians, cos, sin, asin, sqrt

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
