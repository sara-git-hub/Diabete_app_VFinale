# 🏥 API de Gestion Médicale - Prédiction de Diabète

Une application complète pour les professionnels de santé permettant de gérer les patients et prédire les risques de diabète.

## ✨ Fonctionnalités

### 🔐 Authentification Sécurisée
- Inscription et connexion des médecins
- Sessions protégées
- Gestion des permissions

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
-HTML/CSS simple

**Data:**
-PostgreSQL
-Pandas (prétraitement)

**ML:**
-Scikit-learn
-Joblib (sérialisation)

### 📊 Structure du projet
text
medical_app/
│
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
│   ├── base.html
│   └── navbar.html
│
├── models/                # Modèles Pydantic et SQLAlchemy
│   ├── schemas.py         # Schémas Pydantic
│   └── database.py        # Modèles SQLAlchemy

### 🔒 Sécurité
-Hashage des mots de passe (bcrypt)
-Gestion des sessions sécurisées
-Validation des données via Pydantic
-Protection des routes sensibles

