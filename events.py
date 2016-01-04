#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata
from unicodedata import normalize
import requests
import xml.etree.ElementTree as ET

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

    def tostring(self):
        return self.index


class ParseEvents:
    __src = "http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199"

    def __xml2obj(self, act):
        nom = act.find('nom').text
        carrer = act.find('lloc_simple/adreca_simple/carrer').text
        data = act.find('data/data_proper_acte').text

        lloc = act.find('lloc_simple/nom').text
        barri = act.find('lloc_simple/adreca_simple/barri').text

        lat = act.find('lloc_simple/adreca_simple/coordenades/googleMaps').get('lat')
        lon = act.find('lloc_simple/adreca_simple/coordenades/googleMaps').get('lon')
        #print nom
        return Event(nom,lloc,barri,carrer,data,lon,lat)

    def __init__(self):
        self.events = []

        #resp = requests.get(self.__src)
        #msg = resp.content
        #tree = ET.fromstring(msg)
        tree = ET.parse('bcn.xml')
        root = tree.getroot()

        for act in root.findall('body/resultat/actes/acte'):
            self.events.append(self.__xml2obj(act))

    def test(self,n):
        for i in self.events:
            if i.itmatch(n):
                print i.tostring()


class Events:

    def __init__(self):
        self.pe = ParseEvents()

    def __evalEntrada(self,entrada):
        if isinstance(entrada, list):
            #s'ha de complir alguna d'elles
            print entrada, "is a list"
            for i in entrada:
                self.__evalEntrada(i)

        elif isinstance(entrada,tuple):
            #s'ha de complir tot
            print entrada, "is a tuple"
            #for i in entrada:
            #    self.__evalEntrada(i)

        else:
            #print entrada, "is a string"
            return entrada


    def getEvents(self,entrada):
        res = eval(entrada)
        self.__evalEntrada(res)
