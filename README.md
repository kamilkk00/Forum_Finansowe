# Forum Finansowe

### English version below

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

---

# Financial Forum

This online forum was designed with the idea of sharing knowledge between experienced individuals or specialists in their respective fields (such as tax advisors, accountants, and others).

The Financial Forum is a web application based on the Django framework.  
The forum serves two types of users:  
The first group consists of individuals seeking knowledge in specific areas related to running a business. These users can find articles of interest to them and view profiles of the authors to get additional information such as a website or phone number, allowing them to contact an expert.  
The second group consists of specialists who want to share their knowledge. If these professionals offer advisory services (e.g., accounting), they can upgrade their profile to a professional user and provide detailed information about their services. After reading an article, users may be interested in using the services of that advisor.

The platform offers many features, such as creating professional profiles with detailed information, editing posts, commenting, and liking posts and comments.  
Likes influence the ranking on the homepage, and users can search for articles by categories or keywords.  
Professional profiles also allow users to leave reviews and ratings (from 1 to 5).

## Features

- **Registration and Login**: Users can register, log in, and log out.
- **Post Creation**: Logged-in users can create new posts in selected categories.
- **Commenting**: Users can comment on posts and edit their comments.
- **User Profiles**: Users can view other users' profiles, including professional profiles.
- **Professional Profiles**: Users can upgrade their accounts to professional profiles and provide detailed information about their services.
- **Saving and Liking Posts**: Users can save posts for later viewing and add likes.
- **Searching**: Users can search for posts by title or content.
- **Adding Reviews**: Users can leave reviews and ratings for professional profiles.

## Project Structure

- **views.py**: Contains the application’s logic, including handling post creation, comments, user profiles, and other functions.
- **models.py**: Defines data models such as User, Post, Comment, ProfessionalUser, Like, SavedPost, etc.
- **urls.py**: Defines URL paths for various views.
- **templates/finance**: Contains HTML templates for the application, including the homepage, login, registration, post creation, user profiles, etc.
- **static/finance**: Contains static files such as CSS and JavaScript used in the application.

## Reporting Issues
If you find any issues or have suggestions for improvement, please report them via [GitHub Issues].