# 🎬 MovieWebApp – Dynamische Film-Favoriten-App

Eine vollwertige, dynamische Webanwendung, die Benutzerprofile verwaltet und eine Liste von Lieblingsfilmen über die **OMDb-API** mit Live-Covern und Regisseur-Infos anreichert.

## 🛠️ Tech Stack & Konzepte
- **Framework & Routing:** Python Flask (Backend)
- **Datenbankschicht (ORM):** Flask-SQLAlchemy (SQLite)
- **Datenkapselung (OOP):** Entkoppelte Datenlogik über die Klasse `DataManager`
- **Sicherheit:** Schutz von API-Keys über `.env`-Umgebungsvariablen (`python-dotenv`)
- **Fehlerbehandlung:** Robuste try/except-Blöcke und ein HTTP 404-Errorhandler

## 🏁 Startanleitung
1. Klone das Repository.
2. Erstelle eine `.env`-Datei im Stammverzeichnis und trage deinen `OMDB_API_KEY` ein.
3. Installiere die Abhängigkeiten: `pip install Flask Flask-SQLAlchemy requests python-dotenv`
4. Starte die Anwendung über das Terminal: `flask run --host=0.0.0.0 --port=5002`
