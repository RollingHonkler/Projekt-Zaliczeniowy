# Projekt Python mk. 4
import json   # pozwala na prace z rozszerzeniami .json, używanymi do odczytywania i zapisywania wyników analizy
from pathlib import Path #pozwala na sprawdzenie czy dany plik w ogole istnieje i na zarządzanie ścieżkami do plików
import re # pozwala na prostsze wyszukiwanie okreslonych wzorcow (litery, cyfry etc.) w tekscie

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

    def ilosc_slow(self): #zdefiniowanie składowej klasy, liczacej ilosc slow
        wzor_slowo = r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b' #okreslenie wzorca, szyfru znaków który zostanie wyszukany przez tekst (a-z alfabet lacinski, A-Z wlk litery alf. lacinskiego, ąćęłńóśźżĄĆĘŁŃÓŚŹŻ polskie znaki) b\ to granica poczatek lub koniec wyrazenia
        slowa = re.findall(wzor_slowo, self.tekst, re.UNICODE) # re.findall() szuka wszystkich wyrazen przez wzorzec okreslony linijke wyzej, re.UNICODE obejmuje obsluga polskie znaki
        return len(slowa) #zwrocenie ilosci objektow w liscie czyli ilosci slow

    def ilosc_liczb(self): #zdefiniowanie składowej klasy, liczacej ilosc liczb
        wzor_liczba = r'\b\d+([.,]\d+)?\b' #okreslenie wzorca, d+ szuka liczb ,[.,] szuka kropki lub przecinka, b\ poczatek/koniec (w tym wypadku metoda szuka np. 1 123 1.2 1,4 etc.)
        liczby = re.findall(wzor_liczba, self.tekst) # re.findall() szuka wszystkich wyrazen przez wzorzec okreslony linijke wyzej
        return len(liczby) #zwrocenie ilosci objektow w liscie czyli ilosci liczb

    def wlk_litery(self): #zdefiniowanie składowej klasy, wypisujacej wszystkie wyrazy zaczynajace sie z wielkiej litery
        wzor_wielka = r'\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]*\b' #okreslenie wzorca, \b[A-ZĄĆĘŁŃÓŚŹŻ] dopasowuje pierwsza wielka litere, dopasowuje pozniejsze male litery w slowie, * oznacza ze po wlk literze moze wystapic dowolna ilosc malych liter (w tym 0), b/ poczatek/koniec
        duze_slowa = re.findall(wzor_wielka, self.tekst, re.UNICODE) # re.findall() szuka wszystkich wyrazen przez wzorzec okreslony linijke wyzej, re.UNICODE obejmuje obsluga polskie znaki
        return sorted(set(duze_slowa)) #zwrócenie wyniku, set() konwersja na lista->zbior co usuwa powtórzenia, sorted() sortuje alfabetycznie

    def wyraz_sekwencja(self): #zdefiniowanie składowej klasy, szukajacej slow z podana w pliku sekwencja liter
        wyniki = {} #stworzenie pustego slownika do przechowywania rezultatów
        for sekwencja in self.sekwencje: #dla kazdej sekwencji podanych liter wykonuje ponizsze kroki
            wzor = '.*'.join([re.escape(bravo) for bravo in sekwencja]) #re.escape() wymienia litery z podanej sekwencji, .join() laczy te elementy, '.*' dodaje do liter wyrazenie (wzorzec ktory znajdzie litere sekwencji np. a i po ilus innych literach znajdzie nastepna)
            pasujace = re.findall(r'\b\w+\b', self.tekst) #re.findall() szuka tekst w poszukiwaniu fragmentów spełniajacych wyrazenie, w+ to litery i cyfry, efekt to zapisanie wszystkich słów z tekstu jako lista w zmiennej pasujace
            pasujace_slowa = [charlie for charlie in pasujace if re.search(wzor, charlie, re.UNICODE)] #re.search() sprawdza czy slowa z listy pasujace pasuja do stworzonego wzorca, re.UNICODE obejmuje polskie znaki
            wyniki["".join(sekwencja)] = sorted(set(pasujace_slowa)) #.join(sekwencja) tworzy klucz (litery sekwencji) w słowniku, nastepnie wymienione zostaja posortowane alfabetycznie, bez powtorzen, slowa pasujace do danej sekwencji, efekt to słownik w którym kazda kombinacja liter przechwouje pasujace slowa
        return wyniki #zwraca wynik pracy kodu

    def alfab_slowa(self): #zdefiniowanie składowej klasy, segregujacej wyrazy alfabetycznie
        wzor_slowo = r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b' #okreslenie wzorca, [a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ] znajduje wszystkie litery (lacinskie wlk/male + polskie), \b granice slow
        nowe_slowa = re.findall(wzor_slowo, self.tekst, re.UNICODE) #re.findall() przeszukuje tekst wg wzorca, ignorujac wielkosc liter, uzywajac UNICODE co obsluguje polskie znaki
        nowe_slowa = [delta.lower() for delta in nowe_slowa] #delta przeksztalca wszystkie litery w slowach na male, zapobiega powtorzeniom wynikajacym z uzywaniem malych/wielkich liter (Kot,kot to 2 rozne slowa)
        return sorted(set(nowe_slowa)) #zwraca wynik, posortowany alfabetycznie, bez powtorzen

    def licz_wystapienia(self):  #zdefiniowanie składowej klasy, zliczajacej wystapienia slow
        wzor_slowo = r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b' #okreslenie wzorca, [a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ] znajduje wszystkie litery, \b granice slow
        slowa = re.findall(wzor_slowo, self.tekst, re.UNICODE) # re.findall() szuka wszystkich wyrazen przez wzorzec okreslony linijke wyzej, re.UNICODE obejmuje obsluga polskie znaki
        wystapienia = {} # stworzenie pustego słownika
        for slowo in slowa: #przechodzi przez kazdy element pliku tekstowego i wykonuje polecenie
            slowo = slowo.lower() #konwertuje slowa na male litery aby uniknac powtorzen w wyniku (kot i Kot to 2 rozne slowa)
            wystapienia[slowo] = wystapienia.get(slowo, 0) + 1 #program przechodzi przez każde słowo, get() sprawdza czy słowo wczesniej bylo juz zarejestrowane w slowniku (nie ma = 0, jest = obecna ilosc wystapien) i dodaje +1 do danego slowa
        return dict(sorted(wystapienia.items(), key=lambda x: x[1], reverse=True)) #sortowanie wyniku, .items() zamienia słownik na listę par (słowo/liczba), key=lambda x: x[1] sortuje wg drugiego elementu każdej pary, reverse=True sortuje od najwiekszej do najmniejszej
                #nie wiem czy jest latwiejsza forumła na ta metode

    def zapisz_wyniki(self): #zdefiniowanie składowej klasy, metody która zbiera powyzej wykonane wyniki
        wyniki = { #stwórz slownik który bedzie zawierał wyniki i wywoła wyniki metod np. self.ilosc_slow()
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

    while True: #rozpoczęcie pętli, program ciągle będzie pytał o nowe pliki do analizy chyba ze uzytkownik wpisze 'koniec'
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
