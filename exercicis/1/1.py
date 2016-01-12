#!/usr/bin/python

def difElemList(lista):
    ret = []
    for i in lista:
        if i not in ret:
            ret.append(i)
    return len(ret)

def maxList(lista):
    ret = lista[0]
    for i in lista[1:]:
        if i > ret:
            ret = i
    return ret

def maxList(lista):
    return (reduce(lambda x,y: x+y, lista))/len(lista)

def aplanaList(lista):
    ret = []
    if isinstance(lista,list):
        for i in lista:
            ret = ret + aplanaList(i)
    else:
        ret = [lista]
    return ret

def insOrd(lista,n):
    if n <= lista[0]:
        return [n] + lista
    else:
        return lista[0] + insOrd(lista[1:],n)

def evenAndOdd(lista):
    e = []
    o = []
    for i in lista:
        if i%2 == 0:
            e.append(i)
        else:
            o.append(i)

    return (e,o)

def getDivisors(n, primeCheck = False):
    ret = [1]
    for i in range(2,n+1):
        if n%i == 0:
            if primeCheck:
                ret.append(i)
            elif len(getDivisors(i, True)) <= 2:
                ret.append(i)
    return ret

def mOrd(l1,l2):
    if len(l1) == 0:
        return l2
    elif len(l2) == 0:
        return l1
    elif l1[0] <= l2[0]:
        return [l1[0]] + mOrd(l1[1:],l2)
    else:
        return [l2[0]] + mOrd(l1,l2[1:])

def mergeSort(lista):
    if (len(lista) <= 1):
        return lista
    else:
        s = len(lista)/2
        l1 = lista[:s]
        l2 = lista[s:]
        return mOrd(mergeSort(l1),mergeSort(l2))

def quickSort(lista):
    s = len(lista)
    if s <= 1:
        return lista

    else:
        s = s/2
        l1 = quickSort(filter(lambda x: x < lista[s], lista))
        l2 = quickSort(filter(lambda x: x > lista[s], lista))
        return l1 + [lista[s]] + l2
