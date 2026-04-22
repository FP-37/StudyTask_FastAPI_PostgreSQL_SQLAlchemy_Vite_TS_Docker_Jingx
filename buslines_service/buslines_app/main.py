from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from buslines_app.db.init_db import init_db
from buslines_app.api.bus_lines import router as bus_lines_router
from buslines_app.kafka.outbox_relay import start_relay


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_relay()
    yield


app = FastAPI(title="BusLines Service", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bus_lines_router)


@app.get("/health")
def health():
    return {"status": "ok"}
