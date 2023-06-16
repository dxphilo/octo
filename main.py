from fastapi import FastAPI
from routes.entry import entry_routes
from routes.user import user_routes
from config.config import settings
import uvicorn

app=FastAPI()

app.include_router(entry_routes)
app.include_router(user_routes)

@app.get('/health')
async def health_check():
    return {'status':'ok 👍 '}


if __name__ == "__main__":
    port = int(settings.PORT)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)