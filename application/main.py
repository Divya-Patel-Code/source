from fastapi import FastAPI
from application.db.session import Base, engine
from application.api import provider_routes, connection_routes

app = FastAPI()

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(provider_routes.router, prefix="/api/v1", tags=["Providers API"])
app.include_router(connection_routes.router, prefix="/api/v1", tags=["Connection API"])