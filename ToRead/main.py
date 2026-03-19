from fastapi import FastAPI
import models
from database import engine

app = FastAPI()
#Connecting database
models.Base.metadata.create_all(bind=engine)
