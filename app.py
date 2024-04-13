import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import post

# read env file
config = dotenv_values(".env")

app = FastAPI()

# apply cors (for dev purpose allowed all)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def start_db_client():
    """
    _summary_: connect mongodb client at the start of the app
    :return: None
    """
    # TODO: connect redis
    pass


@app.on_event("shutdown")
def stop_db_client():
    """
    __summary__: close connection at the end of the app

    :return: None
    """
    app.mongo_client.close()


app.include_router(post.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
