import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers.computers import mark_stale_computers, router as computers_router


async def offline_monitor(stop_event: asyncio.Event) -> None:
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=5)
        except TimeoutError:
            db = SessionLocal()
            try:
                mark_stale_computers(db)
            finally:
                db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    stop_event = asyncio.Event()
    monitor_task = asyncio.create_task(offline_monitor(stop_event))
    try:
        yield
    finally:
        stop_event.set()
        await monitor_task


app = FastAPI(title="Lab Management System API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(computers_router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
