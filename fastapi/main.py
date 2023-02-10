from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/home")
async def home():
    return {"Response" : "This is the home path."}