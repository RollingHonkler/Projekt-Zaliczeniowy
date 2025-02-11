# Projekt Python mk. 2
import json   # pozwala na prace z rozszerzeniami .json, używanymi do odczytywania i zapisywania wyników analizy
from pathlib import Path #pozwala na sprawdzenie czy dany plik w ogole istnieje i na zarządzanie ścieżkami do plików
class Alpha: #zdefiniowanie klasy, odpowiedzialnej za całą analizę tekstu
    def __init__(self, nazwa_pliku): #__init__ tzw. konstruktor klasy, przypisuje na poczatku wartosci do atrybutów obiektu
        self.nazwa_pliku = nazwa_pliku #przypisanie wartosci parametru do zmiennej, co pozwoli na przechowywanie nazwy pliku
        self.tekst = "" #pusty ciąg znaków który później bedzie zawierał treść z pliku .txt
        self.sekwencje = [] #pusta lista w której później znajdą się dane (faktyczna sekwencja znaków) z pliku .json

        try:
            with open(nazwa_pliku, 'r', encoding='utf-8') as plik: # spróbuj otworzyć plik o nazwie przekazanej w parametrze nazwa_pliku
                self.tekst = plik.read() #otworzenie i zapisanie zawartości pliku .txt do atrybutu self.tekst patrz wyżej ^^
            with open('sekwencje.json', 'r', encoding='utf-8') as plik: # otwarcie/odczytanie pliku
                self.sekwencje = json.load(plik) #json.load() wczytuje dane z pliku sekwencje.json i zapisuje do atrybutu self.sekwencje ^^^


        except Exception as błąd: #jesli podczas wykonywania kodu w bloku try, bedzie blad (zmienna błąd zawiera dane o błędzie)
            print("Blad podczas wczytywania pliku:", błąd) #kod wyswietli komunikat i przyczynę błędu

    def ilosc_slow(self): #zdefiniowanie składowej klasy
        slowa = self.tekst.split() #.split() dzieli tekst na listę słów, rozdzielając je w miejscach spacji
        licznik = 0 #zmienna przechowujaca ilosc wyrazów
        for slowo in slowa: # przechodzi przez kazdy element listy i wykonuje polecenie
            if slowo.isalpha(): #.isalpha sprawdza czy wszystkie znaki to litery
                licznik += 1 #jesli tak to +1 do licznika
        return licznik #zwraca wynik (licznik)

    def ilosc_liczb(self): #zdefiniowanie składowej klasy
        slowa = self.tekst.split() # split() jak wyżej ^^^.
        licznik = 0 #zmienna przechowująca ilosc liczb
        for slowo in slowa: # przechodzi przez kazdy element listy i wykonuje polecenie
            try:
                float(slowo) # spróbuj zamienić słowo na liczbę zmienoprzecinkową
                licznik += 1 #jesli udalo sie dodaj +1 do zmiennej na poczatku
            except ValueError: # jesli wystapi blad (ValueError - nie jest liczbą tzn. wyraz), pass każe nic nie robić, kod przechodzi do nastepnego slowa
                pass
        return licznik # zwróć wynik

    def wlk_litery(self): #zdefiniowanie składowej klasy
        slowa = self.tekst.split() #jak wyzej
        duze_slowa = [] #stworzenie pustej listy, do ktorej kod doda slowa wpasowujace sie w kryterium
        for slowo in slowa: # przechodzi przez kazdy element pliku tekstowego i wykonuje polecenie
            if slowo[0].isupper(): #jesli pierwsza litera (slowo[0]) jest wielką (.isupper())
                duze_slowa.append(slowo) #dodaj do w.w. listy
        return sorted(set(duze_slowa)) #set() zamienia na zbiór w celu usunięcia powtórzeń, sorted() sortuje słowa alfabetycznie

    def wyraz_sekwencja(self): #zdefiniowanie składowej klasy
        wyniki = {} #stworzenie pustego slownika
        slowa = self.tekst.split() #jak wyzej

        for sekwencja in self.sekwencje: # przechodzi przez wszystkie sekwencje z pliku sekwencje.json
            pasujace_slowa = [] # stworzenie pustej listy do kazdej sekwencji, do której dodaje te słowa z tekstu, które spełnią kryterium
            for slowo in slowa: #przechodzi przez kazdy element pliku tekstowego i wykonuje polecenie
                indeks = 0 #zmienna czyli indeks który sledzi postep w dopasowywaniu znaków
                for znak in slowo: #sprawdza kazdego znaku w slowie i wykonuje dalsze kroki
                    if indeks < len(sekwencja) and znak == sekwencja[indeks]: #indeks < len(sekwencja) sprawdza czy indeks nie wyszedł poza sekwencję; znak == sekwencja[indeks] czy znak w wyrazie odpowiada znakowi z sekwencji
                        indeks += 1 #jeslli pasuje zwiekszanie licznika o 1 i przejscie do nastepnego znaku
                if indeks == len(sekwencja): #jesli licznik jest rowny dlugosci sekwencji oznacza ze w slowie znaleziono okreslona ilosc znaków sekwencji w odpowiedniej kolejnosci
                    pasujace_slowa.append(slowo) #.append() dodaje to słowo do listy okreslonej na poczatku
            wyniki["".join(sekwencja)] = sorted(set(pasujace_slowa)) # .join() łączy znaki sekwencji w jeden ciąg, set() usuwa duplikaty z listy pasujących słów, sorted() sortuje alfabetycznie liste, przypisanie efektów pracy do słownika wyniki
        return wyniki # zwrócenie słownika wyniki

    def alfab_slowa(self): #zdefiniowanie składowej klasy
        slowa = self.tekst.split() #jak wyżej
        nowe_slowa = [] # stworzenie pustej listy na wyniki
        for slowo in slowa: # przechodzi przez kazdy element pliku tekstowego i wykonuje polecenie
            if slowo.isalpha(): #.isalpha sprawdza czy wszystkie znaki to litery
                nowe_slowa.append(slowo.lower()) #przekształca cale slowo na tylko wyłącznie małe litery, .append dodaje słowo do listy nowe_slowa
        return sorted(set(nowe_slowa)) #set() usuwa powtarzające się słowa, sorted() sortuje je alfabetycznie, i zwraca to w formie  wyniku

    def licz_wystapienia(self): #zdefiniowanie składowej klasy
        slowa = self.tekst.split() #jak wyżej
        wystapienia = {} # stworzenie pustego słownika
        for slowo in slowa:  # przechodzi przez kazdy element pliku tekstowego i wykonuje polecenie
            wystapienia[slowo] = wystapienia.get(slowo, 0) + 1 # program przechodzi przez każde słowo, get() sprawdza czy słowo wczesniej bylo juz zarejestrowane w slowniku (nie ma = 0, jest = obecna ilosc wystapien) i dodaje +1 do danego slowa
        return dict(sorted(wystapienia.items(), key=lambda x: x[1], reverse=True)) # sortowanie wyniku, .items() zamienia słownik na listę par (słowo/liczba), key=lambda x: x[1] sortuje wg drugiego elementu każdej pary, reverse=True sortuje od najwiekszej do najmniejszej

    def zapisz_wyniki(self): #zdefiniowanie składowej klasy, metody która zbiera powyzej wykonane wyniki
        wyniki = { #stwórz który bedzie zawierał wyniki i wywoła wyniki metod np. self.ilosc_slow()
            "Liczba slów": self.ilosc_slow(), #zwraca przeanalizowana wczesniej ilosc slów
            "Ilosc liczb": self.ilosc_liczb(), #zwraca przeanalizowana wczesniej ilosc liczb
            "Zaczynające wielkie litery": self.wlk_litery(), #zwraca wczesniej przeanalizowana listę słów ktore zaczynaja się z wielkiej litery
            "Słowa z literami z sekwencji": self.wyraz_sekwencja(), #zwraca listę słów które zawieraja określoną sekwencje liter
            "Seg. alfabetyczna": self.alfab_slowa(), #zwraca listę słów posortowaną alfabetycznie
            "Seg. występowanie": self.licz_wystapienia() #zwraca listę słów i ich wystapien w tekscie
        }
        nowa_nazwa = self.nazwa_pliku.replace('.txt', '_wyniki.json') #zmiana nazwy pliku (np. unabomber.txt na unabomber_wyniki .json) #.replace() w tym przypadku szuka koncowki .txt i zamienia ja na _wyniki.json
        try:
            with open(nowa_nazwa, 'w', encoding='utf-8') as plik: #próbuje utworzyć plik o zmienionej nazwie, w kodowaniu utf-8 (rozszerza standardowy angielski alfabet o inne znaki np. polskie), w trybie zapisu 'w' (nadpisze zawartość, jesli nie istnieje to go stworzy)
                json.dump(wyniki, plik, ensure_ascii=False, indent=4) #json.dump zapisuje dane (konkretnie wyniki, patrz wyżej^^^) w formacie .json do 'plik'^^, ensure_ascii=false pozwala na zapis polskich znaków (spoza standardu ASCII), indent=4 formatuje tekst i dodaje wciecia
            print("Wyniki zapisane do pliku", nowa_nazwa) #po udanym zapisie kod informuje uzytkownika o pomyslnym zapisaniu pliku i podaje nazwe nowego pliku
        except Exception as błąd: #obsługa potencjalnego błędu, zmienna 'błąd' zawiera szczegóły błędu
            print("bład podczas zapisu wynikow:", błąd) #komunikat + info o błędzie


def main(): #zdefiniowanie funkcji main(), glówna funkcja programu
    print("Program do analizy tekstu. Wpisz 'koniec', aby zakonczyc.") #informacja powitalna wraz z informacja ja zakończyć działanie programu

    while True: #rozpoczęcie pętli, program ciągle będzie pytał o nowe pliki do analizy chyba ze uzytkownik wpisze koniec
        nazwa = input("Podaj nazwe pliku: ") #prośba o wpisanie nazwy pliku, input() zatrzymuje program do czasu interakcji przez uzytkownika

        if nazwa.lower() == "koniec": #jesli uzytkownik wpisze komende 'koniec' (niezaleznie czy wielkimi czy malymi literami)
            break #przerywa pętle i kończy program

        if not Path(nazwa).is_file(): #sprawdza czy plik o podanej nazwie istnieje
            print("Plik nie istnieje! Sprobuj ponownie.") #jesli nie wyswietla komunikat o bledzie
            continue #powrót do początku pętli

        analizator = Alpha(nazwa) #przypisanie klasy do zmiennej
        analizator.zapisz_wyniki() #prośba o zapisanie wyników analizy


if __name__ == "__main__": #sprawdza czy kod jest uruchamiany jako główny program, a nie moduł
    main() #jesli tak wywołuje funkcję main() która rozpoczyna cały proces
