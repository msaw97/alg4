#POLITECHNIKA GDANSKA WFTIMS
#MATEMATYKA SEMESTR IV
#ALGORYTMY I STRUKTURY DANYCH
#LABORATORIUM 4: TABLICE Z DOSTEPEM ROZPROSZONYM
#MILOSZ SAWICKI
#18.04.2019


import random
import matplotlib.pyplot as plt
dane = []



rozmiar=20000
T=[None] * rozmiar
licznik=0

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

def hash_podwojne_insert(T, s, funkcja_h):
    global licznik
    key = funkcja_h(s) % 20000
    while T[key] != None:
        key = ((key + hash_moja(s)) % 102547) % 20000
        licznik += 1
    T[key] = s
    return key


def hash_podwojne_search(T, s, funkcja_h):
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

def menu_main():
    menu = {}
    menu['1']="Wstaw element poprzez sondowanie liniowe"
    menu['2']="Wstaw element poprzez podwojne rozpraszanie"
    menu['3']="Wyszukaj element poprzez sondowanie liniowe"
    menu['4']="Wyszukaj element poprzez podwojne rozpraszanie"
    menu['5']="Policz srednia ilosc kolizji przy wstawianiu 1000 elementow do tablicy 5000, 7000 i 9000 elementowej"
    menu['6']="Wyczysc tablice"
    menu['7']="Wyjscie z programu"
    while True:
        wybor=menu.keys()
        print("Obecna ilosc elementow w tablicy:",  end = " ")
        print(ilosc())
        for n in wybor:
            print(n, menu[n])

        selection=input("\nProsze wybrac opcje:")
        if selection =='1':
            print('Prosze podac slowo do wstawienia:', end = " ")
            slowo = input()
            print("")
            menu_hashf(hash_insert_open, slowo)
        elif selection == '2':
            print('Prosze podac slowo do wstawienia:', end = " ")
            slowo = input()
            print("")
            menu_hashf_p(hash_podwojne_insert, slowo)
        elif selection == '3':
            print('Prosze podac slowo do wyszukania:', end = " ")
            slowo = input()
            print("")
            menu_hashf(hash_search_open, slowo)
        elif selection == '4':
            print('Prosze podac slowo do wyszukania:', end = " ")
            slowo = input()
            print("")
            menu_hashf_p(hash_podwojne_search, slowo)
        elif selection == '5':
            zeruj()
            menu_srednia()
            pause()
        elif selection == '6':
            zeruj()
        elif selection == '7':
            break
        else:
            print("Wybor jest od 1 do 7!")

def menu_hashf(opcja, slowo):
    menu = {}
    menu['1']="Uzyj funkcji haszujacej 1"
    menu['2']="Uzyj funkcji haszujacej 2"
    menu['3']="Wroc"
    while True:
        wybor=menu.keys()
        for n in wybor:
            print(n, menu[n])

        selection=input("\nProsze wybrac opcje: ")
        if selection =='1':
            print("Miejsce w tablicy:", end = " ")
            print(opcja(T, slowo, hash_1))
            pause()
            break
        elif selection == '2':
            print("Miejsce w tablicy:", end = " ")
            print(opcja(T, slowo, hash_2))
            pause()
            break
        elif selection == '3':
            break
        else:
            print("Wybor od 1 do 3!")

def menu_hashf_p(opcja, slowo):
    menu = {}
    menu['1']="Uzyj podwojnego rozpraszania dla funkcji 1"
    menu['2']="Uzyj podwojnego rozpraszania dla funkcji 2"
    menu['3']="Wroc"
    while True:
        wybor=menu.keys()
        for n in wybor:
            print(n, menu[n])

        selection=input("\nProsze wybrac opcje: ")
        if selection =='1':
            print("Miejsce w tablicy:", end = " ")
            print(opcja(T, slowo, hash_1))
            pause()
            break
        elif selection == '2':
            print("Miejsce w tablicy:", end = " ")
            print(opcja(T, slowo, hash_2))
            pause()
            break
        elif selection == '3':
            break
        else:
            print("Wybor od 1 do 3!")


def menu_srednia():
    menu = {}
    menu['1']="Uzyj sondowania liniowego i funkcji haszujacej 1"
    menu['2']="Uzyj sondowania liniowego i funkcji haszujacej 2"
    menu['3']="Uzyj podwojnego rozpraszania i funkcji haszujacej 1"
    menu['4']="Uzyj podwojnego rozpraszania i funkcji haszujacej 2"
    menu['5']="Wroc"
    while True:
        wybor=menu.keys()
        for n in wybor:
            print(n, menu[n])

        selection=input("\nProsze wybrac opcje: ")
        if selection =='1':
            print(srednia(hash_1, hash_insert_open))
            break
        elif selection == '2':
            print(srednia(hash_2, hash_insert_open))
            break
        elif selection == '3':
            print(srednia(hash_1, hash_podwojne_insert))
            break
        elif selection == '4':
            print(srednia(hash_2, hash_podwojne_insert))
            break
        elif selection == '5':
            break
        else:
            print("Wybor od 1 do 3!")



menu_main()
