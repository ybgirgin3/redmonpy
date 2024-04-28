import uvicorn

# from dotenv import dotenv_values
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from routes import execute
from orm import RedOrm

# read env file
# config = dotenv_values(".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    red_mon = RedOrm()
    yield
    red_mon.quit()


app = FastAPI(lifespan=lifespan)

# apply cors (for dev purpose allowed all)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(execute.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
