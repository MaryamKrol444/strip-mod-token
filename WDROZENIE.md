# Jak uruchomić stronę na GitHub Pages

## Adres docelowy

**https://maryamkrol444.github.io/strip-mod-token/**

To adres docelowy, nie potwierdzenie aktywnej publikacji. Status publikacji sprawdzisz w zakładce **Actions** i w **Settings → Pages**. Repozytorium: https://github.com/MaryamKrol444/strip-mod-token

## Co zostało przygotowane

- Kompletna statyczna strona: dziewięć plików HTML, obrazy, style, sitemap.xml i robots.txt.
- Automatyczne wdrożenie w `.github/workflows/pages.yml`.
- Obsługa prefiksu `/strip-mod-token/`, aby obrazy, menu, linki wewnętrzne, canonical i Open Graph działały na adresie projektu GitHub Pages.
- Testy treści i linków uruchamiane przy każdym wdrożeniu.
- Publikacja wyłącznie plików publicznych, bez źródeł, testów, zależności i danych repozytorium.

Aktualna gałąź publikacji to **`arena/385c2232-strip-mod-token`**. Nie musisz scalać jej do `main`, aby wdrożenie działało. Zmiana dowolnego pliku na tej gałęzi uruchamia nowe wdrożenie. Workflow nie publikuje automatycznie zmian z `main`.

## Jednorazowa konfiguracja w Twoim koncie

Integracja mogła odczytać repozytorium, ale próba włączenia Pages przez API otrzymała **403 — Resource not accessible by integration**. Dlatego poniższy krok musi wykonać właściciel repozytorium.

1. Zaloguj się na GitHubie na konto mające uprawnienia administratora tego repozytorium.
2. Otwórz **Settings → Pages**:
   https://github.com/MaryamKrol444/strip-mod-token/settings/pages
3. W sekcji **Build and deployment** ustaw **Source → GitHub Actions**. Nie wybieraj „Deploy from a branch”; przygotowany workflow sam zbuduje i prześle pliki strony.
4. Otwórz **Actions**:
   https://github.com/MaryamKrol444/strip-mod-token/actions
5. Wybierz przebieg **Deploy OpenRoom to GitHub Pages** dla gałęzi `arena/385c2232-strip-mod-token`. Jeżeli wcześniejsze uruchomienie nie powiodło się przed włączeniem Pages, wybierz **Re-run all jobs**. **Jeżeli nie ma żadnego przebiegu**, przejdź do zakładki **Code**, wybierz gałąź `arena/385c2232-strip-mod-token`, otwórz ten plik (`WDROZENIE.md`), kliknij ikonę ołówka, dodaj np. notatkę „Pages włączone” i wybierz **Commit changes** bezpośrednio na tej samej gałęzi. Taki commit wykonany z Twojego konta uruchomi publikację. Integracja nie miała również uprawnienia do ręcznego uruchomienia workflow (HTTP 403), dlatego nie zakładamy, że początkowy przebieg już istnieje.
6. Poczekaj, aż zadania **build** i **deploy** będą zielone. Otwórz adres wyświetlony w zadaniu **deploy**, w sekcji **Deployments** lub na stronie **Settings → Pages**.
7. Sprawdź stronę główną i co najmniej jedną podstronę oraz obraz. Pełny adres zawiera `/strip-mod-token/` — samo `maryamkrol444.github.io` to inny adres.

Nie ma gwarantowanego czasu publikacji. Stan zadań w Actions jest ważniejszy niż odświeżanie niedziałającego adresu.

## Jeśli wdrożenie wymaga zgody lub jest blokowane

- Jeżeli GitHub pyta o uruchomienie Actions, zatwierdź je wyłącznie dla tego repozytorium i przygotowanego workflow.
- Jeżeli pojawi się komunikat o niedozwolonej gałęzi dla środowiska `github-pages`, przejdź do **Settings → Environments → github-pages → Deployment branches and tags** i dopuść dokładnie `arena/385c2232-strip-mod-token`. Nie musisz wyłączać wszystkich zabezpieczeń środowiska.
- Jeżeli Actions są wyłączone, sprawdź **Settings → Actions → General**. Ten workflow używa standardowych akcji `actions/checkout`, `actions/setup-python`, `actions/configure-pages`, `actions/upload-pages-artifact` i `actions/deploy-pages`.
- Jeżeli nie widzisz przebiegu workflow po wysłaniu plików, upewnij się, że oglądasz właściwe repozytorium i gałąź. Nowy commit na gałęzi publikacji uruchamia workflow. Przycisk „Run workflow” może być niedostępny, gdy plik workflow nie znajduje się na domyślnej gałęzi; wtedy użyj ponownego uruchomienia istniejącego przebiegu albo nowego commita.
- Jeżeli widzisz 404, sprawdź, czy Pages jest włączone, zadanie deploy zakończyło się sukcesem i otwierasz adres z nazwą repozytorium.

Nie podawaj nikomu haseł, tokenów GitHuba ani kodów 2FA. Przy problemach z uprawnieniami integracji odśwież połączenie GitHub w Arena lub wykonaj ustawienie Pages bezpośrednio w swoim koncie.

## Późniejsze aktualizacje

W edytorze GitHuba wybierz gałąź `arena/385c2232-strip-mod-token`. Główne artykuły edytuje się w `content/*.md`, wspólny szablon i podstrony informacyjne w `scripts/build.py`, wygląd w `assets/styles.css`. Zapisz zmianę przez **Commit changes** na tej samej gałęzi. Workflow wygeneruje HTML i opublikuje nową wersję.

Jeśli edytujesz artykuły, nie zmieniaj wyłącznie wygenerowanych plików HTML — workflow odtworzy je ze źródeł Markdown. Jeśli samodzielnie zmienisz gałąź publikacji w przyszłości, trzeba też zaktualizować filtr `on.push.branches` w workflow i reguły środowiska.

## Własna domena — opcjonalnie

Domena nie jest potrzebna do pierwszej publikacji. Jeśli później ją podłączysz:

1. Skonfiguruj **Settings → Pages → Custom domain** i rekordy DNS według instrukcji wyświetlonych przez GitHub.
2. Włącz **Enforce HTTPS**, gdy GitHub udostępni tę opcję.
3. Uruchom ponownie workflow. Korzysta on z rzeczywistego adresu zwracanego przez GitHub Pages, więc odbuduje canonical, Open Graph, sitemap i ścieżki plików dla aktualnego adresu.
4. Sprawdź przekierowania i linki po wdrożeniu. Nie wpisuj wymyślonych rekordów DNS — użyj aktualnych instrukcji GitHuba dla wybranego typu domeny.

## Ważne przed traktowaniem strony jako gotowego serwisu produkcyjnego

Techniczna publikacja nie zastępuje uzupełnienia informacji prawnych i redakcyjnych. Nadal trzeba podać prawdziwe dane wydawcy, prywatny kontakt w sprawach prywatności, informacje o hostingu/logach i faktyczne relacje afiliacyjne, jeśli istnieją. Nie zostały one wymyślone. Obecne polityki ujawniają te braki. Publiczne zgłoszenia GitHub służą wyłącznie do niesensytywnych korekt redakcyjnych.

Treść dotyczy branży 18+, ale nie zawiera nagości ani instrukcji obchodzenia zabezpieczeń. Wydawca odpowiada za zgodność materiałów i sposobu monetyzacji z bieżącymi zasadami GitHuba oraz lokalnym prawem. Zasady platform i promocje trzeba ponownie sprawdzić przed komercyjnym uruchomieniem. Szczegóły wykluczonych linków i ostrzeżenia przy filmie opisuje `LINK_AUDIT.md`.
