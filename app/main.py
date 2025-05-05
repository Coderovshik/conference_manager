from fastapi import FastAPI
from api.v1.conference_routes import router as conference_router
from api.v1.auth_routes import router as auth_router

app = FastAPI(title="Conference Manager API")
app.include_router(conference_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")