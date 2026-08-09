from fastapi import FastAPI
from app.api.v1.router import router as v1_router


app = FastAPI(
    title="AI Coach",
    description="AI-powered multi-sport training coach",
    version="1.0.0",
)

app.include_router(v1_router)

@app.get("/")
def root():
    return {"message": "AI Coach API"}