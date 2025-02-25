from fastapi import FastAPI
from controllers.root_controller import read_root
from controllers.upload_controller import upload_file
from controllers.query_controller import query_route
from controllers.user_controller import router as user_router
from database.database import Base, engine
from controllers.auth_controller import router as auth_router

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routes
app.get("/")(read_root)
app.post("/upload")(upload_file)
app.get("/query")(query_route)
app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
