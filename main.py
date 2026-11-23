import sqlite3
import uuid
from datetime import datetime, timezone
import bcrypt
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

DB_NAME = "crashcall.db"

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'citizen',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

app = FastAPI(
    title="CrashCall API",
    version="1.0.0",
    description="Emergency Response & Citizen Safety Platform API"
)

# Enable CORS for frontend/mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class UserRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    phone: str = Field(..., min_length=7, max_length=15, example="+919876543210")
    password: str = Field(..., min_length=6, max_length=128, example="SecretPassword123")

class UserResponseData(BaseModel):
    user_id: str
    full_name: str
    email: str
    phone: str
    role: str
    created_at: str

class UserRegisterResponse(BaseModel):
    status: str = "success"
    message: str = "User registered successfully"
    data: UserResponseData


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "CrashCall API",
        "docs_url": "/docs"
    }

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post(
    "/api/v1/auth/users/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterResponse,
    tags=["Auth"],
    summary="Register a new citizen/user account",
    description="Registers a new user into CrashCall. Validates credentials, securely hashes the password, and stores the user profile."
)
def register_user(payload: UserRegisterRequest):
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    
    # Securely hash password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), salt).decode('utf-8')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if email or phone already exists
    cursor.execute("SELECT email, phone FROM users WHERE email = ? OR phone = ?", (payload.email, payload.phone))
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        existing_email, existing_phone = existing
        if existing_email == payload.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email address already exists."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this phone number already exists."
            )
    
    # Insert new user
    cursor.execute(
        """
        INSERT INTO users (id, full_name, email, phone, password_hash, role, created_at)
        VALUES (?, ?, ?, ?, ?, 'citizen', ?)
        """,
        (user_id, payload.full_name, payload.email, payload.phone, password_hash, created_at)
    )
    conn.commit()
    conn.close()

    return UserRegisterResponse(
        status="success",
        message="User registered successfully",
        data=UserResponseData(
            user_id=user_id,
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
            role="citizen",
            created_at=created_at
        )
    )
