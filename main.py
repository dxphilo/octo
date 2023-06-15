from fastapi import FastAPI
from routes.entry import entry_routes
from routes.user import user_routes

app=FastAPI()

app.include_router(entry_routes)
app.include_router(user_routes)

@app.get('/health')
async def health_check():
    return {'status':'ok 👍 '}






