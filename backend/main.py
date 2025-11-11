from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from routes import jobs
import requests

app = FastAPI()

# Allow frontend origins (localhost + any random Angular port)
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ✅ allowed origins
    allow_credentials=True,
    allow_methods=["*"],             # ✅ allow all HTTP methods
    allow_headers=["*"],             # ✅ allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}


app.include_router(jobs.router)
