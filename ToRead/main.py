from fastapi import FastAPI

try:
    # Recommended (run from repo root): `uvicorn ToRead.main:app --reload`
    from . import models
    from .database import engine
    from .routers import auth, todos
except ImportError:  # pragma: no cover
    # When running from inside `ToRead/`: `uvicorn main:app --reload`
    import models
    from database import engine
    from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
