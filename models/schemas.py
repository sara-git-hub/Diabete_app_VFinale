from pydantic import BaseModel, Field, field_validator

# =====================================================
# MODÈLES PYDANTIC
# =====================================================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=0, le=120)
    sex: str = Field(..., pattern=r'^(M|F)$')
    glucose: float = Field(..., ge=0, le=300, description="Niveau de glucose")
    bmi: float = Field(..., ge=10, le=50, description="Indice de masse corporelle")
    bloodpressure: float = Field(..., ge=40, le=200, description="Pression artérielle")
    pedigree: float = Field(..., ge=0, le=2, description="Fonction de pedigree du diabète")

    @field_validator('sex')
    def validate_sex(cls, v):
        if v.upper() not in ['M', 'F']:
            raise ValueError('Le sexe doit être M ou F')
        return v.upper()
