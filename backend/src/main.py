from time import sleep

import uvicorn
from fastapi import FastAPI

from auth.router import router as auth_router
from auth.service import JWTService

app = FastAPI(
    description="API for Dashboard."
)

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
