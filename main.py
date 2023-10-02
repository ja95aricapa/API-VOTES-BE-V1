from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes import vote
import uvicorn
from config.database import create_db_and_tables

votes = []


# Creates citec_brokerage instance
vote_app = FastAPI(
    title="Vote App",
    description="A simple vote app",
    version="0.0.1",
)


# Adding middlewares
vote_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@vote_app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Adding routers
vote_app.include_router(vote.vote_router)

# Run the server
if __name__ == "__main__":
    uvicorn.run(vote_app, host="0.0.0.0", port=9000)
