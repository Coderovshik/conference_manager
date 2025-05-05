from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.v1.conference_routes import router as conference_router
from api.v1.auth_routes import router as auth_router

app = FastAPI(title="Conference Manager API")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Маршрут для главной страницы
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Подключаем маршруты API
app.include_router(conference_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")