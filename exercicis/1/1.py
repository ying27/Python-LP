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



######################################################################

def listProd(lista):
    return reduce(lambda a,b: a*b, lista)

def evenListProd(lista):
    return listProd(filter(lambda x: x%2 == 0, lista))

def invertList(lista):
    return reduce(lambda a,b: [b]+a,lista,[])



def times(n,lista):
    return map(lambda x: reduce(lambda a,b: a+(b==n),x,0),lista)

#######################################################################

def zipWith(f,l1,l2):
    l = zip(l1,l2)
    return map(lambda (a,b): f(a,b),l)

def takeWhile(f,l):
    if len(l) == 0 or not f(l[0]):
        return []
    else:
        return [l[0]]+takeWhile(f,l[1:])

def dropWhile(f,l):
    if len(l) == 0 or not f(l[0]):
        return l
    else:
        return dropWhile(f,l[1:])

def foldl(f,a,b):
    return reduce(f,b,a)

def foldr(f,b,a):
    inv = reduce(lambda c,d: [d]+c,a,[])
    return reduce(f,inv,b)

def scanl(f,a,b):
    if len(b) == 1:
        return [f(a,b[0])]
    else :
        res = f(a,b[0])
        return [res]+scanl(f,res,b[1:])

def countIf(f,l):
    return reduce(lambda a,b: a+(f(b)),l,0)

def insertion(f,e,l):
    if len(l) == 0:
        return [e]
    elif f(e,l[0]):
        return [e]+l
    else:
        return [l[0]]+insertion(f,e,l[1:])

def insertionSort(l):
    return reduce(lambda a,b:insertion(lambda x,y:x<=y,b,a),l,[])
