#!/usr/bin/python
import csv
from math import radians, cos, sin, asin, sqrt

class Station:

    dist = 500

    def __init__(self, equipament, lat, lon):
        self.equipament = equipament
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return self.equipament

    def tostring(self):
        return self.equipament

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

    def __addStation(self, st):
        sta = Station(st[6], st[4], st[5])

        if 'fgc' in st[6].lower():
            self.fgc.append(sta)

        elif 'metro' in st[6].lower():
            self.metro.append(sta)

        elif 'tramvia' in st[6].lower():
            self.tram.append(sta)

        elif 'Day buses' in st[3]:
            self.busd.append(sta)

        elif 'Night buses' in st[3]:
            self.busn.append(sta)


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


    def __getNearestStations(self, aux, lat, lon):
        aux.sort(key=lambda tup: tup.getDist(lon,lat))
        return aux[:6]

    def getNearFGC(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.fgc)
        return self.__getNearestStations(aux, lat, lon)

    def getNearMetro(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.metro)
        return self.__getNearestStations(aux, lat, lon)

    def getNearTram(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.tram)
        return self.__getNearestStations(aux, lat, lon)

    def getNearBusDia(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.busd)
        return self.__getNearestStations(aux, lat, lon)

    def getNearBusNit(self, lat, lon):
        aux = filter(lambda x: x.isNear(lon,lat), self.busn)
        return self.__getNearestStations(aux, lat, lon)
