## 1. Wstęp

### 1.1 Cel aplikacji

Aplikacja pozwala użytkownikowi na zarządzanie swoją listą zadań do zrobienia.

Głównym celem aplikacji jest ułatwienie użytkownikowi zarządzania zadaniami poprzez prosty interfejs konsolowy. Aplikacja obsługuje dodawanie nowych zadań, wyświetlanie listy zadań, oznaczanie jako wykonane, usuwanie oraz wyszukiwanie zadań po słowie kluczowym. Każdy użytkownik posiada własną, odrębną bazę danych.

### 1.2 Technologia

Do budowy aplikacji wykorzystano:

- **Język programowania:** Python - prostota tworzenia aplikacji.
- **Baza danych:** SQLite - lekkie rozwiązanie bazy danych, które dzięki zapisywaniu w pliku pozwala na przenoszenie danych pomiędzy komputerami.
- **System kontroli wersji:** Git - używany do śledzenia zmian w kodzie oraz współpracy zespołowej.

## 2. Wymagania systemowe

### 2.1 Wymagania sprzętowe

Aby aplikacja działała poprawnie, komputer użytkownika powinien spełniać następujące wymagania:

- **Procesor:** min. 1 GHz - wystarczający do obsługi operacji wykonywanych przez skrypt.
- **RAM:** min. 512 MB - niezbędny do przechowywania danych operacyjnych aplikacji.
- **Wolne miejsce na dysku:** min. 50 MB - przestrzeń potrzebna na plik skryptu, pliki baz danych użytkowników oraz plik logów.
- **System operacyjny:** Windows, Linux, macOS (każdy system operacyjny, na którym można uruchomić interpreter Pythona).

### 2.2 Wymagania programowe

Aby uruchomić aplikację, należy zainstalować:

- **Język programowania:** Zainstalowany interpreter Python w wersji 3.12 lub nowszej.

## 3. Instalacja i konfiguracja

### 3.1 Pobranie aplikacji

1.  Pobierz kod źródłowy:
    ```sh
    git clone https://github.com/przxmus/projekt-ddawidek.git
    ```
2.  cd projekt-ddawidek

### 3.2 Konfiguracja bazy danych

Aplikacja automatycznie tworzy i zarządza plikami bazy danych SQLite.
Logi aplikacji są automatycznie zapisywane do pliku `logi.txt`, tworzonego w tym samym katalogu co skrypt `main.py`.

## 4. Uruchomienie aplikacji

Aby uruchomić aplikację:

1.  Otwórz terminal lub cmd.
2.  Przejdź do folderu, w którym znajduje się plik `main.py`.
    ```sh
    cd projekt-ddawidek
    ```
3.  Uruchom skrypt za pomocą polecenia:
    `sh
python main.py
`
    Po uruchomieniu, aplikacja wyświetli powitanie, poprosi o podanie nazwy użytkownika, a następnie zaprezentuje menu główne w konsoli, umożliwiając interakcję.

## 5. Struktura aplikacji

Aplikacja składa się z jednego głównego pliku wykonywalnego oraz plików generowanych dynamicznie podczas jej działania:

```
/katalog_aplikacji/
│
│-- main.py                    # Główny plik skryptu aplikacji w Pythonie
│
│-- [nazwa_uzytkownika1].db    # Plik bazy danych SQLite dla użytkownika1 (generowany)
│-- [nazwa_uzytkownika2].db    # Plik bazy danych SQLite dla użytkownika2 (generowany)
│-- ...                        # Kolejne pliki baz danych dla innych użytkowników
│
│-- logi.txt                   # Plik logów aplikacji (generowany)
```

- `main.py`: Zawiera cały kod źródłowy aplikacji, w tym definicje klas (`Log`, `Task`, `TaskManager`), logikę zarządzania zadaniami, interakcję z użytkownikiem poprzez CLI, oraz obsługę bazy danych SQLite i logowania zdarzeń.
- `[nazwa_użytkownika].db`: Pliki baz danych SQLite. Każdy taki plik przechowuje zadania (treść, status wykonania) dla konkretnego użytkownika. Nazwa pliku jest tworzona na podstawie nazwy podanej przez użytkownika przy uruchomieniu aplikacji.
- `logi.txt`: Plik tekstowy, w którym zapisywane są chronologicznie logi dotyczące operacji wykonywanych w aplikacji (np. dodanie zadania, oznaczenie jako wykonane, usunięcie, napotkane błędy) wraz ze znacznikiem czasu, typem logu (INFO, BŁĄD) i komunikatem.

## 6. Opis funkcjonalności

### 6.1 Logowanie i rejestracja

Aplikacja nie implementuje tradycyjnego systemu rejestracji i logowania z hasłem. Zamiast tego, przy uruchomieniu prosi użytkownika o podanie "Nazwy użytkownika". Ta nazwa służy do:

- Identyfikacji pliku bazy danych (`[nazwa_użytkownika].db`), w którym przechowywane są zadania danego użytkownika. Jeśli plik dla podanej nazwy nie istnieje, jest tworzony. Jeśli istnieje, zadania są z niego wczytywane.
- Personalizacji wpisów w pliku logów (`logi.txt`), gdzie operacje są przypisywane do konkretnego użytkownika.

### 6.2 Zarządzanie danymi

Aplikacja umożliwia zarządzanie listą zadań poprzez następujące operacje dostępne w menu głównym:

- **Dodaj zadanie (opcja 1):** Użytkownik jest proszony o podanie treści nowego zadania. Zadanie jest tworzone, dodawane do listy zadań i zapisywane w pliku bazy danych użytkownika. Operacja jest logowana.
- **Lista zadań (opcja 2):** Wyświetla wszystkie zadania aktualnego użytkownika. Każde zadanie jest prezentowane z unikalnym numerem ID (licząc od 1), treścią oraz statusem ("Do zrobienia." lub "Zrobione!").
- **Oznacz zadanie jako zrobione (opcja 3):** Użytkownik jest proszony o podanie numeru ID zadania, które ma zostać oznaczone jako wykonane. Po walidacji ID, status zadania jest zmieniany na `True` (zrobione) i zmiana jest zapisywana w bazie danych. Operacja jest logowana.
- **Usuń zadanie (opcja 4):** Użytkownik jest proszony o podanie numeru ID zadania do usunięcia. Po walidacji ID, zadanie jest usuwane z listy w pamięci i z bazy danych. Operacja jest logowana.
- **Wyszukaj zadanie (opcja 5):** Użytkownik jest proszony o podanie słowa kluczowego. Aplikacja przeszukuje treści wszystkich zadań (ignorując wielkość liter) i wyświetla te, które zawierają podane słowo, wraz z ich ID i statusem.
- **Wyjdź (opcja 0):** Kończy działanie aplikacji.

Wszystkie modyfikacje danych (dodawanie, oznaczanie jako zrobione, usuwanie) są natychmiast zapisywane w pliku bazy danych SQLite, zapewniając trwałość danych między sesjami.

## 7. Testowanie aplikacji

### 7.1 Testy jednostkowe

Dostarczony kod aplikacji nie zawiera zaimplementowanych testów jednostkowych.

## 8. Potencjalne problemy i ich rozwiązania

Brak.
