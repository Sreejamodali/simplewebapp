from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import time
from fastapi.responses import RedirectResponse

# ----------------------------
# LOGGING SETUP
# ----------------------------
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ----------------------------
# FASTAPI APP
# ----------------------------
app = FastAPI(title="Cloud Engineering App")

# ----------------------------
# CORS (for frontend/backend split deployment)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# REQUEST LOGGING MIDDLEWARE
# ----------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url}")

    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"Completed: {request.method} {request.url} "
            f"| Status: {response.status_code} "
            f"| Time: {process_time:.2f}ms"
        )

        return response

    except Exception as e:
        logger.exception(f"Error handling request: {request.method} {request.url}")
        raise e

# ----------------------------
# SERVE FRONTEND (STATIC UI)
# ----------------------------
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")

# ----------------------------
# HEALTH CHECK (for Azure monitoring)
# ----------------------------
@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}




@app.get("/")
def root():
    return RedirectResponse(url="/ui")

# ----------------------------
# TASK API
# ----------------------------
@app.get("/tasks")
def get_tasks():
    logger.info("Fetching tasks list")

    tasks = [
        {"id": 1, "task": "Learn Azure"},
        {"id": 2, "task": "Deploy FastAPI"}
    ]

    logger.info(f"Returned {len(tasks)} tasks")
    return tasks