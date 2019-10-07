#POLITECHNIKA GDANSKA WFTIMS
#MATEMATYKA SEMESTR IV
#ALGORYTMY I STRUKTURY DANYCH
#LABORATORIUM 4: TABLICE Z DOSTEPEM ROZPROSZONYM
#MILOSZ SAWICKI
#18.04.2019


import random
import matplotlib.pyplot as plt
import argparse


dane = []
rozmiar=20000
T=[None] * rozmiar
licznik=0


def Main():
    parser = argparse.ArgumentParser(description = "Tablica z dostepem rozproszonym (DHT)\n Example use: -slowo Adam insert -p2", prog = "DHT")
    group_0 = parser.add_mutually_exclusive_group(required=True)
    group_0.add_argument("-slowo",  help = "Prosze podac dowolne slowo",  type= str)
    group_0.add_argument("-avr",  help = "Policz srednia ilosc kolizji przy wstawianiu 1000 elementow do tablicy 5000, 7000 i 9000 elementowej", action = "store_true")


    parser_parent = argparse.ArgumentParser(add_help=False)
    group_1 = parser_parent.add_mutually_exclusive_group(required=True)
    group_1.add_argument("-o", help = "Uzyj adresowania otwartego", action='store_const', const='open')
    group_1.add_argument("-p", help = "Uzyj podwojnego rozpraszania", action='store_const', const='podwojne')
    group_2 = parser_parent.add_mutually_exclusive_group(required=True)
    group_2.add_argument("-1", help = "Uzyj funkcji haszujacej 1", action='store_const', const='hash_1')
    group_2.add_argument("-2", help = "Uzyj funkcji haszujacej 2", action='store_const', const='hash_2')

    subparsers = parser.add_subparsers(help='sub-command help', dest ="i/s",)
    parser_open = subparsers.add_parser('insert', help = "Wstawie elementu w tablicy", parents = [parser_parent])
    parser_search = subparsers.add_parser('search', help = "Wyszukiwanie elementu w tablicy", parents = [parser_parent])

    args= vars(parser.parse_args())

    opcje = [args['avr'] or args['slowo'], args['i/s'], args['1'] or args['2'], args['o'] or args['p']]

    def output(arg0,arg1,arg2,arg3):
        if arg0 == True:
            print(srednia(eval(arg2), eval('hash_{}_{}'.format(arg1, arg3))))
        else:
            print(eval('hash_{}_{}'.format(arg1,arg3))(T, arg0, eval(arg2)))

    output(*opcje)


def hash_1(s):      #pierwsza funkcja haszujaca
    ascii=0
    for i in range(len(s)):
        ascii += ord(s[i])
    ascii=ascii%rozmiar
    return(ascii)

def hash_2(s):      #druga funkcja haszujaca
    hash=5381
    for i in range(len(s)):
        hash=hash*33 + ord(s[i])
    hash=hash%rozmiar
    return(hash)

def hash_moja(s):       #moja funkcja haszujaca
    prime=1000033
    hash=5381
    for i in range(len(s)):
        hash=hash*37 + ord(s[i])
    hash=hash%prime
    return(hash)



def hash_insert_open(T, s, funkcja_h):      #wstawianie przy adresowaniu otwartym dla funkcji 1 lub 2
    global licznik
    i=0
    key = funkcja_h(s) %rozmiar  #generowanie klucza dla funkcji haszujacej okreslonej w argumencie

    while i != (len(T)-1):
        if T[key +i] == None:
            T[key +i] = s
            return(key + i)
        else:
            i += 1
            licznik += 1
    print('error: przepelnienie')

def hash_search_open(T, s, funkcja_h):      #szukanie przy adresowaniu otwartym dla funkcji 1 lub 2
    i=0
    key = funkcja_h(s) %rozmiar #generowanie klucza dla funkcji haszujacej okreslonej w argumencie
    while T[key+i] != None:
        if T[key+i] == s:
            return(key + i)
        else:
            i += 1
    return None

def hash_insert_podwojne(T, s, funkcja_h):
    global licznik
    key = funkcja_h(s) % 20000
    while T[key] != None:
        key = ((key + hash_moja(s)) % 102547) % 20000
        licznik += 1
    T[key] = s
    return key


def hash_search_podwojne(T, s, funkcja_h):
    key = funkcja_h(s) % 20000
    while T[key] != None:
        if T[key] == s:
            return(key)
        else:
            key = ((key + hash_moja(s)) % 1000033) % 20000
    return None


def srednia(funkcja_nr, sposob):     #funkcja liczaca srednia ilosc kolizji

    def funkcja_1(var1, funkcja_nr):
        global licznik

        #aby przyspieszyc wybieranie losowych, nie powtarzajacych sie elementow wybieram od razu dana ilosc elementow + 1000 i dziele na dwie osobne listy
        elementy_rand=random.sample(range(len(slownik)),var1)
        elementy_1 = elementy_rand[1000:]       #zawiera 5000, 7000 lub 9000 losowych, niepowtarzajacych sie elementow
        elementy_2 = set(elementy_rand) - set(elementy_1)   #zawiera zawsze 1000 losowych, niepowtarzajacych sie elementow roznych od elementy_1
        elementy_2 = list(elementy_2)
        #print(len(elementy_rand),len(elementy_1), len(elementy_2))

        for i in elementy_1:
            sposob(T, slownik[i], funkcja_nr)
            i+=1

        licznik=0
        for i in elementy_2:
            sposob(T, slownik[i], funkcja_nr)
            i+=1
        kolizje.append(licznik)


    kolizje = []
    dane=odczyt('dict.txt')     #odczyt i konwersja danych wejsciowych do listy
    slownik = dane.split()

    var=[6000, 8000, 10000]

    for i in var:
        zeruj()     #czysci tablice
        funkcja_1(i, funkcja_nr)

    kolizje_avr = [ float(x)  / 1000 for x in kolizje]      #liczy srednia ilosc kolizji na 1000 wstawien
    print("Srednia ilosc kolizji dla tablicy opowiednio 5000, 7000, 9000 elementowej na 1000 wstawien:")
    return(kolizje_avr)


def odczyt(pliktxt):    #funkcja odczytujaca dane z pliku
    f = open(pliktxt, 'r')
    return f.read()

def pause():    #funkcja pauzujaca program
    input('')

def zeruj():    #funkcja zerujaca glowna tablice
    global T
    T=[None] * rozmiar

def ilosc():    #funkcja liczaca ilosc elementow w tablicy
    return (len([x for x in T if x is not None]))


if __name__== '__main__':
    f= open('table.txt', 'w+')
    Main()
    f.writelines(str(T))
