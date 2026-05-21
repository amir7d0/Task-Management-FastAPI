from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .api.routes.tasks import router as tasks_router
from .api.routes.users import router as users_router
from .db import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting up Task Management application...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected")
    print("✅ Application startup complete")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down FastAPI application...")
    if engine:
        engine.dispose()
        print("✅ Database connection closed")
    print("✅ Application shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Task Management API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}


### Static files and templates for using Scalar API Explorer
### If you prefer swagger-ui, you can remove these and the /scalar endpoint

app.mount("/static", StaticFiles(directory= "static"), name="static")
templates = Jinja2Templates(directory= "templates")

@app.get("/scalar", response_class=HTMLResponse, 
         include_in_schema=False)
async def scalar_docs(request: Request):
    return templates.TemplateResponse(
        request,
        "scalar.html",
    )


app.include_router(tasks_router)
app.include_router(users_router)

