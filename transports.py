#!/usr/bin/python
from stations import TransportTMB
from bicing import Bicing

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
            ret = ret + '<pre>BICING:<br/><b>Bikes:</b><br/>'
            for i in self.bicingBikes:
                ret = ret + '    ' + i.tohtml() + '<br/>'
            ret = ret + '<b>Slots:</b><br/>'
            for i in self.bicingSlots:
                ret = ret + '    ' + i.tohtml() + '<br/>'
            ret = ret + '</pre>'
        else:
            ret = ret + 'TMB:'
            for i in self.tmb:
                ret = ret + '<br/>   ' + i.tohtml()
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
        else:
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
                    if ret.hasBicing: break
                else:
                    ret.tmb = self.tmb.getTransports(lat,lon)
                    if ret.hasTmb: break
        return ret
