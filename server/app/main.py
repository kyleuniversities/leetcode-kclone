# Imports
from fastapi import FastAPI
from .database import models
from .database import database
from .router import user
import datetime

# Initialize app
app = FastAPI()

# Bind Database Engine
models.Base.metadata.create_all(bind=database.engine)

# Test GET Method
@app.get("/test")
async def test_get_method():
    return { 'message': f"GET: \"{datetime.datetime.now()}\"" }

# Test POST Method
@app.post("/test")
async def test_post_method():
    return { 'message': f"POST: \"{datetime.datetime.now()}\"" }

# Include Routers
app.include_router(user.router)