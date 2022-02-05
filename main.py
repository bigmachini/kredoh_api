import uvicorn
from fastapi import FastAPI
from kredoh.routers import callback,kyanda,kredoh,mpesa

app = FastAPI()
app.include_router(callback.router)
app.include_router(kyanda.router)
app.include_router(kredoh.router)
app.include_router(mpesa.router)



if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8010, reload=True)
