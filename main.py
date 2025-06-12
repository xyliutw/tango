# main.py
from fastapi import FastAPI
from Controllers import auth as authAPI, match as matchAPI, user as userAPI, notice as noticeAPI
from Databases.session import Base, engine
from fastapi.openapi.utils import get_openapi
from Models import user, match, notice, user_action

# 建立資料表（開發用，正式環境建議 Alembic）
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "Tango API"
app.version = "0.0.1"
app.include_router(authAPI.router, prefix="/auth", tags=["Auth"])
app.include_router(userAPI.router, prefix="/users", tags=["Users"])
app.include_router(matchAPI.router, prefix="/match", tags=["Match"])
app.include_router(noticeAPI.router, prefix="/notices", tags=["Notices"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Tango API",
        version="1.0.0",
        description="API for Tango",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Welcome to Tango 👋"}
