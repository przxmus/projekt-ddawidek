## 1. Wstęp

### 1.1 Cel aplikacji

Aplikacja jest prostym forum działającym w konsoli. Umożliwia użytkownikom rejestrację, logowanie, tworzenie postów, przeglądanie postów innych użytkowników, komentowanie oraz polubienie treści.

Głównym celem aplikacji jest stworzenie platformy do dyskusji poprzez interfejs tekstowy. Aplikacja oferuje również podstawowe funkcje moderacji postów dla ich autorów oraz administratora, a także wyszukiwanie treści. Wszystkie dane przechowywane są w jednej, wspólnej bazie danych.

### 1.2 Technologia

Do budowy aplikacji wykorzystano:

- **Język programowania:** Python - prostota tworzenia aplikacji.
- **Baza danych:** SQLite - lekkie rozwiązanie bazy danych, które dzięki zapisywaniu w pliku (`forum.db`) pozwala na łatwe zarządzanie danymi aplikacji. Baza zawiera tabele `users`, `posts`, `comments` oraz `likes`.
- **System kontroli wersji:** Git - używany do śledzenia zmian w kodzie oraz współpracy zespołowej.

## 2. Wymagania systemowe

### 2.1 Wymagania sprzętowe

Aby aplikacja działała poprawnie, komputer użytkownika powinien spełniać następujące wymagania:

- **Procesor:** min. 1 GHz - wystarczający do obsługi operacji wykonywanych przez skrypt.
- **RAM:** min. 512 MB - niezbędny do przechowywania danych operacyjnych aplikacji.
- **Wolne miejsce na dysku:** min. 50 MB - przestrzeń potrzebna na plik skryptu, plik bazy danych `forum.db` oraz plik logów.
- **System operacyjny:** Windows, Linux, macOS (każdy system operacyjny, na którym można uruchomić interpreter Pythona).

### 2.2 Wymagania programowe

Aby uruchomić aplikację, należy zainstalować:

- **Język programowania:** Zainstalowany interpreter Python w wersji 3.12 lub nowszej.

## 3. Instalacja i konfiguracja

### 3.1 Pobranie aplikacji

1.  Pobierz kod źródłowy (zakładając, że nazwa repozytorium pozostaje taka sama):
    ```sh
    git clone https://github.com/przxmus/projekt-ddawidek2.git
    ```
2.  Przejdź do katalogu projektu:
    ```sh
    cd projekt-ddawidek2
    ```

### 3.2 Konfiguracja bazy danych

Aplikacja automatycznie tworzy plik bazy danych `forum.db` przy pierwszym uruchomieniu, jeśli nie istnieje. Inicjalizowane są w niej niezbędne tabele oraz tworzony jest domyślny użytkownik 'admin' z hasłem 'admin'.
Logi aplikacji są automatycznie zapisywane do pliku `logi.txt`, tworzonego w tym samym katalogu co skrypt `main.py`.

## 4. Uruchomienie aplikacji

Aby uruchomić aplikację:

1.  Otwórz terminal lub cmd.
2.  Przejdź do folderu, w którym znajduje się plik `main.py`.
    ```sh
    cd projekt-ddawidek2
    ```
3.  Uruchom skrypt:
    ```sh
    python main.py
    ```
    Po uruchomieniu, aplikacja wyświetli menu powitalne, oferując opcje rejestracji lub logowania. Po pomyślnym zalogowaniu, użytkownikowi zostanie zaprezentowane menu główne forum, umożliwiające interakcję z jego funkcjami.

## 5. Struktura aplikacji

Aplikacja składa się z jednego głównego pliku oraz plików generowanych podczas jej działania:

```
/projekt-ddawidek2/
│
│-- main.py                    # Głowny skrypt
│
│-- forum.db                   # Baza danych
│
│-- logi.txt                   # Logi
```

- `main.py`: Zawiera cały kod źródłowy aplikacji.
- `forum.db`: Plik bazy danych. Przechowuje dane wszystkich użytkowników, postów, komentarzy oraz polubień.
- `logi.txt`: Plik tekstowy, w którym zapisywane są chronologicznie logi dotyczące operacji wykonywanych w aplikacji wraz ze znacznikiem czasu, typem logu (INFO, BŁĄD) i komunikatem.

## 6. Opis funkcjonalności

### 6.1 Logowanie i Rejestracja

Aplikacja implementuje system rejestracji i logowania użytkowników.

- **Rejestracja:** Użytkownik może utworzyć nowe konto podając unikalny login oraz hasło. Data rejestracji jest zapisywana automatycznie.
- **Logowanie:** Aby uzyskać dostęp do funkcji forum, użytkownik musi zalogować się używając swojego loginu i hasła.
- **Użytkownik Admin:** Przy pierwszym uruchomieniu aplikacji i inicjalizacji bazy danych, tworzone jest konto administratora: login `admin`, hasło `admin`.
- **Wylogowanie:** Zalogowany użytkownik może wylogować się z systemu, co powoduje powrót do menu powitalnego.

Operacje logowania, rejestracji i wylogowania są zapisywane w pliku `logi.txt`.

### 6.2 Główne funkcje forum

Po zalogowaniu, aplikacja umożliwia korzystanie z następujących funkcji forum, dostępnych poprzez menu główne:

- **Utwórz nowy post (opcja 1):** Zalogowany użytkownik może utworzyć nowy post, podając jego tytuł i treść. Post zostaje zapisany w bazie danych i przypisany do autora. Operacja jest logowana.
- **Wyświetl wszystkie posty (opcja 2):** Wyświetla listę wszystkich postów na forum, posortowaną od najnowszych. Każdy post jest prezentowany z ID, tytułem, nazwą autora oraz liczbą komentarzy i polubień.
- **Przeglądaj konkretny post (opcja 3):** Użytkownik podaje ID posta, aby wyświetlić jego pełną zawartość, w tym tytuł, treść, autora, datę utworzenia, liczbę polubień oraz wszystkie komentarze do tego posta (wraz z ich autorami i treścią). W tym widoku dostępne są dodatkowe akcje:
  - **Dodaj komentarz:** Umożliwia dodanie nowego komentarza do przeglądanego posta.
  - **Polub post:** Pozwala zalogowanemu użytkownikowi polubić przeglądany post. Jeden użytkownik może polubić dany post tylko raz.
  - **Moderuj post:** Jeśli zalogowany użytkownik jest autorem posta lub administratorem (`admin`), pojawia się opcja moderacji, która pozwala na edycję (zmiana tytułu/treści) lub usunięcie posta. Usunięcie posta kasuje również powiązane z nim komentarze i polubienia.
- **Wyszukaj posty (opcja 4):** Użytkownik może wprowadzić słowo kluczowe, aby przeszukać tytuły i treści wszystkich postów. Wyświetlana jest lista pasujących postów.
- **Wyloguj (opcja 5):** Kończy sesję aktualnego użytkownika i powraca do menu powitalnego.

Wszystkie modyfikacje danych (tworzenie postów, dodawanie komentarzy, polubienia, edycja/usuwanie postów) są natychmiast zapisywane w pliku bazy danych `forum.db` i logowane w `logi.txt`.

## 8. Potencjalne problemy i ich rozwiązania

- **Bezpieczeństwo haseł:** Hasła użytkowników są przechowywane w bazie danych w formie jawnego tekstu. Trzeba zaimplementować hashowanie haseł.
- **Walidacja danych wejściowych:** Walidacja danych wprowadzanych przez użytkownika jest bardzo mała, można byłoby ją rozszerzyć.
- **Brak stron:** Przy dużej liczbie postów lub komentarzy, ich wyświetlanie może stać się nieczytelne. W przyszłości można by dodać system stron.

## 9. Wykorzystanie AI

- "Przekonwertowanie" bazy z pliku .sql (wyeksportowanego przez phpMyAdmin) na kod pythonowy pod SQLite.
- Dowiadywanie się rzeczy o których nie wiedziałem.
- Przeredagowanie dokumentacji, aby była lepiej ubrana w słowa.
- Sporadyczna pomoc "autocompletion" z Copilota.
