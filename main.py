import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from typing import Optional
import pandas as pd
import joblib
from starlette.middleware.sessions import SessionMiddleware

from models.schemas import UserCreate, UserLogin, PatientCreate 
from models.database import Base, Medecin, Patient, Prediction

# =====================================================
# CONFIGURATION
# =====================================================
# Charger les variables d'environnement
load_dotenv()

# Variables d'environnement pour la base de données
SECRET_KEY = os.getenv("SECRET_KEY")
user = os.getenv("PGUSER")
password = os.getenv("PGPASSWORD")
host = os.getenv("PGHOST")
port = int(os.getenv("PGPORT"))
database = os.getenv("PGDATABASE")

# créer l'application FastAPI
app = FastAPI(title="API Gestion Médicale Minimale", version="1.0.0")

# Middleware pour les sessions
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Configuration des templates Jinja2
templates = Jinja2Templates(directory="templates")

# Configuration de la gestion du hachage des mots de passe avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de données POSTGRESQL
engine = engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Chargement du modèle
try:
    diabetes_model = joblib.load('model.pkl')
except:
    diabetes_model = None

# Créer les tables
Base.metadata.create_all(bind=engine)

# =====================================================
# UTILITAIRES
# =====================================================

# Fonction pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour hasher les mots de passe
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Fonction pour vérifier les mots de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour faire une prédiction de diabète
def predict_diabetes(patient_data: PatientCreate) -> tuple[Optional[int], float]:
    """Faire une prédiction de diabète et retourner (prediction, confidence)"""
    if not diabetes_model:
        return None, 0.0
    
    try:
        # Créer DataFrame avec validation automatique via Pydantic
        df = pd.DataFrame([[
            patient_data.glucose,
            patient_data.bloodpressure,
            patient_data.bmi,
            patient_data.pedigree,
            patient_data.age
        ]], columns=['Glucose', 'BloodPressure', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
        
        prediction = diabetes_model.predict(df)[0]
        prediction_proba = diabetes_model.predict_proba(df)[0]
        confidence = max(prediction_proba) * 100
        
        return int(prediction), round(confidence, 2)
        
    except Exception as e:
        print(f"Erreur lors de la prédiction: {e}")
        return None, 0.0

# =====================================================
# ROUTES D'AUTHENTIFICATION
# =====================================================

# Routes pour l'authentification des médecins
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Route pour soumettre le formulaire de connexion des medecins
@app.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Validation via Pydantic
        login_data = UserLogin(username=username, password=password)
        
        user = db.query(Medecin).filter(Medecin.username == login_data.username).first()
        
        if not user or not verify_password(login_data.password, user.password):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Identifiants incorrects"
            })
        
        request.session["doctor_id"] = user.id
        request.session["username"] = user.username
        
        return RedirectResponse(url="/patients", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": f"Erreur: {str(e)}"
        })

# Route pour afficher le formulaire d'enregistrement
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Route pour soumettre le formulaire d'enregistrement
@app.post("/register")
async def register_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Validation via Pydantic
        user_data = UserCreate(username=username, email=email, password=password)
        
        # Vérifier unicité
        if db.query(Medecin).filter(Medecin.username == user_data.username).first():
            raise HTTPException(400, "Nom d'utilisateur déjà pris")
        
        if db.query(Medecin).filter(Medecin.email == user_data.email).first():
            raise HTTPException(400, "Email déjà utilisé")
        
        # Créer utilisateur
        new_user = Medecin(
            username=user_data.username,
            email=user_data.email,
            password=get_password_hash(user_data.password)
        )
        
        db.add(new_user)
        db.commit()
        
        return templates.TemplateResponse("register.html", {
            "request": request,
            "success": "Compte créé avec succès !"
        })
        
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": str(e)
        })

# Route pour la déconnexion
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

# =====================================================
# ROUTES PRINCIPALES
# =====================================================

# Route d'accueil
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route pour afficher le formulaire d'ajout de patient
@app.get("/add", response_class=HTMLResponse)
async def add_patient_form(request: Request):
    if "doctor_id" not in request.session:
        return RedirectResponse(url="/login")  
    return templates.TemplateResponse("add_patient.html", {"request": request})

# Route pour soumettre le formulaire d'ajout de patient
@app.post("/submit")
async def submit_patient(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    glucose: float = Form(...),
    bmi: float = Form(...),
    bloodpressure: float = Form(...),
    pedigree: float = Form(...),
    db: Session = Depends(get_db)
):
    if "doctor_id" not in request.session:
        return RedirectResponse(url="/login")
    
    try:
        # Validation via Pydantic
        patient_data = PatientCreate(
            name=name, age=age, sex=sex, glucose=glucose,
            bmi=bmi, bloodpressure=bloodpressure, pedigree=pedigree
        )
        
        # Faire la prédiction
        prediction, confidence = predict_diabetes(patient_data)
        
        # Interpréter le résultat
        if prediction is not None:
            result_text = "Diabétique" if prediction == 1 else "Non diabétique"
        else:
            result_text = "Erreur de prédiction"
            prediction = -1
            confidence = 0
        
        # Créer le nouveau patient
        db_patient = Patient(
            doctorid=request.session["doctor_id"],
            name=patient_data.name,
            age=patient_data.age,
            sex=patient_data.sex,
            glucose=patient_data.glucose,
            bmi=patient_data.bmi,
            bloodpressure=patient_data.bloodpressure,
            pedigree=patient_data.pedigree,
            result=result_text
        )
        
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        
        # Enregistrer la prédiction si elle est valide
        if prediction != -1:
            db_prediction = Prediction(
                patientid=db_patient.id,
                result=int(prediction),
                confidence=float(confidence)
            )
            db.add(db_prediction)
            db.commit()
        
        return RedirectResponse(
            url=f"/patients?success=Patient ajouté: {result_text} (Confiance: {confidence:.1f}%)",
            status_code=303
        )
        
    except Exception as e:
        db.rollback()
        return RedirectResponse(
            url=f"/add?error=Erreur: {str(e)}",
            status_code=303
        )

# Route pour afficher la liste des patients et les statistiques
@app.get("/patients", response_class=HTMLResponse)
async def patients_dashboard(request: Request, db: Session = Depends(get_db)):
    if "doctor_id" not in request.session:
        return RedirectResponse(url="/login")
    
    try:
        patients = db.query(Patient).filter(
            Patient.doctorid == request.session["doctor_id"]
        ).order_by(Patient.created_at.desc()).all()
        
        # Statistiques
        total = len(patients)
        diabetic = len([p for p in patients if "Diabétique" in str(p.result)])
        stats = {
            "total": total,
            "diabetic": diabetic,
            "non_diabetic": total - diabetic,
            "diabetic_percentage": round((diabetic / total * 100) if total > 0 else 0, 1)
        }
        
        return templates.TemplateResponse("patients.html", {
            "request": request,
            "patients": patients,
            "stats": stats,
            "success": request.query_params.get("success"),
            "username": request.session.get("username")
        })
        
    except Exception as e:
        return templates.TemplateResponse("patients.html", {
            "request": request,
            "patients": [],
            "stats": {"total": 0, "diabetic": 0, "non_diabetic": 0, "diabetic_percentage": 0},
            "error": str(e)
        })

# Route pour supprimer un patient
@app.post("/delete/{patient_id}")
async def delete_patient(patient_id: int, request: Request, db: Session = Depends(get_db)):
    if "doctor_id" not in request.session:
        return RedirectResponse(url="/login")
    
    try:
        patient = db.query(Patient).filter(
            Patient.id == patient_id,
            Patient.doctorid == request.session["doctor_id"]
        ).first()
        
        if not patient:
            raise HTTPException(404, "Patient non trouvé")
        
        db.delete(patient)
        db.commit()
        
        return RedirectResponse(url="/patients?success=Patient supprimé", status_code=303)
        
    except Exception as e:
        return RedirectResponse(url=f"/patients?error={str(e)}", status_code=303)


# =====================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)

#python -m uvicorn main:app --reload --port 8082