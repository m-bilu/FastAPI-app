import sys
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware # USED TO BYPASS CORS



# REMOVE THIS LATER / FIX ISSUE !
sys.setrecursionlimit(30000)

# Line creates tables on postgreSQL
# models.Base.metadata.create_all(bind=engine)
# THE LINE ABOVE was mainly used for sqlalchemy, we now use alembic for this stuff, so line is commented outk


app = FastAPI() ## function from the FastAPI library that creates an instance of the API object

origins = ["*"] ## THIS SHOULD ONLY BE THE WEBAPPS UR WORKING WITH

# STUFF FROM FASTAPI DOCUMENTATION TO BYPASS CORS
app.add_middleware(
    CORSMiddleware,   # MIDDLEWARE IS A FUNCTION THAT RUNS B4 EVERY REQUEST
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



## Connection with PostgreSQL server



# THESE 2 commands connect the router in post, user to the main app instance
# Router object helps seperating and connecting funtionality across filesk
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")                                   ## 3 LINES are path operation
def root():                                      ## async keyword OPTIONAL: tasks like API calls, talking
                                                ## to database, will remove for now

    ## app.get is an http method (get, put, post, delete, etc) WHAT ARE THESE?!
        ## Also a decorator, @ represents decorator.
    ## ("/") root path name to site, google.com/ is home page of google, etc
    ## ("/post/vote") take you to this specific url


    return {"message": "Welcome to my API!!"}
    ## Do not use --reload when uvicorning when submitting production

#######################################################################

















