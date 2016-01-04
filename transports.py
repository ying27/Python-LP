#!/usr/bin/python
from stations import TransportTMB
from bicing import Bicing

class Transport:
    def __init__(self):
        self.bicingBikes = []
        self.bicingSlots = []
        self.fgc = []
        self.metro = []
        self.tramvia = []
        self.busdia = []
        self.busnit = []

    def setBicingBikes(self, bikes):
        self.bicingBikes = bikes

    def setBicingSlots(self, slots):
        self.bicingSlots = slots

    def setFGC(self, fgc):
        self.fgc = fgc

    def setMetro(self, metro):
        self.metro = metro

    def setTram(self, tram):
        self.tramvia = tram

    def setBusDia(self, busdia):
        self.busdia = busdia

    def setBusNit(self, busnit):
        self.busnit = busnit

    def hasBicing(self):
        return len(self.bicingBikes) != 0

    def hasTmb(self):
        sum = len(self.fgc) + len(self.metro) + len(self.tramvia) + len(self.busdia) + len(self.busnit)
        return sum != 0

    def __tostring(self,n):
        aux = str()
        for i in n:
            aux = aux + i.tostring() + '\n'
        return aux

    def showTransport(self):
        print '*BICING*'
        print 'Bikes:\n', self.__tostring(self.bicingBikes)
        print 'Slots:\n', self.__tostring(self.bicingSlots)
        print '*FGC*\n', self.__tostring(self.fgc)
        print '*Metro*\n', self.__tostring(self.metro)
        print '*Tramvia*\n', self.__tostring(self.tramvia)
        print '*Bus Dia*\n', self.__tostring(self.busdia)
        print '*Bus Nit*\n', self.__tostring(self.busnit)



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
                    ret.setBicingBikes(self.bicing.getNearBikes(lat, lon))
                    ret.setBicingSlots(self.bicing.getNearSlots(lat, lon))
                    if ret.hasBicing: break
                else:
                    ret.setFGC(self.tmb.getNearFGC(lat,lon))
                    ret.setMetro(self.tmb.getNearMetro(lat,lon))
                    ret.setTram(self.tmb.getNearTram(lat,lon))
                    ret.setBusDia(self.tmb.getNearBusDia(lat,lon))
                    ret.setBusNit(self.tmb.getNearBusNit(lat,lon))
                    if ret.hasTmb: break
        return ret
