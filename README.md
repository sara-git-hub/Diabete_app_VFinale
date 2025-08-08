# 🏥 API de Gestion Médicale - Prédiction de Diabète

Application web dédiée aux médecins, permettant la gestion des dossiers patients et la prédiction du risque de diabète grâce à un modèle de ML. Développée avec HTML/CSS pour le frontend, FastAPI en backend et PostgreSQL pour la BDD.

## ✨ Fonctionnalités

### 🔐 Authentification et Sécurité
-Inscription/connexion avec validation Pydantic
-Sessions via cookies signés
-Mots de passe hashés en bcrypt
-Protection des routes par vérification de session
-Validation stricte des données entrantes

### 📋 Gestion des Patients
- Ajout/suppression de patients
- Visualisation des dossiers
- Historique complet

### 🔮 Prédiction Intelligente
- Analyse des facteurs de risque :
  - Taux de glucose
  - Pression artérielle
  - IMC
  - Antécédents familiaux
  - Âge
- Résultat avec indice de confiance

### 📊 Statistiques Avancées
- Tableau de bord complet
- Visualisation des tendances
- Export des données

### 🔧 Technologies Clés

**Backend:**
-FastAPI
-SQLAlchemy ORM
-Pydantic (validation)
-Passlib (hash)

**Frontend:**
-Jinja2 Templates
-HTML/CSS

**Data:**
-PostgreSQL
-Pandas (prétraitement)

**ML:**
-Joblib (sérialisation)

### 📊 Structure du projet

medical_app/

├── main.py                # Fichier principal de l'application

├── model.pkl              # Modèle de machine learning

├── README.md

│

├── templates/             # Templates HTML

│   ├── login.html         # Page de connexion

│   ├── register.html      # Page d'inscription

│   ├── patients.html      # Liste des patients

│   ├── add_patient.html   # Formulaire d'ajout

│   ├── index.html         # Page d'accueil

│   └── navbar.html        # Barre de navigation

│   └── base.html          # Template parent avec structure commune (HTML, CSS, blocs définissables)

│
├── models/                # Modèles Pydantic et SQLAlchemy

│   ├── schemas.py         # Schémas Pydantic

│   └── database.py        # Modèles SQLAlchemy


### 🔄 Fonctions Utilitaires

-get_db()                      : Obtient une session de base de données
-get_password_hash(password)   : Hash un mot de passe avec bcrypt
-verify_password(plain, hashed):Vérifie un mot de passe contre son hash
-predict_diabetes(patient_data):Prédit le diabète avec le modèle ML (retourne prédiction + confiance)

### 🔐 Routes d'Authentification (HTML)

|Méthode	|Route	    |Fonction	        |Description                   |
|---------|-----------|-----------------|------------------------------|
|GET	    |/login	    |login_page()	    |Affiche le formulaire de login|
|POST	    |/login	    |login_submit()	  |Traite la connexion           |
|GET	    |/register	|register_page()  |Affiche l'inscription         |
|POST	    |/register	|register_submit()|Traite l'inscription          |
|GET	    |/logout	  |logout()	        |Déconnexion                   |

### 🏠 Routes Principales (HTML)

|Méthode	|Route	     |Fonction	          |Description                  |
|---------|---------------------------------|-----------------------------|
|GET	    |/	         |root()	            |Page d'accueil               |
|GET	    |/add	       |add_patient_form()  |Formulaire d'ajout de patient|
|POST	    |/submit	   |submit_patient()	  |Traite l'ajout de patient    |
|GET	    |/patients	 |patients_dashboard()|Liste des patients + stats   |
|POST	    |/delete/{id}|delete_patient()	  |Supprime un patient          |

### 🧩 Modèles Pydantic (schemas.py)
-UserCreate : Validation création utilisateur
-UserLogin : Validation connexion
-PatientCreate : Validation données patient

### 🗃️ Modèles SQLAlchemy (database.py)
-Medecin : Table médecins        -Champs : id, username, email, password
-Patient : Table patients        -Champs : id, doctorid, name, age, sex, glucose, etc.
-Prediction : Table prédictions  -Champs : id, patientid, result, confidence