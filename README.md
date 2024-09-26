# Forum Finansowe

## Link do aplikacji: [forum_finansowe](https://www.biznesiwiedza.pl)

Forum finansowe zostało zaprojektowane z myślą o dzieleniu się wiedzą pomiędzy doświadczonymi osobami lub specjalistami w swoich dziedzinach (takich jak doradcy podatkowi, księgowi i inni).

Forum Finansowe to aplikacja internetowa oparta na frameworku Django.  
Forum ma służyć dwóm typom użytkowników:  
Pierwsza grupa to osoby poszukujące wiedzy w konkretnej dziedzinie związanej z prowadzeniem biznesu. Użytkownicy ci mogą znaleźć interesujące ich artykuły, a także przeglądać profile osób, które stworzyły artykuły, w celu uzyskania dodatkowych informacji (takich jak strona internetowa lub numer telefonu), co umożliwi kontakt z ekspertem.  
Druga grupa to specjaliści, którzy chcą dzielić się swoją wiedzą. Jeśli osoby te świadczą usługi doradcze (np. księgowe), mogą zaktualizować swój profil do poziomu profesjonalnego użytkownika, gdzie będą mogli podać informacje o swoim doświadczeniu i szczegółowe dane. Użytkownicy mogą być zainteresowani skorzystaniem z ich usług po przeczytaniu artykułów.

Platforma oferuje wiele funkcji, takich jak tworzenie profesjonalnych profili, edytowanie postów, komentowanie i polubienia.  
Polubienia mają wpływ na ranking na stronie głównej, a użytkownicy mogą wyszukiwać artykuły według kategorii lub słów kluczowych.  
Profesjonalne profile pozwalają na dodawanie opinii i ocen (od 1 do 5) przez użytkowników.

## Funkcje

- **Rejestracja i logowanie**: Użytkownicy mogą się rejestrować, logować i wylogowywać.
- **Tworzenie postów**: Zalogowani użytkownicy mogą tworzyć nowe posty w wybranych kategoriach.
- **Komentowanie**: Użytkownicy mogą komentować posty i edytować swoje komentarze.
- **Profile użytkowników**: Możliwość przeglądania profili innych użytkowników, w tym profili profesjonalnych.
- **Profile profesjonalne**: Użytkownicy mogą aktualizować swoje konta do poziomu profilu profesjonalnego, podając szczegółowe informacje o swoich usługach.
- **Zapisywanie i polubienia postów**: Użytkownicy mogą zapisywać posty do późniejszego przeglądania i dodawać polubienia.
- **Wyszukiwanie**: Użytkownicy mogą wyszukiwać posty po tytule lub treści.
- **Dodawanie opinii**: Użytkownicy mogą dodawać opinie i oceny profili profesjonalnych.

## Struktura projektu

- **views.py**: Zawiera logikę aplikacji, w tym obsługę tworzenia postów, komentarzy, profili użytkowników i innych funkcji.
- **models.py**: Definiuje modele danych, takie jak Użytkownik, Post, Komentarz, UżytkownikProfesjonalny, Polubienie, ZapisanePosty itd.
- **urls.py**: Definiuje ścieżki URL dla poszczególnych widoków.
- **templates/finance**: Zawiera szablony HTML aplikacji, w tym stronę główną, logowanie, rejestrację, tworzenie postów, profile użytkowników itd.
- **static/finance**: Zawiera pliki statyczne, takie jak CSS i JavaScript, używane w aplikacji.

## Zgłaszanie błędów
Jeśli znajdziesz jakiekolwiek błędy lub masz propozycje ulepszeń, zgłoś je za pomocą [GitHub Issues].
