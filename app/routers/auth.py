from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags = ["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(userCred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == userCred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    # Comparing new plain password, database-saved hash password for authenticity
    if not utils.verify(userCred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    # Create a token using oauth2 file
    accessToken = oauth2.createToken(data = {"userID" : user.id})

    # Return token to valid user, what is a bearer token?!?!
    return {"accessToken" : accessToken, "tokenType" : "bearer", "id" : user.id}
    #return oauth2.getCurrentUser(accessToken)