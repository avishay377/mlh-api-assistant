from fastapi import FastAPI

from app.api.routes.assistant import router as assistant_router

app = FastAPI(title="MLH API Assistant Backend")

app.include_router(assistant_router)


@app.get("/")
async def root():
    return {"status": "ok"}