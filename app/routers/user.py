from fastapi import Body, status, HTTPException, Depends, APIRouter 
                                                        ## Response imports error codes
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

# Cant simply import app object, need api router object
router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

# Tags allows for cleaner organization on FastAPI Docs Page

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def createUser(newUser: schemas.UserCreate, db: Session = Depends(get_db)):

    search = db.query(models.User).filter(models.User.email == newUser.email)


    if search.first() != None:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT,
       detail = f"user with email: {newUser.email} cannot be created, already exists.")
    
    
    # Before making user instance, we must hash password
    # Here, password context is declared on first line, is passlib instance used to encrypt
    #   passwords on PostgreSQL database.
    # PassLib instance has hash method, which takes string and returns hashified version, no modif
    hashed_password = utils.hash(newUser.password)
    newUser.password = hashed_password
    # Since user is pydantic object, we can convert to dict, then create SQLAlchemy version
    user = models.User(**newUser.dict()) ## creates instance of new user

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}", response_model=schemas.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} does not exist")

    return user # This will return according to schema from UserResponse