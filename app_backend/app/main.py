from fastapi import FastAPI
import logging

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

logging.basicConfig(level=logging.INFO)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    logging.info("Home endpoint called")
    return {"message": "App is running"}

@app.get("/tasks")
def get_tasks():
    return [{"id": 1, "task": "Learn Azure"}]