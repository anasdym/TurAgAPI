# 🌍 TurAgAPI: Biuro podróży

Prosta aplikacja API stworzona w Pythonie przy użyciu FastAPI. Umożliwia dodawanie, przeglądanie i filtrowanie podróży oraz przeliczanie cen z PLN na inne waluty przy użyciu API Narodowego Banku Polskiego (NBP).

## 📦 Technologie

- Python 3.8+
- FastAPI
- SQLite
- Requests (do zapytań HTTP)
- API NBP do pobierania kursów walut

---

## 🚀 Uruchomienie aplikacji

1. **Klonowanie repozytorium lub skopiowanie plików**
2. **Utworzenie i aktywacja środowiska wirtualnego:**

```bash
python -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows

pip install -r requirements.txt

uvicorn main:app --reload
lub
python -m uvicorn app:app --reload
```

Aplikacja będzie dostępna pod adresem: http://127.0.0.1:8000
Dokumentacja Swagger UI: http://127.0.0.1:8000/docs

## 💾 Baza danych

Dane są przechowywane lokalnie w pliku travel.db (SQLite).

Tabela trips jest tworzona automatycznie przy pierwszym uruchomieniu aplikacji.

Pola: id, destination, month, price_pln


## 🌐 Endpointy API

✅ GET /health
Szybkie sprawdzenie statusu aplikacji.

Odpowiedź:
{ "status": "ok" }

➕ POST /trips
Dodanie nowej podróży.

Przykładowe zapytanie:
{
  "destination": "Paryż",
  "month": "Wrzesień",
  "price_pln": 2200.0
}

Odpowiedź:
{
  "id": 1,
  "destination": "Paryż",
  "month": "Wrzesień",
  "price_pln": 2200.0

🌍 GET /trips
Zwraca wszystkie dostępne podróże. Obsługuje przeliczenie cen na walutę podaną w parametrze currency.

Parametry zapytania: currency (opcjonalnie, domyślnie: PLN) – np. EUR, USD

Przykład odpowiedzi:
{
  "trips": [
    {
      "id": 1,
      "destination": "Paryż",
      "month": "Wrzesień",
      "price": "501.12",
      "currency": "EUR"
    }
  ]
}

🎯 GET /trips/{destination}
Zwraca podróże do konkretnego miejsca docelowego. Można również przeliczyć cenę na wybraną walutę.

Parametry:
- destination – nazwa miejsca (np. Paryż)
- currency – (opcjonalnie) waluta do przeliczenia

Przykład:
/trips/Paryż?currency=USD

## 📝 Licencja
Projekt edukacyjny. Możesz używać, modyfikować i rozbudowywać bez ograniczeń.

Zadanie: https://mhyla.com/jica-python11/#mini-projekt-proste-api-biuro-podr%C3%B3%C5%BCy-2-osobowe-zespo%C5%82y