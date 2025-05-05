from fastapi import FastAPI
from api.v1.conference_routes import router

app = FastAPI(title="Conference Manager API")
app.include_router(router, prefix="/api/v1")