🔄 Fonctions Utilitaires

-get_db()                      : Obtient une session de base de données
-get_password_hash(password)   : Hash un mot de passe avec bcrypt
-verify_password(plain, hashed):Vérifie un mot de passe contre son hash
-predict_diabetes(patient_data):Prédit le diabète avec le modèle ML (retourne prédiction + confiance)

🔐 Routes d'Authentification (HTML)

|Méthode	|Route	    |Fonction	      |Description
------------------------------------------------------------------------
|GET	    |/login	    |login_page()	  |Affiche le formulaire de login
|POST	    |/login	    |login_submit()	  |Traite la connexion
|GET	    |/register	|register_page()  |Affiche l'inscription
|POST	    |/register	|register_submit()|Traite l'inscription
|GET	    |/logout	|logout()	      |Déconnexion

🏠 Routes Principales (HTML)

|Méthode	|Route	     |Fonction	          |Description
------------------------------------------------------------------------
|GET	    |/	         |root()	          |Page d'accueil
|GET	    |/add	     |add_patient_form()  |Formulaire d'ajout de patient
|POST	    |/submit	 |submit_patient()	  |Traite l'ajout de patient
|GET	    |/patients	 |patients_dashboard()|Liste des patients + stats
|POST	    |/delete/{id}|delete_patient()	  |Supprime un patient


📡 Endpoints API (RESTful)

**Patients**
|Méthode	|Route	        |Fonction	           |Description
---------------------------------------------------------------------------------
|POST	    |/api/patients	|create_patient_api()  |Crée un patient (JSON)
|GET	    |/api/patients	|get_patients_api()	   |Liste tous les patients (JSON)

**Prédictions**
|Méthode	|Route	                |Fonction	                |Description
-------------------------------------------------------------------------------------------
|GET	    |/api/predictions/{id}	|get_patient_predictions()	|Prédictions d'un patient
|POST	    |/api/predict	        |predict_api()	            |Prédiction sans sauvegarde

**Système**
|Méthode	|Route	                |Fonction	                |Description
-------------------------------------------------------------------------------------------
GET	        |/health	            |health_check()	            |Vérifie l'état de l'API


🧩 Modèles Pydantic (schemas.py)
-UserCreate : Validation création utilisateur
-UserLogin : Validation connexion
-PatientCreate : Validation données patient
-PatientResponse : Format réponse patient
-PredictionResponse : Format prédiction
-PredictionData : Données de prédiction

🗃️ Modèles SQLAlchemy (database.py)
-Medecin : Table médecins
-Champs : id, username, email, password
-Patient : Table patients
-Champs : id, doctorid, name, age, sex, glucose, etc.
-Prediction : Table prédictions
-Champs : id, patientid, result, confidence

Récapitulatif des Routes - Système de Gestion Médicale
Routes de Navigation Principales
🏠 Route d'accueil

URL : /
Méthode : GET
Template : index.html
Description : Page d'accueil du système avec présentation des fonctionnalités
Authentification : Optionnelle (contenu adapté selon l'état de connexion)


Routes d'Authentification
🔑 Connexion

URL : /login
Méthodes : GET (affichage), POST (traitement)
Template : login.html
Description : Formulaire de connexion pour les médecins
Champs requis : username, password

📝 Inscription

URL : /register
Méthodes : GET (affichage), POST (traitement)
Template : register.html
Description : Création de nouveau compte médecin
Champs requis : username (min 3 car.), email, password (min 6 car.)

🚪 Déconnexion

URL : /logout
Méthode : GET
Description : Déconnexion et suppression de la session
Redirection : Vers la page d'accueil


Routes de Gestion des Patients
📋 Liste des patients

URL : /patients
Méthode : GET
Template : patients.html
Description : Affichage de tous les patients du médecin connecté
Fonctionnalités :

Statistiques (total, diabétiques, non-diabétiques, pourcentage)
Tableau détaillé des patients
Actions de suppression


Authentification : Requise

➕ Ajouter un patient

URL : /add
Méthode : GET
Template : add_patient.html
Description : Formulaire d'ajout de nouveau patient
Authentification : Requise

💾 Sauvegarder un patient

URL : /submit
Méthode : POST
Description : Traitement du formulaire d'ajout patient
Champs requis :

name : Nom complet
age : Âge (0-120)
sex : Sexe (M/F)
glucose : Taux de glucose (0-300 mg/dL)
bloodpressure : Pression artérielle (40-200)
bmi : IMC (10-50)
pedigree : Fonction Pedigree Diabète (0-2)


Fonctionnalité : Prédiction automatique du diabète via IA
Authentification : Requise

🗑️ Supprimer un patient

URL : /delete/<patient_id>
Méthode : POST
Description : Suppression d'un patient spécifique
Paramètre : patient_id (ID du patient à supprimer)
Confirmation : Popup JavaScript de confirmation
Authentification : Requise


Gestion des Sessions
Variables de session utilisées :

doctor_id : ID du médecin connecté
username : Nom d'utilisateur du médecin

Logique conditionnelle :

Si connecté : Affichage du menu complet (Accueil, Patients, Ajouter, Déconnexion)
Si non connecté : Menu restreint (Accueil, Connexion, Inscription)


Fonctionnalités Transversales
🔄 Gestion des messages

Messages d'erreur : Variable error dans les templates
Messages de succès : Variable success dans les templates
Types d'alertes : alert-danger, alert-success

📊 Prédiction IA

Intégrée au processus d'ajout de patient
Utilise les données médicales pour prédire le risque de diabète
Résultat affiché dans la liste des patients

🎨 Design et UX

Interface responsive avec CSS Grid
Navigation cohérente sur toutes les pages
Icônes emoji pour améliorer l'UX
Validation côté client (HTML5) et serveur


Structure des URLs
/ ────────────────────── Accueil
├── /login ──────────── Connexion
├── /register ───────── Inscription
├── /logout ─────────── Déconnexion
└── /patients ───────── Gestion patients
    ├── /add ────────── Nouveau patient
    ├── /submit ─────── Sauvegarder patient
    └── /delete/<id> ── Supprimer patient