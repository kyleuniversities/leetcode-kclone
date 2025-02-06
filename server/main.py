# Imports
from fastapi import FastAPI
import datetime

# Initialize app
app = FastAPI()

# Test GET Method
@app.get("/test")
async def test_get_method():
    return { 'message': f"GET: \"{datetime.datetime.now()}\"" }

# Test POST Method
@app.post("/test")
async def test_post_method():
    return { 'message': f"POST: \"{datetime.datetime.now()}\"" }
