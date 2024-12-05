from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engines.sql_engine import Base, engine
from middleware import AuthenticationMiddleware, FILE_PATH
from sqlalchemy.ext.asyncio import AsyncEngine
from handlers.users_handler import router as users_router
from handlers.authentication_handler import router as authentication_router
from handlers.foods_handler import router as foods_router
from handlers.orders_handler import router as orders_router
from handlers.vendors_handler import router as vendors_router
from handlers.restaurant_handler import router as restaurants_router
from RBAC.create_RBAC_config import update_routes_json

# create tables in the db if don't exist
async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# drop tables only for development 
async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# create app
app = FastAPI()

# add all routers to app
app.include_router(users_router)
app.include_router(authentication_router)
app.include_router(foods_router)
app.include_router(orders_router)
app.include_router(vendors_router)
app.include_router(restaurants_router)

# check for tables creation on the startup
@app.on_event("startup")
async def on_startup():
    # update routes config file 
    update_routes_json(app, file_path=FILE_PATH)
    await create_tables(engine)
    
# drop tables endpoint to drop all tables and data in db (only for development)
@app.get("/drop-tables")
async def drop_tables_route():
    await drop_tables(engine)
    return {"message": "tables has been dropped!"}

# configure CORS middleware (allowed to everyone for now)
origins = ["*"]

# Middlewares

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add token verfication, authentication, and RBAC middlware. Doing it on middlware level before each request so 
# could seperate the logic from endpoint level. Will allow moving to micro-servies easily.
app.add_middleware(AuthenticationMiddleware)

# home route
@app.get("/")
def home():
    return "Hello from foody!"