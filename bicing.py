#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import radians, cos, sin, asin, sqrt
import requests
import xml.etree.ElementTree as ET


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
