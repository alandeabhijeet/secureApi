from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.auth import create_access_token, verify_token, USERS_DB

app = FastAPI(title="Secure Tasks API")
security = HTTPBearer()


class LoginRequest(BaseModel):
    username: str
    password: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return username


@app.post("/login")
def login(request: LoginRequest):
    user = USERS_DB.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/tasks")
def get_tasks(current_user: str = Depends(get_current_user)):
    tasks = [
        {"id": 1, "title": "Complete assignment", "status": "pending"},
        {"id": 2, "title": "Review code", "status": "done"},
        {"id": 3, "title": "Deploy application", "status": "in-progress"},
    ]
    return {"user": current_user, "tasks": tasks}
