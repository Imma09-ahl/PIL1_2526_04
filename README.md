# IFRI MentorLink — PIL1_2526_04 (Groupe 4)

Application web de mise en relation entre étudiants de l'IFRI pour du mentorat académique et professionnel.

## Fonctionnalités

- **Authentification** (`feature/auth`) : inscription, connexion, réinitialisation mot de passe, tableau de bord
- **Profil** (`feature/profil`) : informations personnelles, filière, niveau, bio, photo, compétences, disponibilités
- **Compétences** (`feature/competences`) : matières fortes/faibles, créneaux horaires, format de séance
- **Matching** (`feature/matching`) : algorithme de compatibilité mentor/mentoré
- **Messagerie** (`feature/messagerie`) : conversations, messages, notifications en temps réel (polling)

## Architecture

```
Client (HTML/CSS/JS + Tailwind)
        ↕
Serveur Flask (Python) — Blueprints modulaires
        ↕
MySQL (SGBD relationnel)
```

| Module | Dossier principal |
|--------|-------------------|
| Auth | `app/routes/auth.py`, `app/services/auth_service.py` |
| Profil | `app/routes/profile.py` |
| Compétences | `app/routes/competences.py` |
| Matching | `app/routes/matching.py`, `app/services/matching_service.py` |
| Messagerie | `app/routes/messages.py`, `app/models/message.py` |

## Technologies

- **Backend** : Python 3, Flask
- **Frontend** : HTML5, CSS3, JavaScript, Tailwind CSS (CDN)
- **Base de données** : MySQL
- **Sécurité** : Werkzeug (hash MDP), sessions Flask

## Structure des dossiers

```
PIL1_2526_04/
├── app/
│   ├── __init__.py          # Factory Flask
│   ├── config.py            # Configuration
│   ├── models/              # Accès BDD
│   ├── routes/              # Blueprints (routes HTTP)
│   ├── services/            # Logique métier
│   ├── static/              # CSS, JS, uploads
│   ├── templates/           # Templates Jinja2
│   └── utils/               # Décorateurs (login_required)
├── database/
│   └── schema.sql           # Structure BDD finale
├── rapport/                 # Rapport HTML (branche messagerie)
├── run.py                   # Point d'entrée
└── requirements.txt
```

## Installation

### Prérequis

- Python 3.10+
- MySQL 8+
- Git

### Étapes

```bash
git clone <url-du-depot>
cd PIL1_2526_04
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Variables d'environnement optionnelles :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `SECRET_KEY` | `mentorlink_secret_key` | Clé secrète Flask |
| `MYSQL_HOST` | `localhost` | Hôte MySQL |
| `MYSQL_PORT` | `3306` | Port MySQL |
| `MYSQL_USER` | `root` | Utilisateur MySQL |
| `MYSQL_PASSWORD` | *(vide)* | Mot de passe MySQL |
| `MYSQL_DB` | `mentorlink` | Nom de la base |

## Base de données

```bash
mysql -u root -p < database/schema.sql
```

## Lancement

```bash
python run.py
```

Application accessible sur : **http://localhost:5000**

## Utilisation

1. Créer un compte via **S'inscrire**
2. Se connecter → redirection vers le **tableau de bord**
3. Compléter le **profil** (filière, compétences, disponibilités)
4. Gérer les matières dans **Compétences**
5. Consulter les **résultats de matching**
6. **Contacter** un mentor via la messagerie

## Branches Git

| Branche | Responsable(s) | Module |
|---------|------------------|--------|
| `feature/auth` | Jordy Agboton | Authentification |
| `feature/profil` | Aholou Houéfa | Profil utilisateur |
| `feature/competences` | Atinkpahoun Hardy, Karamba Rafiou | Compétences & disponibilités |
| `feature/matching` | Leguede Aristide | Algorithme de matching |
| `feature/messagerie` | Akpo Sara, Olufadé Ayilara | Messagerie |
| `main` | — | Branche d'intégration |

## Procédure de fusion (à faire plus tard)

```bash
git checkout main
git merge feature/auth
git merge feature/profil
git merge feature/competences
git merge feature/matching
git merge feature/messagerie
```

**Fichiers à surveiller lors de la fusion :**

- `app/models/user.py`
- `app/config.py`
- `app/__init__.py`
- `app/templates/layouts/app_layout.html`
- `database/schema.sql`

## Équipe — Groupe 4

1. AHOLOU Houéfa Immaculée Christelle (IA)
2. AGBOTON ATCHOU Tounded Jordy Kristy (GL)
3. AKPO Sara Franckelle Jéhoforte (SI)
4. ATINKPAHOUN Mendel Hardy Mahugnon (SE&IoT)
5. KARAMBA Rafiou (SI)
6. LEGUEDE Aristide (IM)
7. OLUFADE AYILARA Alayi Barakaath Omowumi (GL)

## Licence

Projet académique — IFRI, Université d'Abomey-Calavi, PIL1 2025-2026.
