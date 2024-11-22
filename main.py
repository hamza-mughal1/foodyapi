from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engines.sql_engine import Base, engine
from schemas.db_schemas import *
from sqlalchemy.ext.asyncio import AsyncEngine

# create all tables and objects in the db if don't exist


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# create app
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_tables(engine)

# configure CORS middleware (allowed to everyone for now)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# home route
@app.get("/")
def home():
    return "Hello from foody!"